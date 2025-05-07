#!/bin/bash
# Script para instalar os serviços do BoraDeDesconto no systemd-user.

set -e

# Diretório do projeto
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# Verifica se o diretório existe
if [ ! -d "$PROJECT_DIR" ]; then
  echo "Diretório do projeto não encontrado: $PROJECT_DIR"
  exit 1
fi

# Cria diretório para os serviços se não existir
mkdir -p ~/.config/systemd/user/

# Define o serviço de API
cat > ~/.config/systemd/user/deals-api.service << EOF
[Unit]
Description=BoraDeDesconto API Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/env/bin/uvicorn api.app:app --host 127.0.0.1 --port 8000
Restart=on-failure
RestartSec=5
Environment="PYTHONPATH=$PROJECT_DIR"

[Install]
WantedBy=default.target
EOF

# Define o serviço de Scraper
cat > ~/.config/systemd/user/deals-scraper.service << EOF
[Unit]
Description=BoraDeDesconto Scraper Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/env/bin/python scraper/scheduler.py
Restart=on-failure
RestartSec=10
Environment="PYTHONPATH=$PROJECT_DIR"

[Install]
WantedBy=default.target
EOF

# Recarrega os serviços do systemd
systemctl --user daemon-reload

# Habilita os serviços
systemctl --user enable deals-api.service
systemctl --user enable deals-scraper.service

echo "Serviços instalados com sucesso!"
echo "Para iniciar os serviços, execute:"
echo "systemctl --user start deals-api.service"
echo "systemctl --user start deals-scraper.service"
echo ""
echo "Para verificar o status, execute:"
echo "systemctl --user status deals-api.service"
echo "systemctl --user status deals-scraper.service" 