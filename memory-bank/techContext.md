# techContext.md

## Tecnologias Utilizadas
- **Backend:** Python 3.12, FastAPI, APScheduler, Playwright, httpx
- **Banco de Dados:** SQLite 3 (modo WAL)
- **Frontend:** Next.js 15, Tailwind CSS
- **Sistema Operacional:** Windows 11
- **Gerenciamento:** systemd-user services (a ser adaptado para Windows)
- **Integrações Futuras:** Mautic (CRM), WhatsApp Cloud API, OpenAI (LLM), Redis Streams

## Setup de Desenvolvimento
- Ambiente Python isolado (venv)
- Node.js 20 via instalação direta no Windows
- Git instalado via winget
- Instalação de browsers headless Playwright em user-space
- Inicialização do banco via script Python
- Adaptação dos serviços para Windows (alternativa ao systemd)

## Restrições Técnicas
- Proibido uso de root/Docker
- Compatibilidade com Windows 11
- Banco local, sem servidor externo
- Integração futura com AWS (RDS, Lambda, ECS)

## Dependências
- Python: FastAPI, APScheduler, Playwright, httpx, tenacity
- Node: Next.js, Tailwind, Vitest
- Outros: Mautic, ngrok, Redis (para watch-jobs)
- Windows: winget (gerenciador de pacotes) 