@echo off
echo ===================================================
echo Iniciando Todos os Componentes do BoraDeDesconto
echo Incluindo MCP Playwright para Automacao
echo ===================================================

echo.
echo [1/4] Configurando o ambiente MCP Playwright...
cd %~dp0\..\automation\mcp
node setup.js

echo.
echo [2/4] Iniciando API (porta 8000)...
start cmd /k "cd %~dp0\..\api && python app.py"
timeout /t 5

echo.
echo [3/4] Iniciando Frontend (porta 3000)...
start cmd /k "cd %~dp0\..\web && npm run dev"
timeout /t 5

echo.
echo [4/4] Iniciando Scraper...
start cmd /k "cd %~dp0\..\scraper && python main.py"
timeout /t 5

echo.
echo ===================================================
echo Todos os componentes iniciados!
echo.
echo API: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Para usar o MCP Playwright:
echo cd %~dp0\..\automation\mcp
echo node record_offers.js
echo ===================================================

echo.
echo Pressione qualquer tecla para iniciar o navegador...
pause > nul

start "" http://localhost:3000 