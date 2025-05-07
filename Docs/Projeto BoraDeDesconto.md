# Projeto **BoraDeDesconto** – Versão Bare‑Metal (Bazzite OS)

## 1. Visão Geral

Plataforma de agregação de ofertas em tempo quase‑real que coleta promoções de grandes e‑commerces (Amazon, Mercado Livre, AliExpress, Shopee e outros), armazena em banco SQLite e apresenta em landing page criada em Next.js. O MVP roda inteiramente no diretório do usuário, sem dependências de root ou Docker, facilitando testes em distros imutáveis como o Bazzite OS.

**Objetivos do MVP**

* Provar fluxo “coleta → API → UI” localmente.
* Facilitar migração futura para AWS (apenas trocar engines).
* Garantir instalação 100 % user‑space.

## 2. Arquitetura de Alto Nível

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
└────────────┘                            └──────────┘
```

## 3. Componentes & Tecnologias

| Camada        | Tecnologia                          | Observações                                               |
| ------------- | ----------------------------------- | --------------------------------------------------------- |
| **Scraper**   | Python 3.12, Playwright 1.44, httpx | Browsers headless instalados em `~/.cache/ms-playwright`. |
| **Agendador** | APScheduler 3.x                     | Mantém loop asyncio; persiste no systemd‑user.            |
| **Banco**     | SQLite 3 (WAL mode)                 | Arquivo `api/deals.db`; sem servidor externo.             |
| **API**       | FastAPI ± Uvicorn                   | Endpoints REST simples.                                   |
| **UI**        | Next.js 15, Tailwind CSS            | Grid responsivo, proxy para API via rewrite.              |
| **Gerência**  | systemd‑user services               | Sem privilégio root; reinício automático.                 |

## 4. Estrutura de Diretórios

```
boradedesconto/
├─ env/                  # venv Python
├─ scraper/
│  ├─ main.py            # lógica de scraping
│  ├─ scheduler.py       # APScheduler loop
│  └─ utils.py           # helpers HMAC, parsing
├─ api/
│  ├─ app.py             # FastAPI
│  ├─ models.py          # schema & init_db()
│  └─ deals.db           # (gerado)
└─ web/
   ├─ next.config.js
   ├─ package.json
   └─ src/
       ├─ pages/
       ├─ lib/useOffers.ts
       └─ components/OfferCard.tsx
```

## 5. Banco de Dados

```sql
CREATE TABLE offers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant TEXT NOT NULL,
    external_id TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    price REAL NOT NULL,
    discount_pct INTEGER NOT NULL,
    ts DATETIME NOT NULL,
    UNIQUE(merchant, external_id)
);
```

*Índices adicionais* podem ser criados em `discount_pct` e `ts` para consultas frequentes.

## 6. Scraper Detalhado

### 6.1 Fluxo

1. Recebe `job_context` (merchant, parâmetros).
2. Faz chamada via API oficial (quando existir) ou Playwright.
3. Converte resultado em dicionários conformes ao schema.
4. Upsert na tabela `offers`.

### 6.2 Boas‑práticas

* `async with semaphore(3)` para limitar concorrência.
* `retry` exponencial (`tenacity`) em 429 e timeouts.
* Rotacionar `User‑Agent` e `Accept‑Language`.
* Logar no `~/.local/share/deals‑hub/logs/scraper.log` (rotating 5×1 MB).

## 7. Scheduler (APScheduler)

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
sched = AsyncIOScheduler(timezone="UTC")
for merchant in ["amazon", "ml"]:
    sched.add_job(run_task, "interval", hours=1, args=[merchant], id=merchant)
```

* Jobs são salvos em memória; reinício limpa agenda → aceitável para MVP.

## 8. API Design

| Método | Rota           | Descrição                                                      |
| ------ | -------------- | -------------------------------------------------------------- |
| `GET`  | `/offers`      | Lista ofertas (`merchant`, `min_discount`, `limit`, `offset`). |
| `GET`  | `/offers/{id}` | Detalhe single offer.                                          |
| `GET`  | `/go/{id}`     | Registra clique e redireciona (`307`).                         |

