# projectbrief.md

## Objetivo
Desenvolver uma plataforma de agregação de ofertas em tempo quase-real, coletando promoções de grandes e-commerces (Amazon, Mercado Livre, AliExpress, Shopee, etc.), armazenando em banco SQLite e apresentando em uma landing page Next.js. O MVP deve rodar 100% em user-space, sem root ou Docker, facilitando testes em sistemas imutáveis como o Bazzite OS.

## Escopo
- Scraper automatizado (APScheduler, Playwright, httpx)
- Banco local SQLite (modo WAL)
- API REST (FastAPI)
- UI responsiva (Next.js + Tailwind)
- Integrações futuras: WhatsApp, CRM (Mautic), LLM (OpenAI)

## Requisitos Essenciais
- Coleta automatizada de ofertas (Amazon, Mercado Livre)
- API REST: /offers, /offers/{id}, /go/{id}
- Interface responsiva com grid dinâmico e filtros
- Instalação user-space total
- Logging local
- Registro de cliques e redirecionamento

## Fora de Escopo
- Interface administrativa
- Pagamentos embutidos
- Suporte a múltiplos idiomas 