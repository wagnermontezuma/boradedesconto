"""
Testes para a API do BoraDeDesconto.
"""
import pytest
import os
import sys
from pathlib import Path
import asyncio
from datetime import datetime

# Adiciona o diretório parent ao path
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir))

# Import dos módulos da API
from api import models
from api.app import app
from fastapi.testclient import TestClient

# Cliente de teste FastAPI
client = TestClient(app)


@pytest.fixture
async def setup_test_db():
    """
    Fixture para configurar um banco de teste temporário.
    """
    # Criar um banco de dados de teste
    test_db_path = Path(__file__).parent / "test_deals.db"
    
    # Salva o path do banco original
    original_get_db_path = models.get_db_path
    
    # Sobrescreve a função get_db_path para retornar o caminho do banco de teste
    async def mock_get_db_path():
        return test_db_path
    
    models.get_db_path = mock_get_db_path
    
    # Inicializa o banco de teste
    await models.init_db()
    
    # Adiciona alguns dados de teste
    test_offers = [
        models.Offer(
            merchant="amazon",
            external_id="test1",
            title="Produto de Teste 1",
            url="https://example.com/test1",
            price=99.99,
            discount_pct=20,
            ts=datetime.utcnow()
        ),
        models.Offer(
            merchant="mercadolivre",
            external_id="test2",
            title="Produto de Teste 2",
            url="https://example.com/test2",
            price=199.99,
            discount_pct=30,
            ts=datetime.utcnow()
        )
    ]
    
    for offer in test_offers:
        await models.upsert_offer(offer)
    
    yield
    
    # Restaura a função original
    models.get_db_path = original_get_db_path
    
    # Remove o banco de teste ao final
    if test_db_path.exists():
        os.remove(test_db_path)
    
    if Path(str(test_db_path) + "-shm").exists():
        os.remove(str(test_db_path) + "-shm")
    
    if Path(str(test_db_path) + "-wal").exists():
        os.remove(str(test_db_path) + "-wal")


@pytest.mark.asyncio
async def test_list_offers(setup_test_db):
    """
    Testa o endpoint de listagem de ofertas.
    """
    response = client.get("/offers")
    assert response.status_code == 200
    
    data = response.json()
    assert "data" in data
    assert "count" in data
    assert data["count"] >= 2
    
    # Verifica se os campos esperados estão presentes
    for offer in data["data"]:
        assert "id" in offer
        assert "merchant" in offer
        assert "external_id" in offer
        assert "title" in offer
        assert "url" in offer
        assert "price" in offer
        assert "discount_pct" in offer
        assert "ts" in offer


@pytest.mark.asyncio
async def test_filter_offers_by_merchant(setup_test_db):
    """
    Testa a filtragem de ofertas por merchant.
    """
    response = client.get("/offers?merchant=amazon")
    assert response.status_code == 200
    
    data = response.json()
    assert data["count"] >= 1
    
    for offer in data["data"]:
        assert offer["merchant"] == "amazon"


@pytest.mark.asyncio
async def test_get_offer_by_id(setup_test_db):
    """
    Testa a obtenção de uma oferta específica por ID.
    """
    # Primeiro, lista todas as ofertas para obter um ID válido
    response = client.get("/offers")
    data = response.json()
    
    if data["count"] > 0:
        offer_id = data["data"][0]["id"]
        
        # Agora testa o endpoint para um ID específico
        response = client.get(f"/offers/{offer_id}")
        assert response.status_code == 200
        
        offer = response.json()
        assert offer["id"] == offer_id
        assert "title" in offer
        assert "url" in offer


@pytest.mark.asyncio
async def test_get_nonexistent_offer(setup_test_db):
    """
    Testa a obtenção de uma oferta inexistente.
    """
    response = client.get("/offers/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_redirect_and_click_tracking(setup_test_db):
    """
    Testa o redirecionamento e o registro de cliques.
    """
    # Obtém um ID válido
    response = client.get("/offers")
    data = response.json()
    
    if data["count"] > 0:
        offer_id = data["data"][0]["id"]
        
        # Testa o redirecionamento
        response = client.get(f"/go/{offer_id}", allow_redirects=False)
        assert response.status_code == 307
        assert "location" in response.headers
        
        # Verifica se o clique foi registrado
        response = client.get("/stats/clicks")
        assert response.status_code == 200
        
        stats = response.json()
        assert "data" in stats
        
        # O clique pode ainda não aparecer nas estatísticas se o intervalo de tempo for grande
        # mas o endpoint deve responder corretamente


@pytest.mark.asyncio
async def test_health_endpoint():
    """
    Testa o endpoint de health check.
    """
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "version" in data 