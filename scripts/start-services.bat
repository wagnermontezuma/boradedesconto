@echo off
REM Script para iniciar os serviços do BoraDeDesconto no Windows
REM Substitui o systemd-user services no Linux

REM Ajusta PATH para Node.js
set "PATH=%ProgramFiles%\nodejs;%PATH%"

echo Iniciando os serviços BoraDeDesconto...

REM Inicia a API FastAPI em uma janela
start "BoraDeDesconto API" cmd /k "cd %~dp0.. && env\Scripts\activate.bat && cd api && python -m uvicorn app:app --reload --port 8000"

REM Inicia o Frontend Next.js em uma janela
start "BoraDeDesconto Frontend" cmd /k "set PATH=C:\Program Files\nodejs;%PATH% && cd %~dp0..\web && npm.cmd run dev"

echo Serviços iniciados!
echo API: http://localhost:8000
echo Frontend: http://localhost:3000 