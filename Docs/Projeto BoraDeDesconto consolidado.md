````asciidoc
= SPEC-001: BoraDeDesconto – Plataforma de Ofertas em Tempo Quase‑Real
:sectnums:
:toc:


== Background

A crescente demanda por plataformas que concentrem promoções e descontos em tempo quase‑real motivou o desenvolvimento do BoraDeDesconto. Seu objetivo inicial é validar um fluxo local completo — da coleta automatizada até a interface de usuário — sem depender de permissões elevadas ou containers, tornando o projeto compatível com sistemas imutáveis como o Bazzite OS. A arquitetura proposta facilita futura migração para ambientes em nuvem, como AWS, com mínimo acoplamento.

== Requirements

Os requisitos foram definidos com foco em validar localmente o fluxo completo do sistema e viabilizar futuras integrações. A priorização segue o modelo MoSCoW.

=== Must Have

* Coleta automatizada de ofertas de múltiplos e‑commerces (ex: Amazon, Mercado Livre).
* Armazenamento local em banco SQLite no modo WAL.
* API REST para acesso às ofertas com filtros por `merchant`, `discount_pct`, `limit`, `offset`.
* Interface web responsiva em Next.js com grid dinâmico.
* Instalação 100% user‑space sem uso de root ou Docker.
* Agendamento recorrente de scraping via APScheduler.
* Registro de cliques em ofertas com redirecionamento.
* Logging de scraping em disco local.

=== Should Have

* Integração com Mautic para CRM self-hosted.
* Canal WhatsApp para entrega de ofertas personalizadas.
* Classificador de intenção baseado em LLM (OpenAI).
* Sistema de *watch-jobs* para ofertas específicas.
* Analytics de cliques e engajamento (GA4, eventos customizados).

=== Could Have

* SEO avançado com metadados JSON‑LD e Open Graph.
* Fallback automático para scraping via navegador (Playwright) caso API falhe.
* Proxy inteligente via Next.js para chamadas à API.
* Sistema de métricas locais (Prometheus-style).

=== Won't Have (for now)

* Interface administrativa para edição manual de ofertas.
* Sistema de pagamentos ou monetização embutida.
* Suporte a múltiplos idiomas.

== Method

A plataforma BoraDeDesconto adota uma arquitetura modular, com separação clara entre scraping, persistência, API e UI. O sistema é pensado para ser executado localmente, mas com possibilidade de migração futura para nuvem (e.g., AWS).

=== Arquitetura Geral

[plantuml, architecture-diagram, svg]
----
@startuml
actor User

rectangle "Scheduler (APScheduler)" {
  component "scheduler.py" as SCHED
}

rectangle "Scraper (Playwright + httpx)" {
  component "main.py"
}

database "SQLite (WAL mode)" as DB

rectangle "API (FastAPI)" {
  component "app.py"
}

rectangle "Frontend (Next.js)" {
  component "UI"
}

User --> UI
UI --> API : HTTP GET /offers
API --> DB : SQL SELECT
SCHED --> main.py : agenda scraping 1h
main.py --> DB : INSERT/UPSERT ofertas
@enduml
----

=== Banco de Dados

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
````

Índices recomendados:

```sql
CREATE INDEX idx_discount ON offers(discount_pct);
CREATE INDEX idx_ts ON offers(ts DESC);
```

\=== Scraping e Agendamento

```python
async with semaphore(3):
    retry(..., wait=exponential):
        get_offers(merchant)
```

```python
sched.add_job(run_task, "interval", hours=1, args=[merchant])
```

\=== API (FastAPI)

\[cols="1,2,4", options="header"]
|===
\| Método | Rota           | Descrição
\| GET    | /offers        | Lista ofertas com filtros: `merchant`, `min_discount`, `limit`, `offset`.
\| GET    | /offers/{id}   | Detalhe de uma oferta.
\| GET    | /go/{id}       | Registra clique e redireciona com status 307.
|===

\=== Frontend (Next.js 15 + Tailwind)

* `OfferCard`, `FilterBar`, `Countdown`.
* Tailwind grid responsivo.
* JSON-LD + meta OG para SEO.
* Integração com GA4 via `gtag` + evento `click_offer`.

\=== Integração com WhatsApp + IA + CRM

## \[plantuml, wa-intent-flow, svg]

