"""
Testes para os scrapers do projeto.
"""
import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Adiciona o diretório parent ao path
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir))

# Importa os módulos do scraper
from scraper.main import scrape_amazon, scrape_mercadolivre, get_browser
from scraper.models import Offer


@pytest.fixture
def mock_browser():
    """
    Fixture que simula um navegador Playwright.
    """
    browser = MagicMock()
    page = MagicMock()
    browser.new_page.return_value = page
    
    # Configura o método page.goto para não fazer nada
    page.goto = MagicMock()
    
    # Configura o método page.evaluate para retornar HTML falso
    page.content = MagicMock(return_value="<html><body><div>Mock HTML</div></body></html>")
    
    # Configura screenshot
    page.screenshot = MagicMock()
    
    return browser, page


def test_get_browser():
    """
    Testa a função get_browser verificando se retorna um objeto válido.
    """
    with patch('playwright.sync_api.sync_playwright') as mock_playwright:
        mock_instance = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_instance
        
        mock_browser = MagicMock()
        mock_instance.chromium.launch.return_value = mock_browser
        
        browser = get_browser()
        
        # Verifica se o browser foi inicializado corretamente
        assert browser is not None
        assert mock_instance.chromium.launch.called


@pytest.mark.parametrize("keyword", ["smartphone", "notebook"])
def test_scrape_amazon(mock_browser, keyword):
    """
    Testa a função scrape_amazon em cenários diferentes.
    """
    browser, page = mock_browser
    
    # Mock para o context manager async_playwright()
    mock_context = MagicMock()
    mock_context.__aenter__.return_value.chromium.launch = MagicMock(return_value=browser)
    
    # Configura o método querySelectorAll para retornar elementos fictícios
    mock_elements = []
    for i in range(3):
        mock_element = MagicMock()
        mock_element.inner_text = MagicMock(return_value=f"Produto Amazon {i}")
        mock_element.get_attribute = MagicMock(return_value=f"https://amazon.com.br/dp/B0{i}")
        mock_elements.append(mock_element)
    
    # Configura para retornar uma lista de elementos
    page.query_selector_all = MagicMock(return_value=mock_elements)
    
    # Configura os métodos querySelector para retornar atributos específicos
    title_mock = MagicMock()
    title_mock.inner_text = MagicMock(return_value="Título do produto")
    page.query_selector = MagicMock(return_value=title_mock)
    
    # Simula funções específicas de extração de preço
    def mock_extract_price(*args, **kwargs):
        return 1000.0, 800.0
    
    # Simula funções específicas de extração de ID
    def mock_extract_id(*args, **kwargs):
        return "B0123456789"
    
    # Aplica os mocks
    with patch('playwright.async_api.async_playwright', return_value=mock_context):
        with patch('scraper.main.extract_amazon_price', mock_extract_price):
            with patch('scraper.main.extract_external_id', mock_extract_id):
                # Executa a função a ser testada em um loop de eventos
                import asyncio
                offers = asyncio.run(scrape_amazon(keyword=keyword, max_pages=1))
                
                # Verifica se as ofertas foram criadas corretamente
                assert len(offers) > 0
                for offer in offers:
                    assert isinstance(offer, Offer)
                    assert offer.merchant == "amazon"
                    assert offer.url.startswith("https://")
                    assert offer.price > 0


def test_scrape_mercadolivre(mock_browser):
    """
    Testa a função scrape_mercadolivre.
    """
    browser, page = mock_browser
    
    # Mock para o context manager async_playwright()
    mock_context = MagicMock()
    mock_context.__aenter__.return_value.chromium.launch = MagicMock(return_value=browser)
    
    # Configura o método querySelectorAll para retornar elementos fictícios
    mock_elements = []
    for i in range(3):
        mock_element = MagicMock()
        mock_elements.append(mock_element)
    
    def query_selector_all_side_effect(selector):
        if any(s in selector for s in ["promotion-item", "items_container", "dynamic-carousel__item"]):
            return mock_elements
        return []
    
    page.query_selector_all = MagicMock(side_effect=query_selector_all_side_effect)
    
    # Simula que os seletores de títulos e URLs retornam valores válidos
    def mock_query_selector(selector):
        title_mock = MagicMock()
        if any(s in selector for s in ["title", "name"]):
            title_mock.inner_text = MagicMock(return_value="Produto Mercado Livre")
            return title_mock
        elif any(s in selector for s in ["link", "href", "a"]):
            title_mock.get_attribute = MagicMock(return_value="https://www.mercadolivre.com.br/p/MLB12345")
            return title_mock
        elif any(s in selector for s in ["price", "valor"]):
            title_mock.inner_text = MagicMock(return_value="R$ 799,90")
            return title_mock
        else:
            return None
    
    page.query_selector = MagicMock(side_effect=mock_query_selector)
    
    # Simula funções específicas de extração
    with patch('playwright.async_api.async_playwright', return_value=mock_context):
        with patch('scraper.main.extract_mercadolivre_price', return_value=(1000.0, 800.0)):
            with patch('scraper.main.extract_external_id', return_value="MLB12345"):
                # Executa a função a ser testada em um loop de eventos
                import asyncio
                offers = asyncio.run(scrape_mercadolivre(max_pages=1))
                
                # Verifica se as ofertas foram criadas corretamente
                assert len(offers) > 0
                for offer in offers:
                    assert isinstance(offer, Offer)
                    assert offer.merchant == "mercadolivre"
                    assert offer.url.startswith("https://")
                    assert offer.price > 0 