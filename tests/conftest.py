"""
Configuração global para testes de pytest.
"""
import pytest
import os
import sys
from pathlib import Path

# Adiciona o diretório principal ao path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

# Configura pytest para não capturar a saída
def pytest_addoption(parser):
    parser.addoption(
        "--no-print-capture",
        action="store_true",
        default=False,
        help="Não captura a saída padrão durante os testes"
    )

@pytest.fixture(scope="session", autouse=True)
def no_print_capture(request):
    if request.config.getoption("--no-print-capture"):
        os.environ["PYTHONUNBUFFERED"] = "1"

# Desativa avisos de deprecação de asyncio por padrão
def pytest_configure(config):
    config.add_ini_value_line = lambda name, line: None
    pytest.register_assert_rewrite('tests') 