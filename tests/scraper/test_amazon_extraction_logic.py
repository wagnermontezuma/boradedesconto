import pytest
import pytest_asyncio
from pathlib import Path
import sys
from playwright.async_api import async_playwright, Page
from typing import List, Dict, Any

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from scraper.utils import format_price, calculate_discount 
from scraper.models import Offer as ScraperOffer

MOCK_HTML_FILE = Path(__file__).parent / "mock_amazon_page.html"

async def extract_offers_from_page_content(page: Page) -> List[ScraperOffer]:
    extracted_offers = []
    product_elements = await page.query_selector_all('[data-component-type="s-search-result"]')

    for product in product_elements:
        asin = await product.get_attribute('data-asin')
        if not asin:
            continue

        title_el = await product.query_selector('h2 a span')
        title = await title_el.inner_text() if title_el else "Sem título"

        url_el = await product.query_selector('h2 a')
        url_path = await url_el.get_attribute('href') if url_el else ""
        full_url = f"https://www.amazon.com.br{url_path}" if url_path.startswith('/') else url_path
        if "amazon.com.br" in full_url and "tag=" not in full_url:
             separator = "&" if "?" in full_url else "?"
             full_url = f"{full_url}{separator}tag=wagnermontezu-20"

        price_text_el = await product.query_selector('.a-price .a-offscreen')
        price_text = await price_text_el.inner_text() if price_text_el else None
        
        if not price_text:
            price_whole_el = await product.query_selector('.a-price-whole')
            price_fraction_el = await product.query_selector('.a-price-fraction')
            if price_whole_el and price_fraction_el:
                price_whole = await price_whole_el.inner_text()
                price_fraction = await price_fraction_el.inner_text()
                price_text = f"{price_whole},{price_fraction}"

        current_price = format_price(price_text)

        original_price_el = await product.query_selector('.a-text-price .a-offscreen')
        original_price_text = await original_price_el.inner_text() if original_price_el else None
        original_price = format_price(original_price_text) if original_price_text else current_price

        discount_pct = calculate_discount(original_price, current_price)

        offer = ScraperOffer(
            title=title.strip(),
            price=current_price,
            url=full_url,
            merchant="amazon",
            external_id=asin,
            discount_pct=discount_pct,
            original_price=original_price
        )
        extracted_offers.append(offer)
        
    return extracted_offers


@pytest_asyncio.fixture(scope="module")
async def browser_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file://{MOCK_HTML_FILE.resolve()}")
        yield page
        await browser.close()

@pytest.mark.asyncio
async def test_extract_data_from_mock_amazon_html(browser_page: Page):
    offers = await extract_offers_from_page_content(browser_page)
    
    assert len(offers) == 3

    offer1 = next((o for o in offers if o.external_id == "ASIN001"), None)
    assert offer1 is not None
    assert offer1.title == "Título do Produto 1"
    assert offer1.price == 99.90
    assert offer1.original_price == 199.80
    assert offer1.discount_pct == 50
    assert "tag=wagnermontezu-20" in offer1.url

    offer2 = next((o for o in offers if o.external_id == "ASIN002"), None)
    assert offer2 is not None
    assert offer2.title == "Título do Produto 2 Super Desconto"
    assert offer2.price == 145.99
    assert offer2.original_price == 145.99
    assert offer2.discount_pct == 0
    assert "tag=wagnermontezu-20" in offer2.url

    offer3 = next((o for o in offers if o.external_id == "ASIN003"), None)
    assert offer3 is not None
    assert offer3.title == "Produto Sem Preço"
    assert offer3.price == 0.0
    assert offer3.discount_pct == 0 