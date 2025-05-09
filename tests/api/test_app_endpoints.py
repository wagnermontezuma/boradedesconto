import pytest
from fastapi.testclient import TestClient # Embora o client venha da fixture, é bom para tipagem
from datetime import datetime, timedelta
import asyncio # Necessário para o teste de stats

# Ajustar o PYTHONPATH (se conftest não for suficiente ou para clareza)
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from api.models import Offer as ApiOfferModel # Para criar objetos Offer para popular o DB
from api.models import upsert_offer # Para popular o DB diretamente através da camada de modelo

# A fixture 'client' e 'test_db_session' são injetadas automaticamente a partir de conftest.py

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "ok"
    assert "version" in json_response

@pytest.mark.asyncio # Marcar o teste como assíncrono se ele usar 'await' diretamente
async def test_list_offers_empty(client: TestClient, test_db_session): # test_db_session garante DB limpo
    response = client.get("/offers")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["data"] == []
    assert json_response["count"] == 0

@pytest.mark.asyncio
async def test_list_offers_with_data(client: TestClient, test_db_session): # test_db_session garante DB mockado
    # Popular o banco de dados de teste usando a função upsert_offer (que usa o DB mockado)
    offer_data1 = {
        "merchant": "amazon", "external_id": "amz001", "title": "Amazon Offer 1",
        "url": "http://amazon.com/amz001", "price": 10.0, "discount_pct": 10,
        "ts": datetime.utcnow() - timedelta(hours=2)
    }
    offer_data2 = {
        "merchant": "mercado", "external_id": "mrc001", "title": "Mercado Offer 1",
        "url": "http://mercado.com/mrc001", "price": 20.0, "discount_pct": 20,
        "ts": datetime.utcnow() - timedelta(hours=1) # Mais recente
    }
    await upsert_offer(ApiOfferModel(**offer_data1))
    await upsert_offer(ApiOfferModel(**offer_data2))

    response = client.get("/offers")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["count"] == 2
    assert len(json_response["data"]) == 2
    # Verificar a ordem (mais recente primeiro)
    assert json_response["data"][0]["external_id"] == "mrc001"
    assert json_response["data"][1]["external_id"] == "amz001"

@pytest.mark.asyncio
async def test_get_single_offer_not_found(client: TestClient, test_db_session):
    response = client.get("/offers/999") # ID inexistente
    assert response.status_code == 404
    assert response.json()["detail"] == "Oferta não encontrada"

