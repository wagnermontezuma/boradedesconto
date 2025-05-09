import pytest
import pytest_asyncio
from pathlib import Path
import sys
import os
from datetime import datetime
import asyncio

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from scraper.main import scrape_amazon
from scraper.models import Offer as ScraperOffer
from api.models import Offer as ApiOfferModel
from api.models import init_db as init_api_db

import aiosqlite

MOCK_HTML_FILE_SCRAPER_INTEGRATION = Path(__file__).parent / "mock_amazon_page.html"

SCRAPER_TEST_DB_PATH = ":memory:"

@pytest_asyncio.fixture(scope="function")
async def scraper_test_db_conn():
    original_get_db_path_api = None
    
    async def mock_get_db_path_for_scraper_api_module():
        return SCRAPER_TEST_DB_PATH

    import api.models as api_models_module_for_scraper
    if hasattr(api_models_module_for_scraper, 'get_db_path'):
        original_get_db_path_api = api_models_module_for_scraper.get_db_path
    api_models_module_for_scraper.get_db_path = mock_get_db_path_for_scraper_api_module

    await init_api_db()
    
    conn = await aiosqlite.connect(SCRAPER_TEST_DB_PATH)
    conn.row_factory = aiosqlite.Row
    yield conn
    
    await conn.close()
    if SCRAPER_TEST_DB_PATH != ":memory:" and Path(SCRAPER_TEST_DB_PATH).exists():
        os.remove(SCRAPER_TEST_DB_PATH)
    
    if original_get_db_path_api:
        api_models_module_for_scraper.get_db_path = original_get_db_path_api

@pytest.mark.asyncio
async def test_scrape_amazon_integration_with_mock_html(scraper_test_db_conn, monkeypatch):
    original_goto = None
    
    async def mock_page_goto(self, url, **kwargs):
        nonlocal original_goto
        if original_goto:
            return await original_goto(self, f"file://{MOCK_HTML_FILE_SCRAPER_INTEGRATION.resolve()}", **kwargs)
        raise Exception("Original goto not captured")

    from playwright.async_api import Page as PlaywrightPage
    if hasattr(PlaywrightPage, 'goto'):
        original_goto = PlaywrightPage.goto
    monkeypatch.setattr(PlaywrightPage, "goto", mock_page_goto)

    try:
        await scrape_amazon(keyword="test_keyword_ignored", max_pages=1)

        async with scraper_test_db_conn as conn:
            cursor = await conn.execute("SELECT * FROM offers ORDER BY external_id ASC")
            rows = await cursor.fetchall()

            assert len(rows) == 3

            assert rows[0]["external_id"] == "ASIN001"
            assert rows[0]["title"] == "Título do Produto 1"
            assert rows[0]["price"] == 99.90
            assert rows[0]["discount_pct"] == 50 
            assert "tag=wagnermontezu-20" in rows[0]["url"]

            assert rows[1]["external_id"] == "ASIN002"
            assert rows[1]["title"] == "Título do Produto 2 Super Desconto"
            assert rows[1]["price"] == 145.99
            assert rows[1]["discount_pct"] == 0
            
            assert rows[2]["external_id"] == "ASIN003"
            assert rows[2]["title"] == "Produto Sem Preço"
            assert rows[2]["price"] == 0.0 
            assert rows[2]["discount_pct"] == 0

    finally:
        if original_goto:
            monkeypatch.setattr(PlaywrightPage, "goto", original_goto) 