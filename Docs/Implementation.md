== Implementation

A implementação do BoraDeDesconto foi pensada para ser 100% user-space, compatível com sistemas como Bazzite OS. O fluxo completo pode ser validado com os seguintes passos:

=== Setup do Ambiente

[source,bash]
----
# Clonar repositório
mkdir -p ~/Projects && cd ~/Projects
git clone git@github.com:usuario/boradedesconto.git
cd boradedesconto

# Criar ambiente Python
python3.12 -m venv env
source env/bin/activate
pip install -r requirements.txt
playwright install chromium

# Instalar dependências Node.js
nvm install 20
cd web && npm install && cd ..

# Inicializar banco SQLite
python - <<<'import asyncio,api.models as m;asyncio.run(m.init_db())'
----

=== Serviços via systemd‑user

Para executar os serviços de forma persistente, sem privilégios root, é usado `systemd --user`.

[source,bash]
----
# Habilita serviços de API e scraper
bash scripts/install-services.sh
----

Serviços criados:

* `deals-api.service`
* `deals-scraper.service`

=== Execução Local Manual (para dev)

[cols="1,2,1", options="header"]
|===
| Serviço     | Comando                                    | Porta
| Scraper     | `python scraper/main.py`                   | —
| Scheduler   | `python scraper/scheduler.py`              | —
| API         | `uvicorn api.app:app --reload --port 8000` | 8000
| Frontend    | `npm run dev --workspace=web -p 3000`      | 3000
|===

=== Deploy Local de Integrações

* **Mautic**: roda local via PHP-FPM e SQLite em `env/mautic/`.
* **wa-bot**: microserviço Node.js que escuta via `ngrok` e responde mensagens.
* Configuração do bot no WhatsApp Cloud API para apontar para o webhook.

---

Posso seguir para a seção de **Milestones**, com o cronograma de entregas semanais já planejado?
