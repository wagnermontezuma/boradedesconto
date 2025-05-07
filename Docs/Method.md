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

Essa arquitetura valida o ciclo completo de coleta e entrega de ofertas localmente, com camadas bem definidas e comunicação padronizada (REST).

=== Banco de Dados

A estrutura é otimizada para escrita e leitura rápida de ofertas, com deduplicação baseada no par `merchant` e `external_id`.

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
