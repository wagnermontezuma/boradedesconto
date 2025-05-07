"""
Testes para os modelos do scraper.
"""
import pytest
import sys
import json
import os
from datetime import datetime
from pathlib import Path

# Adiciona o diretório parent ao path
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir))

# Importa os módulos do scraper
from scraper.models import Offer, save_offers


@pytest.fixture
def temp_output_dir(tmp_path):
    """
    Cria um diretório temporário para salvar as ofertas.
    """
    output_dir = tmp_path / "offers"
    output_dir.mkdir()
    return output_dir


def test_offer_model():
    """
    Testa a criação e funcionamento do modelo Offer.
    """
    # Criação básica de uma oferta
    offer = Offer(
        title="Produto de Teste",
        price=99.90,
        original_price=149.90,
        url="https://example.com/produto",
        merchant="Loja Teste",
        external_id="TEST123",
        discount_pct=33
    )
    
    # Verifica se todos os campos foram definidos corretamente
    assert offer.title == "Produto de Teste"
    assert offer.price == 99.90
    assert offer.original_price == 149.90
    assert offer.url == "https://example.com/produto"
    assert offer.merchant == "Loja Teste"
    assert offer.external_id == "TEST123"
    assert offer.discount_pct == 33
    
    # Verifica se o timestamp foi gerado
    assert offer.timestamp is not None
    assert isinstance(offer.timestamp, str)
    
    # Verifica se a conversão para dicionário funciona
    offer_dict = offer.to_dict()
    assert isinstance(offer_dict, dict)
    assert offer_dict["title"] == "Produto de Teste"
    assert offer_dict["price"] == 99.90
    assert offer_dict["merchant"] == "Loja Teste"
    
    # Verifica se a conversão para JSON funciona
    offer_json = offer.to_json()
    assert isinstance(offer_json, str)
    
    # Verifica se é possível converter o JSON de volta para um dicionário
    parsed_json = json.loads(offer_json)
    assert parsed_json["title"] == "Produto de Teste"
    assert parsed_json["external_id"] == "TEST123"


def test_offer_equality():
    """
    Testa a igualdade entre ofertas.
    """
    offer1 = Offer(
        title="Produto de Teste",
        price=99.90,
        original_price=149.90,
        url="https://example.com/produto",
        merchant="Loja Teste",
        external_id="TEST123",
        discount_pct=33
    )
    
    offer2 = Offer(
        title="Produto de Teste",
        price=99.90,
        original_price=149.90,
        url="https://example.com/produto",
        merchant="Loja Teste",
        external_id="TEST123",
        discount_pct=33
    )
    
    offer3 = Offer(
        title="Outro Produto",
        price=79.90,
        original_price=129.90,
        url="https://example.com/outro-produto",
        merchant="Loja Teste",
        external_id="TEST456",
        discount_pct=38
    )
    
    # Verificações de igualdade
    assert offer1 == offer2
    assert offer1 != offer3
    assert offer2 != offer3


def test_save_offers(temp_output_dir):
    """
    Testa a função para salvar ofertas em um arquivo.
    """
    # Cria ofertas para o teste
    offers = [
        Offer(
            title="Produto 1",
            price=99.90,
            original_price=149.90,
            url="https://example.com/produto1",
            merchant="Amazon",
            external_id="TEST1",
            discount_pct=33
        ),
        Offer(
            title="Produto 2",
            price=199.90,
            original_price=249.90,
            url="https://example.com/produto2",
            merchant="Mercado Livre",
            external_id="TEST2",
            discount_pct=20
        )
    ]
    
    # Define o nome do arquivo e salva as ofertas
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"amazon_{timestamp}.json"
    output_path = temp_output_dir / filename
    
    # Testa a função save_offers com o diretório temporário
    save_offers(offers, "amazon", str(temp_output_dir))
    
    # Verifica se pelo menos um arquivo foi criado
    assert len(list(temp_output_dir.iterdir())) > 0
    
    # Verifica se os arquivos são JSONs válidos
    for file_path in temp_output_dir.iterdir():
        assert file_path.suffix == ".json"
        
        # Tenta carregar o arquivo JSON
        with open(file_path, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
            
            # Verifica se há ofertas no arquivo
            assert isinstance(saved_data, list)
            assert len(saved_data) == len(offers)
            
            # Verifica se as ofertas têm os campos corretos
            for offer_data in saved_data:
                assert "title" in offer_data
                assert "price" in offer_data
                assert "url" in offer_data
                assert "merchant" in offer_data
                
                # Verifica o merchant conforme o filtro
                if "amazon" in file_path.name.lower():
                    assert "Amazon" in [o["merchant"] for o in saved_data]
                elif "mercadolivre" in file_path.name.lower():
                    assert "Mercado Livre" in [o["merchant"] for o in saved_data] 