@pytest.mark.asyncio
async def test_get_single_offer_found(client: TestClient, test_db_session):
    offer_data = {
        "merchant": "amazon", "external_id": "amz002", "title": "Single Amazon Offer",
        "url": "http://amazon.com/amz002", "price": 15.0, "discount_pct": 5,
        "ts": datetime.utcnow()
    }
    await upsert_offer(ApiOfferModel(**offer_data))
    
    # Precisamos do ID real. Vamos buscar diretamente no DB mockado pela fixture test_db_session
    # A fixture test_db_session retorna uma conexão `conn`
    async with test_db_session as conn: # Usar a conexão retornada pela fixture
      cursor = await conn.execute("SELECT id FROM offers WHERE external_id = 'amz002'")
      row = await cursor.fetchone()
      assert row is not None
      offer_id = row["id"]

    response = client.get(f"/offers/{offer_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["external_id"] == "amz002"
    assert json_response["title"] == "Single Amazon Offer"
    assert json_response["id"] == offer_id


# Testes para filtros no endpoint /offers
@pytest.mark.asyncio
async def test_list_offers_with_filters(client: TestClient, test_db_session):
    await upsert_offer(ApiOfferModel(merchant="amazon", external_id="f1", title="Filter Offer A1", url="u", price=10, discount_pct=10, ts=datetime.utcnow()))
    await upsert_offer(ApiOfferModel(merchant="outra", external_id="f2", title="Filter Offer B1", url="u", price=20, discount_pct=20, ts=datetime.utcnow()))
    await upsert_offer(ApiOfferModel(merchant="amazon", external_id="f3", title="Filter Offer A2 High Discount", url="u", price=30, discount_pct=50, ts=datetime.utcnow()))

    # Filtro por merchant
    response_merchant = client.get("/offers?merchant=amazon")
    assert response_merchant.status_code == 200
    data_merchant = response_merchant.json()
    assert data_merchant["count"] == 2
    assert all(o["merchant"] == "amazon" for o in data_merchant["data"])

    # Filtro por min_discount
    response_discount = client.get("/offers?min_discount=30")
    assert response_discount.status_code == 200
    data_discount = response_discount.json()
    assert data_discount["count"] == 1
    assert data_discount["data"][0]["external_id"] == "f3" # Apenas a de 50%

    # Filtro combinado
    response_combo = client.get("/offers?merchant=amazon&min_discount=40")
    assert response_combo.status_code == 200
    data_combo = response_combo.json()
    assert data_combo["count"] == 1
    assert data_combo["data"][0]["external_id"] == "f3"

@pytest.mark.asyncio
async def test_redirect_offer_and_register_click(client: TestClient, test_db_session):
    offer_data = {
        "merchant": "redirect_test", "external_id": "redir001", "title": "Redirect Offer",
        "url": "http://example.com/redirect_target", "price": 5.0, "discount_pct": 5,
        "ts": datetime.utcnow()
    }
    await upsert_offer(ApiOfferModel(**offer_data))

    offer_id = -1
    async with test_db_session as conn:
        cursor = await conn.execute("SELECT id FROM offers WHERE external_id = 'redir001'")
        row = await cursor.fetchone()
        assert row is not None
        offer_id = row["id"]

    response = client.get(f"/go/{offer_id}", allow_redirects=False)
    assert response.status_code == 307
    
    expected_redirect_url = offer_data["url"]
    if "amazon.com.br" in expected_redirect_url and "tag=" not in expected_redirect_url:
         separator = "&" if "?" in expected_redirect_url else "?"
         expected_redirect_url = f"{expected_redirect_url}{separator}tag=wagnermontezu-20"
    
    assert response.headers["location"] == expected_redirect_url

    async with test_db_session as conn:
        cursor = await conn.execute("SELECT COUNT(*) as count FROM offer_clicks WHERE offer_id = ?", (offer_id,))
        click_count_row = await cursor.fetchone()
        assert click_count_row is not None
        assert click_count_row["count"] == 1

@pytest.mark.asyncio
async def test_redirect_offer_not_found(client: TestClient, test_db_session):
    response = client.get("/go/998", allow_redirects=False)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_click_stats(client: TestClient, test_db_session):
    offer1_data = {"merchant": "stats", "external_id": "s001", "title": "Stats Offer 1", "url": "u1", "price": 1, "discount_pct": 1, "ts": datetime.utcnow() - timedelta(days=2)}
    offer2_data = {"merchant": "stats", "external_id": "s002", "title": "Stats Offer 2", "url": "u2", "price": 2, "discount_pct": 2, "ts": datetime.utcnow() - timedelta(days=1)}
    
    await upsert_offer(ApiOfferModel(**offer1_data))
    await upsert_offer(ApiOfferModel(**offer2_data))

    id_s001, id_s002 = -1, -1
    async with test_db_session as conn:
        cur1 = await conn.execute("SELECT id FROM offers WHERE external_id = 's001'")
        r1 = await cur1.fetchone()
        id_s001 = r1["id"]
        cur2 = await conn.execute("SELECT id FROM offers WHERE external_id = 's002'")
        r2 = await cur2.fetchone()
        id_s002 = r2["id"]

    from api.models import register_offer_click 
    await register_offer_click(offer_id=id_s001, user_agent="test")
    await asyncio.sleep(0.01)
    await register_offer_click(offer_id=id_s001, user_agent="test")
    await asyncio.sleep(0.01)
    await register_offer_click(offer_id=id_s002, user_agent="test")

    response_all = client.get("/stats/clicks")
    assert response_all.status_code == 200
    data_all = response_all.json()["data"]
    assert len(data_all) == 2
    assert data_all[0]["offer_id"] == id_s001
    assert data_all[0]["click_count"] == 2
    assert data_all[1]["offer_id"] == id_s002
    assert data_all[1]["click_count"] == 1

    response_s001 = client.get(f"/stats/clicks?offer_id={id_s001}")
    assert response_s001.status_code == 200
    data_s001 = response_s001.json()["data"]
    assert len(data_s001) == 1
    assert data_s001[0]["offer_id"] == id_s001
    assert data_s001[0]["click_count"] == 2

    response_days = client.get(f"/stats/clicks?days=1")
    assert response_days.status_code == 200
    data_days = response_days.json()["data"]
    assert len(data_days) == 2

    offer3_data = {"merchant": "stats", "external_id": "s003", "title": "Stats Offer 3 No Clicks", "url": "u3", "price": 3, "discount_pct": 3, "ts": datetime.utcnow()}
    await upsert_offer(ApiOfferModel(**offer3_data))
    id_s003 = -1
    async with test_db_session as conn:
        cur3 = await conn.execute("SELECT id FROM offers WHERE external_id = 's003'")
        r3 = await cur3.fetchone()
        id_s003 = r3["id"]
    
    response_s003 = client.get(f"/stats/clicks?offer_id={id_s003}")
    assert response_s003.status_code == 200
    data_s003 = response_s003.json()["data"]
    assert len(data_s003) == 0 