# GMUD - Quick Start Guide

## 🚀 Início Rápido

### Windows
```bash
# Executar script de desenvolvimento
dev.bat

# A aplicação estará em: http://localhost:8000
# Swagger em: http://localhost:8000/docs
```

### Linux/Mac
```bash
# Dar permissão de execução
chmod +x dev.sh

# Executar script
./dev.sh
```

## 📦 Setup Manual

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Criar .env (copiar de exemplo)
copy .env.example .env

# 5. Iniciar
python main.py
```

## 🧪 Testes

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar testes
pytest tests/

# Com cobertura
pytest tests/ --cov=app
```

## 🐳 Docker

```bash
# Construir imagem
docker build -t gmud-api .

# Executar com docker-compose
docker-compose up
```

## 📊 Acessar

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health**: http://localhost:8000/health

## 🔧 Configuração GLPI

Editar `.env`:
```env
GLPI_URL=http://seu-glpi-server/glpi
GLPI_APP_TOKEN=seu_app_token_aqui
GLPI_USER_TOKEN=seu_user_token_aqui
```

## 📝 Estrutura

```
Calendario GMUD/
├── app/
│   ├── models/      # BD models
│   ├── schemas/     # Validação
│   ├── services/    # Lógica de negócio
│   └── routers/     # Endpoints API
├── tests/           # Testes automatizados
├── docs/            # Documentação
├── main.py         # Entry point
└── requirements.txt # Dependências
```

## 🎯 Próximos Passos

1. Configurar `.env` com suas variáveis
2. Executar testes: `pytest tests/`
3. Acessar Swagger: http://localhost:8000/docs
4. Criar primeira GMUD via API

**Dúvidas?** Veja o README.md completo!
