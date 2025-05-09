import pytest
import pytest_asyncio # Para fixtures assíncronas
from pathlib import Path
import sys
import os
from datetime import datetime

# Ajustar o PYTHONPATH
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from api.models import Offer, init_db, upsert_offer, get_offer_by_id, get_offers
import aiosqlite

# Usar um banco de dados em memória para testes
TEST_DB_PATH = ":memory:"
# Ou, para inspecionar após o teste, um arquivo temporário:
# TEST_DB_PATH = "test_deals.db"


@pytest_asyncio.fixture
async def db_conn():
    # Substitui o get_db_path original para usar o banco de teste
    original_get_db_path = None
    
    async def mock_get_db_path():
        return TEST_DB_PATH

    # Monkeypatch a função get_db_path dentro do módulo api.models
    # para que todas as funções do módulo usem nosso banco de teste.
    # É crucial que o patch seja feito no local onde a função é *usada*.
    import api.models
    if hasattr(api.models, 'get_db_path'):
        original_get_db_path = api.models.get_db_path
    api.models.get_db_path = mock_get_db_path

    # Inicializa o esquema no banco em memória/teste
    await init_db()
    
    conn = await aiosqlite.connect(TEST_DB_PATH)
    conn.row_factory = aiosqlite.Row # Para acessar colunas por nome
    yield conn # Fornece a conexão para os testes
    
    # Limpeza após os testes
    await conn.close()
    if TEST_DB_PATH != ":memory:" and Path(TEST_DB_PATH).exists():
        os.remove(TEST_DB_PATH)
    
    # Restaura a função original se foi mockada
    if original_get_db_path:
        api.models.get_db_path = original_get_db_path


@pytest.mark.asyncio
async def test_init_db(db_conn):
    # Verifica se as tabelas foram criadas
    cursor = await db_conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='offers'")
    table = await cursor.fetchone()
    assert table is not None
    assert table['name'] == 'offers'

    cursor = await db_conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='offer_clicks'")
    table = await cursor.fetchone()
    assert table is not None
    assert table['name'] == 'offer_clicks'

@pytest.mark.asyncio
async def test_upsert_and_get_offer(db_conn):
    offer_data = {
        "merchant": "test_merchant",
        "external_id": "test_ext_id_1",
        "title": "Test Offer 1",
        "url": "http://example.com/offer1",
        "price": 99.99,
        "discount_pct": 10,
        "ts": datetime.utcnow() # Pydantic model vai usar o seu default_factory se não fornecido
    }
    offer_obj = Offer(**offer_data)
    
    # Teste Insert
    await upsert_offer(offer_obj)
    
    cursor = await db_conn.execute(
        "SELECT * FROM offers WHERE merchant = ? AND external_id = ?",
        (offer_data["merchant"], offer_data["external_id"])
    )
    inserted_offer_row = await cursor.fetchone()
    assert inserted_offer_row is not None
    assert inserted_offer_row["title"] == offer_data["title"]
    assert inserted_offer_row["price"] == offer_data["price"]
    
    # Teste Update (Upsert)
    updated_offer_data = offer_data.copy()
    updated_offer_data["price"] = 79.99
    updated_offer_data["ts"] = datetime.utcnow()
    
    updated_offer_obj = Offer(**updated_offer_data)
    await upsert_offer(updated_offer_obj)
    
    cursor = await db_conn.execute(
        "SELECT * FROM offers WHERE merchant = ? AND external_id = ?",
        (offer_data["merchant"], offer_data["external_id"])
    )
    updated_offer_row = await cursor.fetchone()
    assert updated_offer_row is not None
    assert updated_offer_row["price"] == 79.99
    assert updated_offer_row["title"] == offer_data["title"]

    cursor = await db_conn.execute("SELECT COUNT(*) as count FROM offers")
    count_row = await cursor.fetchone()
    assert count_row["count"] == 1

    retrieved_offer_pydantic = await get_offer_by_id(inserted_offer_row["id"])
    assert retrieved_offer_pydantic is not None
    assert retrieved_offer_pydantic["title"] == updated_offer_data["title"]
    assert retrieved_offer_pydantic["price"] == updated_offer_data["price"]

# Dados de exemplo para múltiplos ofertas
OFFER_1_DATA = {
    "merchant": "merchant_A", "external_id": "ext_1", "title": "Offer A1", 
    "url": "http://a1.com", "price": 100.0, "discount_pct": 10, "ts": datetime(2023, 1, 1, 10, 0, 0)
}
OFFER_2_DATA = {
    "merchant": "merchant_B", "external_id": "ext_2", "title": "Offer B1",
    "url": "http://b1.com", "price": 200.0, "discount_pct": 20, "ts": datetime(2023, 1, 1, 11, 0, 0)
}
OFFER_3_DATA = {
    "merchant": "merchant_A", "external_id": "ext_3", "title": "Offer A2 High Discount",
    "url": "http://a2.com", "price": 50.0, "discount_pct": 50, "ts": datetime(2023, 1, 1, 12, 0, 0)
}

