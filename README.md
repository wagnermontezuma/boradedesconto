# BoraDeDesconto - Plataforma de Ofertas em Tempo Quase-Real

Agregador de ofertas de e-commerces que coleta promoções, armazena em SQLite e apresenta em interface Next.js. MVP 100% user-space, sem dependências de root ou Docker.

## Visão Geral

![Arquitetura](./docs/arquitetura.png)

```
┌────────────┐      APScheduler       ┌────────────┐
│  Scheduler │ ────────►────────────► │  Scraper   │
└────────────┘  dispara jobs (1h)     └─────┬──────┘
                                            │ escreve ofertas
                                            ▼
                                       ┌──────────┐
                                       │ SQLite   │
                                       └────┬─────┘
                                            │ lê
┌────────────┐      HTTP (localhost)        ▼
│  Next.js   │ ◄─────────────────────────┌──────────┐
│  Frontend  │         JSON              │ FastAPI  │
└────────────┘                           └──────────┘
```

## Componentes

- **Scraper**: Python 3.12, Playwright 1.44, httpx
- **Agendador**: APScheduler 3.x
- **Banco**: SQLite 3 (WAL mode)
- **API**: FastAPI + Uvicorn
- **UI**: Next.js 15, Tailwind CSS
- **Gerência**: systemd-user services

## Instalação

### Requisitos

- Python 3.12+
- Node.js 20+
- Ambiente Linux com systemd (Bazzite OS testado)

### Configuração

```bash
# Clone o repositório
git clone https://github.com/usuario/boradedesconto.git
cd boradedesconto

# Ambiente Python
python -m venv env
source env/bin/activate
pip install -r requirements.txt
playwright install chromium

# Node.js
cd web
npm install
cd ..

# Inicializa o banco
python -c "import asyncio; from api.models import init_db; asyncio.run(init_db())"
```

### Início manual (desenvolvimento)

```bash
# Terminal 1: API
source env/bin/activate
cd api
uvicorn app:app --reload --port 8000

# Terminal 2: Frontend
cd web
npm run dev

# Terminal 3: Scraper (execução única)
source env/bin/activate
cd scraper
python main.py
```

### Serviços (produção)

```bash
# Instala e habilita os serviços do systemd-user
./scripts/install-services.sh

# Inicia os serviços
systemctl --user start deals-api.service
systemctl --user start deals-scraper.service

# Verifica status
systemctl --user status deals-api.service
```

## Uso

- API: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Endpoints API

| Método | Rota           | Descrição                                             |
| ------ | -------------- | ----------------------------------------------------- |
| GET    | /offers        | Lista ofertas com filtros (merchant, min_discount...) |
| GET    | /offers/{id}   | Detalhe de uma oferta                                 |
| GET    | /go/{id}       | Registra clique e redireciona (307)                   |

## Desenvolvimento

### Estrutura de Diretórios

```
boradedesconto/
├── api/
│   ├── app.py           # FastAPI
│   ├── models.py        # SQLite + funções DB
│   └── deals.db         # Banco gerado
├── scraper/
│   ├── main.py          # Scraper principal
│   ├── scheduler.py     # APScheduler
│   └── utils.py         # Funções utilitárias
├── web/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── lib/
│   ├── next.config.js
│   └── package.json
├── scripts/
│   └── install-services.sh # Script de instalação
└── requirements.txt
```

## Licença

MIT 

## Testes Automatizados

O projeto inclui testes automatizados para garantir a qualidade e funcionamento correto das funcionalidades. Os testes estão organizados por módulo:

### Testes do Scraper

- **Tests de Utilitários** (`tests/scraper/test_utils.py`): Testa as funções utilitárias como cálculo de desconto, formatação de preços e geração de headers.

- **Testes de Modelos** (`tests/scraper/test_models.py`): Testa as classes de dados e funções de persistência do scraper.

- **Testes de Scrapers** (`tests/scraper/test_scrapers.py`): Testa as funções de extração de ofertas dos sites.

### Testes da API

- **Testes de Endpoints** (`tests/api/test_api.py`): Testa os endpoints da API, incluindo a funcionalidade de redirecionamento e estatísticas de cliques.

- **Testes de Modelos** (`tests/api/test_models.py`): Testa a camada de dados da API, incluindo funções de CRUD e estatísticas.

## Executando os Testes

Para executar todos os testes:

```bash
pytest
```

Para executar testes específicos:

```bash
# Executar testes do scraper
pytest tests/scraper/

# Executar testes da API
pytest tests/api/

# Executar um arquivo de teste específico
pytest tests/scraper/test_utils.py

# Executar um teste específico
pytest tests/scraper/test_utils.py::test_calculate_discount
```

Para executar os testes com saída detalhada:

```bash
pytest -xvs
``` 