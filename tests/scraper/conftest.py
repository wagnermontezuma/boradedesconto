"""
Configurações para os testes do scraper.
"""
import pytest
import sys
import os
from pathlib import Path

# Adiciona o diretório parent ao path
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir))


@pytest.fixture(scope="session")
def setup_test_environment():
    """
    Configura o ambiente de teste para os testes do scraper.
    """
    # Salva diretório atual
    original_dir = os.getcwd()
    
    # Muda para o diretório raiz do projeto
    os.chdir(str(parent_dir))
    
    # Executa os testes
    yield
    
    # Volta para o diretório original ao finalizar
    os.chdir(original_dir)


@pytest.fixture
def sample_offer_data():
    """
    Retorna dados de exemplo para criação de ofertas.
    """
    return {
        "amazon": {
            "title": "Smartphone Galaxy S21",
            "price": 1999.90,
            "original_price": 2499.90,
            "url": "https://www.amazon.com.br/dp/B0ABCDEF12",
            "merchant": "Amazon",
            "external_id": "B0ABCDEF12",
            "discount": 20
        },
        "mercadolivre": {
            "title": "Notebook Dell Inspiron",
            "price": 3899.90,
            "original_price": 4599.90,
            "url": "https://www.mercadolivre.com.br/p/MLB12345678",
            "merchant": "Mercado Livre",
            "external_id": "MLB12345678",
            "discount": 15
        }
    } 