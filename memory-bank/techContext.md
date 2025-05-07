# techContext.md

## Tecnologias Utilizadas
- **Backend:** Python 3.12, FastAPI, APScheduler, Playwright, httpx
- **Banco de Dados:** SQLite 3 (modo WAL)
- **Frontend:** Next.js 15, Tailwind CSS
- **Gerenciamento:** systemd-user services
- **Integrações Futuras:** Mautic (CRM), WhatsApp Cloud API, OpenAI (LLM), Redis Streams

## Setup de Desenvolvimento
- Ambiente Python isolado (venv)
- Node.js 20 via nvm para frontend
- Instalação de browsers headless Playwright em user-space
- Inicialização do banco via script Python
- Serviços gerenciados por systemd --user (sem root)

## Restrições Técnicas
- Proibido uso de root/Docker
- Compatível com sistemas imutáveis (ex: Bazzite OS)
- Banco local, sem servidor externo
- Integração futura com AWS (RDS, Lambda, ECS)

## Dependências
- Python: FastAPI, APScheduler, Playwright, httpx, tenacity
- Node: Next.js, Tailwind, Vitest
- Outros: Mautic, ngrok, Redis (para watch-jobs) 