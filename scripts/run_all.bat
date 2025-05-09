@echo off
REM Script para automatizar setup e execução do BoraDeDesconto no Windows

REM Altera para o diretório raiz do projeto
cd /d "%~dp0\.."

REM Ativa o ambiente virtual
call env\Scripts\activate.bat

REM Instala dependências Python
pip install --no-cache-dir -r requirements.txt

REM Instala navegadores do Playwright
playwright install chromium

REM Executa o scraper para Amazon
echo.
echo ===== Executando scraper Amazon =====
python -m scraper.main amazon
echo ===== Scraper finalizado =====
echo.

REM Inicia a API em nova janela
echo ===== Iniciando API =====
start "API" cmd /k "call env\Scripts\activate.bat && uvicorn api.app:app --reload --port 8000"

echo.
REM Inicia o frontend em nova janela
echo ===== Iniciando Frontend =====
start "Frontend" cmd /k "cd web && npm run dev"

echo.
pause 