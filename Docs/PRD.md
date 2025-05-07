# PRD: BoraDeDesconto – Plataforma de Ofertas em Tempo Quase-Real

## Contexto

Com o aumento da busca por promoções personalizadas em e-commerces, o projeto BoraDeDesconto visa oferecer uma plataforma eficiente para coleta, exibição e entrega de ofertas em tempo quase-real, com foco em ambientes locais sem permissão de root. O projeto também prepara caminho para futura migração para nuvem, mantendo arquitetura modular e pouco acoplada.

## Visão Geral

O MVP do BoraDeDesconto deve rodar 100% em user-space (sem Docker, root ou system-wide services), integrando:

* Scraper automatizado com agendamento via APScheduler
* Armazenamento local em SQLite (modo WAL)
* API REST com FastAPI
* UI responsiva em Next.js
* Integrações futuras: WhatsApp, CRM (Mautic), LLM (OpenAI)

## Objetivos

1. Validar o fluxo local completo: Scraper → DB → API → UI
2. Rodar em sistemas imutáveis (e.g., Bazzite OS)
3. Suportar integrações com CRM, mensageria e IA
4. Preparar terreno para cloud (AWS, RDS, Lambda)

## Requisitos

### Essenciais (Must Have)

* Coleta automatizada de ofertas (Amazon, Mercado Livre)
* API REST: `/offers`, `/offers/{id}`, `/go/{id}`
* Interface responsiva com grid dinâmico e filtros
* Instalação user-space total
* Logging local
* Registro de cliques e redirecionamento

### Suporte (Should Have)

* Integração com Mautic (CRM)
* Canal WhatsApp com bot e entrega personalizada
* Classificação de intenções com IA (OpenAI)
* Watch-jobs para desejos específicos
* Eventos customizados de analytics

### Desejáveis (Could Have)

* SEO com JSON-LD + OG
* Scraping via navegador (Playwright fallback)
* Proxy via Next.js
* Métricas locais estilo Prometheus

### Fora de Escopo (Won't Have)

* Interface administrativa
* Pagamentos embutidos
* Suporte a múltiplos idiomas

## Arquitetura

Modular, separando scraper, API, banco, UI. Executa localmente com possibilidade de migração para cloud.

```
User → Next.js UI → FastAPI → SQLite
                    → APScheduler → Scraper (Playwright/httpx)
```

## Banco de Dados

Tabela `offers` com campos: id, merchant, external\_id, title, url, price, discount\_pct, ts

Indexes: `discount_pct`, `ts DESC`

## Roadmap

| Semana | Entregas                                              |
| ------ | ----------------------------------------------------- |
| S1     | Repositório, schema SQLite, GET /offers, UI estática  |
| S2     | Scraper Amazon, agendador APScheduler, UI com filtros |
| S3     | Scraper Mercado Livre, registro de cliques, GA4       |
| S3.5   | Bot WhatsApp local (modo echo)                        |
| S4     | Integração Mautic, CRM com tags                       |
| S4.5   | Classificação IA + busca integrada                    |
| S5     | Notificações via WhatsApp com watch-jobs              |

## Dependências

* Python 3.12, Node 20
* SQLite, Playwright, FastAPI, APScheduler
* Next.js, Tailwind
* Mautic, ngrok, Redis (watch-jobs)

## Riscos

* Bloqueios de scraping por CAPTCHAs ou limites
* Instabilidades do WhatsApp Cloud API
* Desatualização de catálogos por falha nos jobs
* Compatibilidade futura com AWS Lambda/EC2

## Apêndices

* Scripts: setup de ambiente, systemd-user services
* Testes: pytest (scraper), vitest (hooks React), pre-commit hooks
* SEO: JSON-LD, meta OG tags
* Logging: arquivos rotativos locais

---

Versão: 2025-05-07
Autor: Bredi Tecnologia Digital / ChatGPT
