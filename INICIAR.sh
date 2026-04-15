#!/bin/bash
# Script para iniciar GMUD - Calendário de Manutenção (Linux/Mac)

clear
echo "=========================================="
echo "  GMUD - Gestão de Manutenção"
echo "  Iniciando servidor..."
echo "=========================================="
echo ""

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
source venv/bin/activate

# Instalar/verificar dependências
echo "Verificando dependências..."
pip install -q fastapi uvicorn[standard] sqlalchemy pydantic pydantic-settings python-dotenv requests python-docx

# Encontrar IP
IP=$(ifconfig | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -1)
if [ -z "$IP" ]; then
    IP=$(hostname -I | awk '{print $1}')
fi

echo ""
echo "=========================================="
echo "   ✅ SERVIDOR INICIANDO"
echo "=========================================="
echo ""
echo "Acesso LOCAL:"
echo "   🌐 http://localhost:8000"
echo "   🌐 http://127.0.0.1:8000"
echo ""
echo "Acesso PELA REDE (compartilhe isso com seu time):"
echo "   🌐 http://$IP:8000"
echo ""
echo "Dashboard disponível em:"
echo "   - http://$IP:8000 (Interface visual)"
echo "   - http://$IP:8000/docs (API Documentation)"
echo ""
echo "=========================================="
echo ""

# Iniciar servidor
python main.py
