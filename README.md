# GMUD - Gestão de Calendário de Manutenção

Aplicação profissional para gerenciar manutenções de equipamentos críticos em produção.

## 📋 Funcionalidades

- ✅ Agendamento de manutenções
- ✅ Rastreamento de status (Agendado, Em Progresso, Concluído, Cancelado)
- ✅ Integração com GLPI (opcional)
- ✅ Dashboard com indicadores
- ✅ Filtros por equipamento e status
- ✅ Documentação automática com Swagger

## 🏗️ Estrutura do Projeto

```
Calendario GMUD/
├── app/
│   ├── models/           # Modelos do banco de dados
│   ├── schemas/          # Schemas Pydantic (validação)
│   ├── services/         # Serviços (GLPI, etc)
│   ├── routers/          # Rotas da API
│   ├── config.py         # Configurações
│   └── database.py       # Setup do banco
├── docs/                 # Documentação
├── templates/            # Templates (futuro)
├── main.py              # Entry point
├── requirements.txt     # Dependências
├── .env.example        # Variáveis de ambiente (exemplo)
└── README.md           # Este arquivo
```

## 🚀 Instalação e Uso

### 1. Clonar/Preparar o projeto
```bash
cd "TECNOLOGIA\SUPORTE\TECNICOS\HIGOR\Calendario GMUD"
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
```bash
# Copiar exemplo
copy .env.example .env

# Editar .env com suas configurações
# especialmente GLPI_URL, GLPI_APP_TOKEN, GLPI_USER_TOKEN
```

### 5. Executar aplicação
```bash
python main.py
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação da API

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints Principais

### GMUDs
- `POST /api/gmuds/` - Criar nova GMUD
- `GET /api/gmuds/` - Listar GMUDs (com filtros)
- `GET /api/gmuds/{id}` - Obter GMUD específica
- `PUT /api/gmuds/{id}` - Atualizar status
- `DELETE /api/gmuds/{id}` - Deletar GMUD

### Dashboard
- `GET /api/gmuds/dashboard/resumo` - Resumo do dashboard

## 📊 Exemplo de Requisição

```bash
curl -X POST http://localhost:8000/api/gmuds/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": "2026-04-15",
    "equipamento": "Compressor A",
    "descricao": "Manutenção preventiva do compressor",
    "justificativa": "Manutenção programada regular",
    "risco": "BAIXO"
  }'
```

## 🔧 Integração com GLPI

Se você usar GLPI para gestão de TI, configure as variáveis de ambiente:

```env
GLPI_URL=http://seu-glpi/
GLPI_APP_TOKEN=seu_app_token
GLPI_USER_TOKEN=seu_user_token
```

Quando uma GMUD é criada, um chamado será automaticamente registrado no GLPI.

## 📝 Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DATABASE_URL` | URL da base de dados | `sqlite:///./gmuds.db` |
| `GLPI_URL` | URL do GLPI | `http://localhost/glpi` |
| `GLPI_APP_TOKEN` | Token da app no GLPI | - |
| `GLPI_USER_TOKEN` | Token do usuário no GLPI | - |
| `DEBUG` | Modo debug | `False` |

## 🛠️ Desenvolvimento

### Estrutura de Arquivos
- **models/**: Definem as tabelas do banco
- **schemas/**: Definem os formatos de entrada/saída
- **services/**: Lógica de integração (GLPI, etc)
- **routers/**: Endpoints da API

### Adicionar novo endpoint
1. Criar função em `app/routers/gmuds.py`
2. Decorar com `@router.get()`, `@router.post()`, etc
3. A documentação Swagger será atualizada automaticamente

## 🗄️ Banco de Dados

Por padrão, usa SQLite (`gmuds.db`). Para usar PostgreSQL ou MySQL, altere `DATABASE_URL` em `.env`:

```env
# PostgreSQL
DATABASE_URL=postgresql://usuario:senha@localhost/gmuds

# MySQL
DATABASE_URL=mysql+pymysql://usuario:senha@localhost/gmuds
```

## 📊 Status de Manutenção

- `AGENDADO` - Manutenção agendada
- `EM_PROGRESSO` - Manutenção em execução
- `CONCLUIDO` - Manutenção finalizada
- `CANCELADO` - Manutenção cancelada

## 🎯 Próximos Passos

- [ ] Interface web (React/Vue)
- [ ] Autenticação de usuários
- [ ] Relatórios em PDF
- [ ] Notificações por email
- [ ] Testes unitários
- [ ] Deploy com Docker

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. Os logs da aplicação
2. Variáveis de ambiente (.env)
3. Conexão com banco de dados
4. Conectividade com GLPI (se configurado)

---

**Desenvolvido para gerenciar manutenções de equipamentos críticos com profissionalismo e segurança.**