*Middleware* de CORS liberando `http://localhost:3000`.

## 9. Front‑end

* **Grid Masonry**: `grid-cols-[repeat(auto-fit,minmax(220px,1fr))]`.
* **Componentes**: `OfferCard`, `FilterBar`, `Countdown` (próxima varredura).
* **SEO**: script JSON‑LD por card; meta OG para compartilhamento.
* **Analytics**: GA4 gtag; evento `click_offer` disparado no `/go/:id`.

## 10. Configuração de Ambiente

### Passo‑a‑passo

```bash
# clone
mkdir -p ~/Projects && cd ~/Projects
git clone git@github.com:usuario/boradedesconto.git
cd boradedesconto

# Python
python3.12 -m venv env
source env/bin/activate
pip install -r requirements.txt  # arquivo raiz consolida deps
playwright install chromium

# Node
nvm install 20
cd web && npm i && cd ..

# Inicializar banco
python - <<<'import asyncio,api.models as m;asyncio.run(m.init_db())'
```

### Systemd‑user Services

Arquivo gerado em `scripts/install-services.sh` adiciona e habilita **api** e **scraper**.

## 11. Desenvolvimento Local

| Serviço          | Comando                                    | Porta |
| ---------------- | ------------------------------------------ | ----- |
| Scraper (manual) | `python scraper/main.py`                   | —     |
| Scheduler        | `python scraper/scheduler.py`              | —     |
| API              | `uvicorn api.app:app --reload --port 8000` | 8000  |
| Frontend         | `npm run dev --workspace=web -p 3000`      | 3000  |

## 12. Testes

* **Pytest** para scraper (mock httpx / playwright).
* **Vitest** para hooks React.
* **Pre‑commit**: black, ruff, isort, prettier.

## 13. Roadmap (4 semanas)

| Semana | Entregas                                                                                           |
| ------ | -------------------------------------------------------------------------------------------------- |
| **S1** | Setup repositório, schema SQLite, endpoint `GET /offers`, UI grid estática com mock.               |
| **S2** | Scraper Amazon (API) + Scheduler, UI dinâmica + filtros.                                           |
| **S3** | Scraper Mercado Livre (REST), rota `/go/{id}`, registro de cliques e analytics.                    |
| **S4** | Integração AliExpress (Portals) ou fallback Playwright; publicar README completo e testes básicos. |

## 14. Migração Futura para AWS

| Local               | AWS              | Mudança                                               |
| ------------------- | ---------------- | ----------------------------------------------------- |
| SQLite              | RDS PostgreSQL   | Altera `DATABASE_URL`; roda Alembic migrations.       |
| systemd‑user        | ECS Fargate Task | Copia entrypoints (`uvicorn`, `scheduler`).           |
| Playwright browsers | Layer AWS Lambda | Padrão `playwright-aws-lambda` se migrar para Lambda. |

## 15. Segurança & Compliance

* `robots.txt` e `terms.md` esclarecendo uso de links afiliados.
* Limite de requisições a < 1 req/s por domínio.
* Variáveis sensíveis (chaves API) fora do git; armazenar em `~/.config/boradedesconto/.env`.

## 16. Integração WhatsApp + IA + CRM

| Bloco                  | Tecnologia sugerida                                                 | Função                                                                                            |
| ---------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Canal**              | **WhatsApp Business Cloud API** (Meta) **ou** Twilio WhatsApp       | Receber mensagens do usuário e enviar ofertas.                                                    |
| **Orquestração**       | Node.js micro‑serviço `wa-bot` (Express + Prisma)                   | Lida com webhook do WhatsApp, consulta LLM e CRM.                                                 |
| **Agente IA**          | OpenAI o3 ⚙️ (via OpenRouter)                                       | Entender intenção, buscar no catálogo (`/offers`) ou acionar busca específica.                    |
| **CRM**                | **Mautic** (self‑host, GPL) – opção mais leve; ou SuiteCRM/Odoo CRM | Armazena contatos, preferências (categoria favorita, limite de preço etc.), histórico de cliques. |
| **Mensageria interna** | Redis Streams (pub/sub)                                             | Comunicação entre bot, scraper e CRM para missões “buscar TV 55'' < R\$2.500”.                    |

