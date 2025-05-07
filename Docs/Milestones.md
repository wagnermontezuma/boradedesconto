== Milestones

O cronograma de desenvolvimento foi dividido em entregas semanais com foco em MVP funcional e expansões iterativas.

[cols="1,4", options="header"]
| Semana | Entregas
| S1     | Setup de repositório, criação do schema SQLite, rota `GET /offers`, UI estática com dados mock.
| S2     | Scraper para Amazon via API, agendamento com APScheduler, UI dinâmica com filtros.
| S3     | Scraper para Mercado Livre (REST), rota `/go/{id}` com registro de cliques e integração com GA4.
| S3.5   | Criação do bot WhatsApp local com webhook de teste (modo echo).
| S4     | Integração com Mautic CRM, salvando leads via API com tags personalizadas.
| S4.5   | Classificador de intenção com LLM + integração com endpoint `/offers`.
| S5     | Notificações proativas via WhatsApp com base em *watch-jobs*.
