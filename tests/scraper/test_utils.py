"""
Testes para as funções utilitárias do scraper.
"""
import pytest
import sys
from pathlib import Path

# Adiciona o diretório parent ao path
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir))

# Import dos módulos do scraper
from scraper.utils import calculate_discount, format_price, get_random_headers


def test_calculate_discount():
    """
    Testa o cálculo de desconto.
    """
    # Casos normais
    assert calculate_discount(100.0, 80.0) == 20  # 20% de desconto
    assert calculate_discount(100.0, 50.0) == 50  # 50% de desconto
    assert calculate_discount(200.0, 100.0) == 50  # 50% de desconto
    
    # Casos extremos
    assert calculate_discount(100.0, 0.0) == 100  # 100% de desconto
    assert calculate_discount(100.0, 100.0) == 0  # 0% de desconto
    
    # Casos inválidos
    assert calculate_discount(0.0, 0.0) == 0  # Preço original zero
    assert calculate_discount(-100.0, -80.0) == 0  # Preços negativos
    assert calculate_discount(100.0, 110.0) == 0  # Preço atual maior que o original


def test_format_price():
    """
    Testa a formatação de preços.
    """
    # Preços bem formatados
    assert format_price("R$ 99,90") == 99.90
    assert format_price("R$ 1.299,90") == 1299.90
    assert format_price("R$ 1.299,00") == 1299.00
    
    # Preços sem símbolo da moeda
    assert format_price("99,90") == 99.90
    assert format_price("1.299,90") == 1299.90
    
    # Preços com formatos alternativos
    assert format_price("R$99,90") == 99.90
    assert format_price("99.90") == 99.90
    assert format_price("99") == 99.00
    
    # Casos especiais
    assert format_price("") == 0.0
    assert format_price("abc") == 0.0
    assert format_price("R$ -") == 0.0
    
    # Casos com múltiplos pontos
    assert format_price("1.234.567,89") == 1234567.89


def test_get_random_headers():
    """
    Testa a geração de headers aleatórios.
    """
    # Verifica se os headers são gerados
    headers = get_random_headers()
    assert headers is not None
    
    # Verifica se os campos obrigatórios estão presentes
    assert "User-Agent" in headers
    assert "Accept-Language" in headers
    assert "Accept" in headers
    
    # Verifica se o User-Agent é um dos da lista predefinida
    from scraper.utils import USER_AGENTS
    assert headers["User-Agent"] in USER_AGENTS
    
    # Verifica se o Accept-Language é um dos da lista predefinida
    from scraper.utils import ACCEPT_LANGUAGES
    assert headers["Accept-Language"] in ACCEPT_LANGUAGES
    
    # Verifica se duas chamadas geram headers diferentes
    # (probabilidade muito baixa de serem iguais)
    headers2 = get_random_headers()
    assert headers != headers2 

class TestScraperUtils:
    def test_format_price(self):
        assert format_price("R$ 1.234,56") == 1234.56
        assert format_price("1.234,56") == 1234.56
        assert format_price("1234.56") == 1234.56 # Ponto como separador decimal
        assert format_price("R$123,45") == 123.45
        assert format_price("R$ 123") == 123.0
        assert format_price("123") == 123.0
        assert format_price("Preço: 50,25") == 50.25
        assert format_price("Apenas 199.99 !") == 199.99
        assert format_price("Valor R$33,33 com taxas") == 33.33
        assert format_price("Gratuito") == 0.0 # Ou como for definido para gratuito
        assert format_price("Indisponível") == 0.0 # Ou como for definido
        assert format_price("") == 0.0
        assert format_price(None) == 0.0
        assert format_price("R$ 1.000,00") == 1000.00
        assert format_price("1,000.50") == 1000.50 # Milhar com vírgula, decimal com ponto

    def test_calculate_discount(self):
        assert calculate_discount(100.0, 80.0) == 20
        assert calculate_discount(200.0, 150.0) == 25
        assert calculate_discount(50.0, 50.0) == 0
        assert calculate_discount(100.0, 120.0) == 0 # Preço atual maior, sem desconto
        assert calculate_discount(100.0, 0.0) == 100 # Desconto total
        with pytest.raises(ValueError): # Preço original não pode ser zero ou negativo se o preço atual for positivo
            calculate_discount(0.0, 50.0)
        assert calculate_discount(0.0, 0.0) == 0 # Ambos zero, sem desconto
        assert calculate_discount(100, None) == 0 # Preço atual None
        assert calculate_discount(None, 50) == 0 # Preço original None
        assert calculate_discount(None, None) == 0 # Ambos None

    def test_get_random_headers(self):
        headers1 = get_random_headers()
        headers2 = get_random_headers()
        assert "User-Agent" in headers1
        assert "Accept-Language" in headers1
        # É estatisticamente improvável que dois UAs sejam iguais, mas não garantido
        # Apenas verifica se a função retorna um dict com as chaves esperadas
        assert len(headers1["User-Agent"]) > 0 