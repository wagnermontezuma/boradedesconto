# systemPatterns.md

## Arquitetura do Sistema
- Modular, separando scraper, API, banco e UI.
- Comunicação via HTTP local (API REST) e banco SQLite.
- Agendamento de scraping com APScheduler (asyncio).
- Scraper utiliza Playwright (headless) e httpx para coleta.
- Banco SQLite em modo WAL para concorrência e performance.
- API FastAPI expõe endpoints REST para frontend e integrações.
- Frontend Next.js consome API via proxy/rewrite.
- Serviços gerenciados por systemd-user (sem root).

## Decisões Técnicas
- 100% user-space, sem root/Docker.
- Logging local com rotação.
- Filtros e paginação na API.
- Fallback para scraping via navegador se API oficial falhar.
- Integração futura com CRM, WhatsApp e IA via microserviços.

## Padrões de Design
- Separação clara de responsabilidades (scraper, API, UI, agendador).
- Uso de semáforo para limitar concorrência no scraping.
- Retry exponencial em falhas de scraping.
- Rotação de User-Agent e Accept-Language.
- Middleware CORS liberando frontend local.

## Relação entre Componentes
- Scheduler dispara jobs para o scraper.
- Scraper coleta e faz upsert no banco.
- API lê do banco e serve para UI e integrações.
- UI consome API e exibe ofertas em grid responsivo.
- Integrações futuras (WhatsApp, CRM, IA) consomem API e publicam eventos. 