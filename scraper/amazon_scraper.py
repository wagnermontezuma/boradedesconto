"""
Script para coletar ofertas da Amazon e salvá-las no banco de dados.
Script simplificado para teste.
"""
import asyncio
import os
import sys
from pathlib import Path

# Adiciona o diretório parent ao PYTHONPATH
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from playwright.async_api import async_playwright
import random
import datetime
from api.models import Offer, upsert_offer, init_db


async def scrape_amazon_offers(keyword="ofertas do dia", max_pages=2, max_offers=10):
    """Coleta ofertas da Amazon."""
    print(f"Iniciando scraping da Amazon para: {keyword}")
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        page = await context.new_page()
        
        # Configura a página com headers úteis
        await page.set_extra_http_headers({
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        })
        
        # Navega para a página inicial de ofertas
        base_url = f"https://www.amazon.com.br/s?k={keyword.replace(' ', '+')}"
        print(f"Navegando para: {base_url}")
        await page.goto(base_url, wait_until="domcontentloaded")
        
        # Tira um screenshot para debug
        screenshot_path = Path(__file__).parent / "amazon_page.png"
        await page.screenshot(path=str(screenshot_path))
        print(f"Screenshot salvo em: {screenshot_path}")
        
        # Para cada página de resultados
        for page_num in range(1, max_pages + 1):
            print(f"Processando página {page_num}")
            
            # Espera pequena para carregar JavaScript
            await page.wait_for_timeout(2000)
            
            # Tenta localizar produtos usando diferentes seletores
            selectors = [
                '[data-component-type="s-search-result"]',
                '.s-result-item.s-asin',
                '.s-card-container',
                '.sg-col-20-of-24 > .s-result-item'
            ]
            
            products = []
            for selector in selectors:
                try:
                    products = await page.query_selector_all(selector)
                    if products and len(products) > 0:
                        print(f"Encontrados {len(products)} produtos com seletor '{selector}'")
                        break
                except Exception as e:
                    print(f"Erro com seletor '{selector}': {str(e)}")
            
            if not products:
                print("Não foi possível encontrar produtos nesta página.")
                continue
            
            # Processa cada produto encontrado (limitando ao máximo)
            for i, product in enumerate(products[:max_offers]):
                try:
                    # Extrai ASIN (ID do produto da Amazon)
                    asin = await product.get_attribute('data-asin')
                    if not asin:
                        # Tenta extrair de outro atributo/seletor
                        asin_el = await product.query_selector('[data-asin]')
                        if asin_el:
                            asin = await asin_el.get_attribute('data-asin')
                    
                    if not asin or asin == "":
                        print("Produto sem ASIN válido, pulando...")
                        continue
                        
                    print(f"Processando produto com ASIN: {asin}")
                    
                    # Extrai título
                    title = "Sem título"
                    title_selectors = [
                        'h2 a span',
                        '.a-text-normal',
                        '.a-link-normal .a-text-normal',
                        '.a-color-base.a-text-normal'
                    ]
                    
                    for title_selector in title_selectors:
                        title_el = await product.query_selector(title_selector)
                        if title_el:
                            title_text = await title_el.inner_text()
                            if title_text and len(title_text.strip()) > 0:
                                title = title_text.strip()
                                break
                    
                    print(f"Título: {title[:50]}...")
                    
                    # Extrai URL
                    url = ""
                    link_selectors = [
                        'h2 a',
                        '.a-link-normal',
                        '.a-link-normal[href*="/dp/"]'
                    ]
                    
                    for link_selector in link_selectors:
                        link_el = await product.query_selector(link_selector)
                        if link_el:
                            href = await link_el.get_attribute('href')
                            if href and '/dp/' in href:
                                if href.startswith('/'):
                                    url = f"https://www.amazon.com.br{href}"
                                else:
                                    url = href
                                break
                    
                    # Se não encontrou URL, constrói com o ASIN
                    if not url and asin:
                        url = f"https://www.amazon.com.br/dp/{asin}"
                        
                    # Adiciona o ID de afiliado
                    if url and "amazon.com.br" in url and "tag=" not in url:
                        separator = "&" if "?" in url else "?"
                        url = f"{url}{separator}tag=wagnermontezu-20"
                        
                    print(f"URL: {url[:50]}...")
                    
                    # Extrai preço atual (simplificado)
                    price = 0.0
                    price_selectors = [
                        '.a-price .a-offscreen',
                        '.a-price-whole',
                        '.a-color-price'
                    ]
                    
                    for price_selector in price_selectors:
                        price_el = await product.query_selector(price_selector)
                        if price_el:
                            price_text = await price_el.inner_text()
                            if price_text:
                                try:
                                    # Formato de preço BR: R$ 1.234,56
                                    price_clean = price_text.replace("R$", "").replace(".", "").replace(",", ".").strip()
                                    price = float(price_clean)
                                    if price > 0:
                                        break
                                except:
                                    continue
                    
                    # Se não encontrou preço, usa valor aleatório para teste
                    if price == 0:
                        price = random.uniform(50, 500)
                        print("⚠️ Preço não encontrado, usando valor aleatório.")
                    
                    # Para teste, define um desconto aleatório
                    discount_pct = random.randint(10, 60)
                    
                    print(f"Preço: R${price:.2f}, Desconto: {discount_pct}%")
                    
                    # Adiciona a oferta à lista
                    if price > 0 and asin and url and title != "Sem título":
                        offer = Offer(
                            merchant="amazon",
                            external_id=asin,
                            title=title,
                            url=url,
                            price=price,
                            discount_pct=discount_pct,
                            ts=datetime.datetime.utcnow()
                        )
                        
                        results.append(offer)
                        print(f"✅ Oferta válida: {title[:30]}... - R${price:.2f} ({discount_pct}% OFF)")
                    else:
                        print(f"❌ Oferta ignorada - dados incompletos")
                
                except Exception as e:
                    print(f"Erro ao processar produto: {str(e)}")
            
            # Se já temos resultados suficientes, paramos
            if len(results) >= max_offers:
                print(f"Já coletamos {len(results)} ofertas, parando.")
                break
        
        await browser.close()
    
    print(f"Amazon: coletadas {len(results)} ofertas")
    return results


async def main():
    """Função principal"""
    # Inicializa o banco
    await init_db()
    print("Banco de dados inicializado")
    
    # Coleta ofertas da Amazon
    print("Coletando ofertas da Amazon...")
    keyword = "ofertas do dia eletronicos"
    offers = await scrape_amazon_offers(keyword=keyword, max_pages=2, max_offers=10)
    
    # Salva no banco
    if offers:
        print(f"Salvando {len(offers)} ofertas no banco...")
        for offer in offers:
            await upsert_offer(offer)
        print("✅ Ofertas salvas com sucesso!")
    else:
        print("❌ Nenhuma oferta encontrada!")


if __name__ == "__main__":
    asyncio.run(main()) 