@pytest.mark.asyncio
async def test_get_offers_filtering_and_pagination(db_conn):
    # Popular com algumas ofertas
    await upsert_offer(Offer(**OFFER_1_DATA))
    await upsert_offer(Offer(**OFFER_2_DATA))
    await upsert_offer(Offer(**OFFER_3_DATA))

    # Teste 1: Sem filtros (deve retornar todos, ordenado por ts DESC)
    all_offers = await get_offers(limit=5)
    assert len(all_offers) == 3
    assert all_offers[0]["title"] == "Offer A2 High Discount" # Mais recente
    assert all_offers[1]["title"] == "Offer B1"
    assert all_offers[2]["title"] == "Offer A1"

    # Teste 2: Filtrar por merchant
    merchant_a_offers = await get_offers(merchant="merchant_A", limit=5)
    assert len(merchant_a_offers) == 2
    assert all(o["merchant"] == "merchant_A" for o in merchant_a_offers)
    assert merchant_a_offers[0]["title"] == "Offer A2 High Discount"

    # Teste 3: Filtrar por min_discount
    high_discount_offers = await get_offers(min_discount=30, limit=5)
    assert len(high_discount_offers) == 1
    assert high_discount_offers[0]["title"] == "Offer A2 High Discount"
    assert high_discount_offers[0]["discount_pct"] == 50

    # Teste 4: Paginação (limit e offset)
    page1 = await get_offers(limit=1, offset=0)
    assert len(page1) == 1
    assert page1[0]["title"] == "Offer A2 High Discount"

    page2 = await get_offers(limit=1, offset=1)
    assert len(page2) == 1
    assert page2[0]["title"] == "Offer B1"
    
    page3 = await get_offers(limit=2, offset=1)
    assert len(page3) == 2
    assert page3[0]["title"] == "Offer B1"
    assert page3[1]["title"] == "Offer A1"

    # Teste 5: Filtro combinado
    combo_filter = await get_offers(merchant="merchant_A", min_discount=40, limit=5)
    assert len(combo_filter) == 1
    assert combo_filter[0]["title"] == "Offer A2 High Discount"


from api.models import register_offer_click, get_offer_clicks_stats, OfferClick
import asyncio # Adicionado aqui

@pytest.mark.asyncio
async def test_register_and_get_offer_clicks(db_conn):
    await upsert_offer(Offer(**OFFER_1_DATA))
    cursor = await db_conn.execute("SELECT id FROM offers WHERE external_id = ?", (OFFER_1_DATA["external_id"],))
    offer_row = await cursor.fetchone()
    offer_id_1 = offer_row["id"]

    click1 = await register_offer_click(offer_id=offer_id_1, user_agent="agent1", referer="ref1")
    assert isinstance(click1, OfferClick)
    assert click1.offer_id == offer_id_1
    assert click1.id is not None

    await register_offer_click(offer_id=offer_id_1, user_agent="agent2")
    await asyncio.sleep(0.01)
    await register_offer_click(offer_id=offer_id_1, user_agent="agent3")

    cursor = await db_conn.execute("SELECT COUNT(*) as count FROM offer_clicks WHERE offer_id = ?", (offer_id_1,))
    count_row = await cursor.fetchone()
    assert count_row["count"] == 3

    stats_offer1 = await get_offer_clicks_stats(offer_id=offer_id_1, days=1)
    assert len(stats_offer1) == 1
    assert stats_offer1[0]["offer_id"] == offer_id_1
    assert stats_offer1[0]["click_count"] == 3
    assert stats_offer1[0]["title"] == OFFER_1_DATA["title"]

    await upsert_offer(Offer(**OFFER_2_DATA))
    cursor = await db_conn.execute("SELECT id FROM offers WHERE external_id = ?", (OFFER_2_DATA["external_id"],))
    offer_row_2 = await cursor.fetchone()
    offer_id_2 = offer_row_2["id"]
    
    await register_offer_click(offer_id=offer_id_2, user_agent="agent_other")

    all_stats = await get_offer_clicks_stats(days=1)
    assert len(all_stats) == 2
    assert all_stats[0]["offer_id"] == offer_id_1
    assert all_stats[0]["click_count"] == 3
    assert all_stats[1]["offer_id"] == offer_id_2
    assert all_stats[1]["click_count"] == 1
    
    stats_non_existent = await get_offer_clicks_stats(offer_id=999, days=1)
    assert len(stats_non_existent) == 0 