@echo off
REM Script para iniciar GMUD - Calendário de Manutenção
REM Este script facilita o startup da aplicação para todo o time

cls
echo ==========================================
echo   GMUD - Gestao de Manutencao
echo   Iniciando servidor...
echo ==========================================
echo.

REM Verificar se venv existe
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv e instalar/verificar dependencias
echo Verificando dependencias...
call venv\Scripts\pip.exe install -q fastapi uvicorn[standard] sqlalchemy pydantic pydantic-settings python-dotenv requests python-docx 2>nul

REM Encontrar IP da maquina
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4"') do set IP=%%a
set IP=%IP:~1%

REM Se houver multiplos IPs, pegar o primeiro
for /f "tokens=1" %%a in ("%IP%") do set IP=%%a

echo.
echo ==========================================
echo   ✅ SERVIDOR INICIANDO
echo ==========================================
echo.
echo Acesso LOCAL:
echo   🌐 http://localhost:8000
echo   🌐 http://127.0.0.1:8000
echo.
echo Acesso PELA REDE (compartilhe isso com seu time):
echo   🌐 http://%IP%:8000
echo.
echo Dashboard disponivel em:
echo   - http://%IP%:8000 (Interface visual)
echo   - http://%IP%:8000/docs (API Documentation)
echo.
echo ==========================================
echo.

REM Iniciar servidor
call venv\Scripts\python.exe main.py
pause
