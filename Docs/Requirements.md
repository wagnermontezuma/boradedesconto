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
