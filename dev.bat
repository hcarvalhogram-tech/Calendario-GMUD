@echo off
REM Script para iniciar ambiente de desenvolvimento no Windows

echo 🚀 Iniciando GMUD em modo desenvolvimento...

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Instalar dependências de desenvolvimento
echo 📦 Instalando dependências...
pip install -r requirements-dev.txt

REM Criar arquivo .env se não existir
if not exist ".env" (
    echo ⚙️ Criando .env...
    copy .env.example .env
)

REM Iniciar em modo debug
echo ✅ Iniciando servidor...
uvicorn main:app --reload --host 0.0.0.0 --port 8000
