import pytest
import pytest_asyncio
from pathlib import Path
import sys
import os
from datetime import datetime
import asyncio # Adicionado para uso potencial em outras fixtures/testes

# Ajustar o PYTHONPATH
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

import aiosqlite
# Importar as funções de models que serão usadas pela API e precisam do DB mockado
from api.models import init_db # Necessário para inicializar o schema

# Usar um banco de dados em memória para testes
TEST_DB_PATH_API = ":memory:" # Nome diferente para evitar conflito se test_db_operations for rodado junto com escopo diferente

@pytest_asyncio.fixture(scope="function") # function scope para garantir isolamento entre testes de endpoint
async def test_db_session(): # Nome da fixture alterado para clareza
    original_get_db_path = None
    
    async def mock_get_db_path_for_api():
        return TEST_DB_PATH_API

    import api.models as api_models_module
    if hasattr(api_models_module, 'get_db_path'):
        original_get_db_path = api_models_module.get_db_path
    api_models_module.get_db_path = mock_get_db_path_for_api

    # Inicializa o esquema no banco em memória/teste
    # init_db é do módulo api.models, que agora usa mock_get_db_path_for_api
    await init_db() 
    
    # A fixture não precisa mais retornar uma conexão direta,
    # pois os endpoints da API usarão o DB mockado internamente.
    # Mas pode ser útil para setup/asserts diretos se necessário.
    conn = await aiosqlite.connect(TEST_DB_PATH_API)
    conn.row_factory = aiosqlite.Row
    
    yield conn # Pode ser usado para popular dados antes de chamar endpoints

    await conn.close()
    if TEST_DB_PATH_API != ":memory:" and Path(TEST_DB_PATH_API).exists():
        os.remove(TEST_DB_PATH_API)
    
    if original_get_db_path:
        api_models_module.get_db_path = original_get_db_path

# Fixture para o TestClient da API
from fastapi.testclient import TestClient
from api.app import app as fastapi_app # Importa a instância da app FastAPI

@pytest.fixture(scope="function")
def client(test_db_session): # Depende do test_db_session para garantir que o DB está mockado
    # O test_db_session já fez o patch de api.models.get_db_path
    # e inicializou o schema com init_db()
    # Agora o TestClient pode ser criado e usará o banco de dados mockado
    # porque a instância 'fastapi_app' importada usará o 'api.models' já mockado.
    
    # É importante que o evento startup da app FastAPI seja executado
    # para que o init_db() dentro dele use o banco mockado.
    # TestClient cuida de rodar os eventos de startup/shutdown.
    
    with TestClient(fastapi_app) as c:
        yield c 