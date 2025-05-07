"""
Testes para os modelos e funções de banco de dados do BoraDeDesconto.
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


@pytest.fixture
async def setup_test_db():
    """
    Fixture para configurar um banco de teste temporário.
    """
    # Criar um banco de dados de teste
    test_db_path = Path(__file__).parent / "test_models.db"
    
    # Salva o path do banco original
    original_get_db_path = models.get_db_path
    
    # Sobrescreve a função get_db_path para retornar o caminho do banco de teste
    async def mock_get_db_path():
        return test_db_path
    
    models.get_db_path = mock_get_db_path
    
    # Inicializa o banco de teste
    await models.init_db()
    
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
async def test_offer_model():
    """
    Testa a criação de um modelo Offer.
    """
    offer = models.Offer(
        merchant="amazon",
        external_id="test123",
        title="Produto de Teste",
        url="https://example.com/test",
        price=99.99,
        discount_pct=20
    )
    
    assert offer.merchant == "amazon"
    assert offer.external_id == "test123"
    assert offer.title == "Produto de Teste"
    assert offer.url == "https://example.com/test"
    assert offer.price == 99.99
    assert offer.discount_pct == 20
    assert offer.ts is not None  # Deve ter um timestamp


@pytest.mark.asyncio
async def test_upsert_and_get_offer(setup_test_db):
    """
    Testa a inserção/atualização e recuperação de uma oferta.
    """
    # Cria e insere uma oferta
    offer = models.Offer(
        merchant="amazon",
        external_id="test123",
        title="Produto de Teste",
        url="https://example.com/test",
        price=99.99,
        discount_pct=20
    )
    
    await models.upsert_offer(offer)
    
    # Lista as ofertas
    offers = await models.get_offers()
    assert len(offers) == 1
    
    # Verifica se a oferta foi inserida corretamente
    db_offer = offers[0]
    assert db_offer["merchant"] == "amazon"
    assert db_offer["external_id"] == "test123"
    assert db_offer["title"] == "Produto de Teste"
    assert db_offer["price"] == 99.99
    assert db_offer["discount_pct"] == 20
    
    # Atualiza a oferta
    offer_id = db_offer["id"]
    updated_offer = models.Offer(
        merchant="amazon",
        external_id="test123",
        title="Produto de Teste Atualizado",
        url="https://example.com/test",
        price=89.99,
        discount_pct=30
    )
    
    await models.upsert_offer(updated_offer)
    
    # Verifica se a oferta foi atualizada
    offers = await models.get_offers()
    assert len(offers) == 1  # Não deve ter criado uma nova oferta
    
    db_offer = offers[0]
    assert db_offer["id"] == offer_id  # Deve manter o mesmo ID
    assert db_offer["title"] == "Produto de Teste Atualizado"
    assert db_offer["price"] == 89.99
    assert db_offer["discount_pct"] == 30
    
    # Testa a busca por ID
    offer_by_id = await models.get_offer_by_id(offer_id)
    assert offer_by_id is not None
    assert offer_by_id["id"] == offer_id
    assert offer_by_id["title"] == "Produto de Teste Atualizado"


@pytest.mark.asyncio
async def test_get_offers_with_filters(setup_test_db):
    """
    Testa a filtragem de ofertas.
    """
    # Insere múltiplas ofertas
    offers = [
        models.Offer(
            merchant="amazon",
            external_id="test1",
            title="Produto Amazon 1",
            url="https://example.com/test1",
            price=99.99,
            discount_pct=10
        ),
        models.Offer(
            merchant="amazon",
            external_id="test2",
            title="Produto Amazon 2",
            url="https://example.com/test2",
            price=199.99,
            discount_pct=20
        ),
        models.Offer(
            merchant="mercadolivre",
            external_id="test3",
            title="Produto Mercado Livre 1",
            url="https://example.com/test3",
            price=299.99,
            discount_pct=30
        )
    ]
    
    for offer in offers:
        await models.upsert_offer(offer)
    
    # Testa filtro por merchant
    amazon_offers = await models.get_offers(merchant="amazon")
    assert len(amazon_offers) == 2
    for offer in amazon_offers:
        assert offer["merchant"] == "amazon"
    
    # Testa filtro por desconto mínimo
    high_discount_offers = await models.get_offers(min_discount=20)
    assert len(high_discount_offers) == 2
    for offer in high_discount_offers:
        assert offer["discount_pct"] >= 20
    
    # Testa combinação de filtros
    filtered_offers = await models.get_offers(merchant="mercadolivre", min_discount=20)
    assert len(filtered_offers) == 1
    assert filtered_offers[0]["merchant"] == "mercadolivre"
    assert filtered_offers[0]["discount_pct"] >= 20
    
    # Testa paginação
    limited_offers = await models.get_offers(limit=1)
    assert len(limited_offers) == 1
    
    paged_offers = await models.get_offers(limit=1, offset=1)
    assert len(paged_offers) == 1
    assert paged_offers[0]["id"] != limited_offers[0]["id"]  # Deve ser diferente


@pytest.mark.asyncio
async def test_register_and_get_clicks(setup_test_db):
    """
    Testa o registro e a consulta de cliques.
    """
    # Insere uma oferta
    offer = models.Offer(
        merchant="amazon",
        external_id="test1",
        title="Produto de Teste",
        url="https://example.com/test",
        price=99.99,
        discount_pct=20
    )
    
    await models.upsert_offer(offer)
    
    # Obtém o ID da oferta inserida
    offers = await models.get_offers()
    offer_id = offers[0]["id"]
    
    # Registra alguns cliques
    for _ in range(3):
        await models.register_offer_click(
            offer_id=offer_id,
            user_agent="Test User Agent",
            referer="https://example.com/referer"
        )
    
    # Testa a obtenção de estatísticas
    stats = await models.get_offer_clicks_stats(offer_id=offer_id)
    
    assert len(stats) == 1
    assert stats[0]["offer_id"] == offer_id
    assert stats[0]["click_count"] == 3
    
    # Testa a obtenção de estatísticas gerais
    all_stats = await models.get_offer_clicks_stats()
    assert len(all_stats) >= 1  # Deve ter pelo menos nossa oferta 