@startuml
actor User
participant "wa-bot (Node.js)" as Bot
participant "OpenAI o3" as AI
participant "FastAPI (/offers)" as API
participant "Mautic (CRM)" as CRM

User -> Bot : "Quero um iPhone 15 abaixo de 5k"
Bot -> AI : classificar intenção
AI -> Bot : busca por keyword+preço
Bot -> API : GET /offers?keyword=iphone15\&max\_price=5000
API --> Bot : resultados
alt se oferta encontrada
Bot -> User : envia link com oferta
else nenhuma oferta
Bot -> Redis : setex watch-job 12h
end
Bot -> CRM : log de busca
@enduml
-------

\[cols="1,3", options="header"]
|===
\| Campo           | Descrição
\| phone           | Hash E.164 do contato.
\| prefs           | JSON com categorias e orçamento.
\| first\_msg       | Timestamp do opt-in.
\| last\_offer\_sent | ID da última oferta enviada.
|===

\== Implementation

\=== Setup do Ambiente

## \[source,bash]

mkdir -p \~/Projects && cd \~/Projects
git clone [git@github.com](mailto:git@github.com)\:usuario/boradedesconto.git
cd boradedesconto
python3.12 -m venv env
source env/bin/activate
pip install -r requirements.txt
playwright install chromium
nvm install 20
cd web && npm install && cd ..
python - <<<'import asyncio,api.models as m;asyncio.run(m.init\_db())'
----------------------------------------------------------------------

\=== Serviços via systemd‑user

## \[source,bash]

## bash scripts/install-services.sh

Serviços:

* `deals-api.service`
* `deals-scraper.service`

\=== Execução Manual

\[cols="1,2,1", options="header"]
|===
\| Serviço     | Comando                                    | Porta
\| Scraper     | `python scraper/main.py`                   | —
\| Scheduler   | `python scraper/scheduler.py`              | —
\| API         | `uvicorn api.app:app --reload --port 8000` | 8000
\| Frontend    | `npm run dev --workspace=web -p 3000`      | 3000
|===

\=== Integrações

* Mautic: `env/mautic/` via PHP-FPM + SQLite.
* wa-bot: microserviço Node.js + tunnel (ngrok).
* Webhook: WhatsApp Cloud API apontando para localhost.

\== Milestones

\[cols="1,4", options="header"]
|===
\| Semana | Entregas
\| S1     | Setup de repositório, criação do schema SQLite, rota `GET /offers`, UI estática com dados mock.
\| S2     | Scraper para Amazon via API, agendamento com APScheduler, UI dinâmica com filtros.
\| S3     | Scraper para Mercado Livre (REST), rota `/go/{id}` com registro de cliques e integração com GA4.
\| S3.5   | Criação do bot WhatsApp local com webhook de teste (modo echo).
\| S4     | Integração com Mautic CRM, salvando leads via API com tags personalizadas.
\| S4.5   | Classificador de intenção com LLM + integração com endpoint `/offers`.
\| S5     | Notificações proativas via WhatsApp com base em *watch-jobs*.
|===

\== Gathering Results

\=== Validação dos Requisitos

\[cols="2,4", options="header"]
|===
\| Requisito                          | Método de Verificação
\| Coleta automatizada               | Verificar execução agendada e registros no banco.
\| API REST funcional                | Testes com `curl`/Postman e cobertura automatizada.
\| UI com dados reais                | Renderização dinâmica e testes de filtro.
\| Registro de cliques              | Eventos enviados para analytics e verificação de redirecionamento.
\| Execução 100% user-space         | Instalação sem root em Bazzite OS.
\| Integração com Mautic CRM        | Leads salvos com tags via API.
\| Entrega via WhatsApp             | Mensagens personalizadas recebidas e registradas.
\| Personalização com IA            | Intenções corretamente classificadas e resultados relevantes.
|===

\=== Métricas de Sucesso

\[cols="2,4", options="header"]
|===
\| Métrica               | Como medir
\| Opt-in Rate           | Total de contatos no CRM ÷ total de cliques no CTA do WhatsApp.
\| Engajamento           | Média de interações por usuário por semana via webhooks.
\| Conversão             | Cliques afiliados gerados a partir de ofertas enviadas pelo bot.
\| Latência scraping→UI  | Tempo entre coleta e exibição via frontend.
\| Cobertura de ofertas  | Número de e-commerces suportados e volume médio de itens por ciclo.
|===

```
