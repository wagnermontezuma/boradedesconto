"""
Testes para os modelos e funções de banco de dados do BoraDeDesconto.
"""
import pytest
import os
import sys
from pathlib import Path
import asyncio
from datetime import datetime
from pydantic import ValidationError

# Adiciona o diretório parent ao path
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir))

# Import dos módulos da API
from api import models

# Ajustar o PYTHONPATH para incluir o diretório raiz do projeto 'boradedesconto'
# Isso permite que 'from api.models import Offer, OfferClick' funcione
project_root = Path(__file__).resolve().parent.parent.parent # Sobe três níveis: tests/api -> tests -> boradedesconto -> raiz do projeto (onde está a pasta 'api')
sys.path.insert(0, str(project_root))

from api.models import Offer, OfferClick # Agora isso deve funcionar

# Dados de exemplo para testes
VALID_OFFER_DATA = {
    "merchant": "amazon",
    "external_id": "B08X7JX9MB",
    "title": "Smartphone Samsung Galaxy A54",
    "url": "https://www.amazon.com.br/dp/B08X7JX9MB",
    "price": 1899.99,
    "discount_pct": 25,
}

VALID_OFFER_CLICK_DATA = {
    "offer_id": 1,
    "user_agent": "test-agent",
    "referer": "test-referer",
}

class TestOfferModel:
    def test_create_valid_offer(self):
        offer = Offer(**VALID_OFFER_DATA)
        assert offer.merchant == VALID_OFFER_DATA["merchant"]
        assert offer.external_id == VALID_OFFER_DATA["external_id"]
        assert offer.title == VALID_OFFER_DATA["title"]
        assert offer.url == VALID_OFFER_DATA["url"]
        assert offer.price == VALID_OFFER_DATA["price"]
        assert offer.discount_pct == VALID_OFFER_DATA["discount_pct"]
        assert offer.id is None  # ID é gerado pelo banco, não no modelo Pydantic inicialmente
        assert isinstance(offer.ts, datetime)

    def test_offer_missing_required_fields(self):
        incomplete_data = VALID_OFFER_DATA.copy()
        del incomplete_data["title"] # 'title' é obrigatório
        with pytest.raises(ValidationError):
            Offer(**incomplete_data)

    def test_offer_invalid_price_type(self):
        invalid_data = VALID_OFFER_DATA.copy()
        invalid_data["price"] = "not_a_float"
        with pytest.raises(ValidationError):
            Offer(**invalid_data)

    def test_offer_invalid_discount_type(self):
        invalid_data = VALID_OFFER_DATA.copy()
        invalid_data["discount_pct"] = "not_an_int"
        with pytest.raises(ValidationError):
            Offer(**invalid_data)

    def test_offer_discount_out_of_bounds(self):
        # Supondo que discount_pct deva estar entre 0-100,
        # mas o modelo Pydantic não tem essa validação explícita.
        # Este teste passaria, a menos que adicionemos validação no modelo.
        # Por agora, vamos testar a criação com valores extremos.
        data_low = VALID_OFFER_DATA.copy()
        data_low["discount_pct"] = -10
        offer_low = Offer(**data_low)
        assert offer_low.discount_pct == -10

        data_high = VALID_OFFER_DATA.copy()
        data_high["discount_pct"] = 110
        offer_high = Offer(**data_high)
        assert offer_high.discount_pct == 110


class TestOfferClickModel:
    def test_create_valid_offer_click(self):
        click = OfferClick(**VALID_OFFER_CLICK_DATA)
        assert click.offer_id == VALID_OFFER_CLICK_DATA["offer_id"]
        assert click.user_agent == VALID_OFFER_CLICK_DATA["user_agent"]
        assert click.referer == VALID_OFFER_CLICK_DATA["referer"]
        assert click.id is None # ID é gerado pelo banco
        assert isinstance(click.ts, datetime)

    def test_offer_click_minimal_valid(self):
        # Somente offer_id é estritamente obrigatório na definição do modelo
        click = OfferClick(offer_id=1)
        assert click.offer_id == 1
        assert click.user_agent is None
        assert click.referer is None
        assert isinstance(click.ts, datetime)


    def test_offer_click_missing_offer_id(self):
        with pytest.raises(ValidationError):
            OfferClick(user_agent="some-agent") # offer_id faltando

    def test_offer_click_invalid_offer_id_type(self):
        with pytest.raises(ValidationError):
            OfferClick(offer_id="not_an_int")


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