### 16.1 Fluxo de On‑boarding

1. **Landing page** exibe CTA *“Entre no nosso grupo VIP de ofertas no WhatsApp”*.
2. Usuário clica → link universal `wa.me/<phone>?text=START`.
3. Bot detecta palavra‑chave **START** e pede duas informações rápidas:

   * **Categoria preferida** (Eletrônicos, Moda, Casa… — quick‑replies)
   * **Orçamento médio** (faixa de preço)
4. Bot chama endpoint `POST /crm/contacts` (Mautic API) → salva lead com tags.
5. Bot confirma: *“Perfeito! Sempre que surgir algo em Eletrônicos até R\$2.500 eu aviso aqui.”*

### 16.2 Personalização & Procuras Específicas

* Mensagens de usuário entram no webhook → agente IA classifica intenção:

  * **“Quero um iPhone 15 abaixo de 5k”** → chama `/offers?keyword=iphone+15&max_price=5000`.
  * Se não encontrar, agenda *watch‑job* (`redis.setex watch:userid:iphone15 43200 …`).
  * Quando o scraper inserir oferta que satisfaz, publisher envia WhatsApp proactive message.

### 16.3 Estrutura de Dados (CRM)

| Campo             | Descrição                                           |
| ----------------- | --------------------------------------------------- |
| `phone`           | Hash E.164 do contato.                              |
| `first_msg`       | Timestamp do opt‑in.                                |
| `prefs`           | JSON: `{ "cats": ["electronics"], "budget": 2500 }` |
| `last_offer_sent` | ID da última oferta entregue, para deduplicar.      |

### 16.4 Deploy local

* **Mautic** roda em `env/mautic/` via PHP‑FPM + SQLite (simples). Quando for AWS, migra para RDS MySQL.
* **wa-bot** é Node app com `npm run dev` na porta 9000; expõe tunnel (ngrok) para testes.
* Adicione serviço `deals-wa.service` no systemd‑user.

### 16.5 Métricas‑chave

| Métrica         | Como medir                                                   |
| --------------- | ------------------------------------------------------------ |
| **Opt‑in rate** | `# contatos no CRM / # cliques CTA`.                         |
| **Engajamento** | Média de respostas por usuário / semana (WhatsApp webhooks). |
| **Conversão**   | `# cliques afiliados gerados via bot`.                       |

## 17. Roadmap Ajustado

| Semana   | Entregas novas                                     |
| -------- | -------------------------------------------------- |
| **S3.5** | Bot WhatsApp local (webhook “echo”).               |
| **S4**   | Integração Mautic → salvar lead + tags.            |
| **S4.5** | IA classificador de intenção + pesquisa `/offers`. |
| **S5**   | Notificações proativas e *watch‑jobs*.             |

---

### Próximos Passos Imediatos

1. Criar número teste WhatsApp Cloud API e webhook ngrok.

2. Inicializar Mautic em `~/Projects/boradedesconto/mautic` (script de instalação).

3. Implementar bot Node básico respondendo *"START"*.

4. Conectar bot → Mautic API, criar lead.

5. Criar repositório Git e commitar este documento como `PROJECT.md`.

6. Consolidar `requirements.txt` global no root.

7. Implementar rota `/offers` e grid de UI com dados mock.

8. Configurar systemd‑user para API.

9. Evoluir scraper Amazon.

---

*Versão*: 2025‑05‑07
*Autor*: Bredi Tecnologia Digital / ChatGPT
