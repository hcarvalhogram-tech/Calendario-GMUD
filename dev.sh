#!/bin/bash
# Script para iniciar ambiente de desenvolvimento

echo "🚀 Iniciando GMUD em modo desenvolvimento..."

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências de desenvolvimento
echo "📦 Instalando dependências..."
pip install -r requirements-dev.txt

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "⚙️  Criando .env..."
    cp .env.example .env
fi

# Iniciar em modo debug
echo "✅ Iniciando servidor..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
