# 🚀 DEPLOYMENT EM VM - GUIA COMPLETO

## 📌 Visão Geral

Este guia fornece instruções passo a passo para fazer deploy do sistema GMUD em uma Máquina Virtual (VM) para uso de toda a equipe. O sistema será acessável de qualquer máquina na rede.

**Tempo estimado**: 15-30 minutos

---

## 🎯 O QUE VOCÊ TERÁ AO FINAL

- Sistema GMUD rodando em uma VM
- Acessível via URL: `http://[IP-DA-VM]:8000`
- Gerar documentos Word com dados de manutenção
- Banco de dados persistente
- Todos do time podem acessar e usar

---

## 📋 REQUISITOS

### Hardware Mínimo
- **RAM**: 2GB (recomendado 4GB)
- **Disco**: 20GB livre
- **Processador**: Qualquer processador moderno (2 cores mínimo)

### Software
- **Windows Server 2019+** OU **Linux (Ubuntu 20.04+)** OU **Docker**
- **Python 3.10+** (se não usar Docker)
- Acesso à rede (máquinas podem se comunicar)

---

## 🔧 OPÇÃO 1: DEPLOY COM PYTHON (Windows/Linux)

### Passo 1: Copiar Projeto para VM

```bash
# Windows PowerShell
Copy-Item -Path "t:\TECNOLOGIA\SUPORTE\TECNICOS\HIGOR\Calemdario GMUD" `
          -Destination "C:\apps\calendario-gmud" -Recurse

# OU Linux/Mac
cp -r ~/Calendario\ GMUD /opt/calendario-gmud
cd /opt/calendario-gmud
```

### Passo 2: Instalar Dependências

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Passo 3: Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env
# Alterar:
# SERVER_HOST=0.0.0.0
# SERVER_PORT=8000
# DATABASE_URL=sqlite:///gmuds.db
```

### Passo 4: Iniciar Servidor

```bash
# Windows
python main.py

# Linux
python3 main.py
```

✅ **Sucesso!** Servidor rodando em `http://[IP-DA-VM]:8000`

---

## 🐳 OPÇÃO 2: DEPLOY COM DOCKER (RECOMENDADO)

### Passo 1: Instalar Docker

```bash
# Windows
# Baixar Docker Desktop em: https://www.docker.com/products/docker-desktop
# Executar instalador e reiniciar

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Iniciar serviço
sudo systemctl start docker
sudo usermod -aG docker $USER  # Adicionar usuário ao grupo docker
```

### Passo 2: Copiar Projeto

```bash
cp -r "Calendario GMUD" /opt/calendario-gmud
cd /opt/calendario-gmud
```

### Passo 3: Construir e Executar

```bash
# Build da imagem
docker build -t calendario-gmud:latest .

# Rodar container
docker run -d \
  --name calendario-gmud \
  -p 8000:8000 \
  -v calendario-gmud-data:/app/data \
  calendario-gmud:latest

# Usando docker-compose (mais fácil)
docker-compose up -d
```

✅ **Sucesso!** Servidor rodando em `http://[IP-DA-VM]:8000`

---

## ☁️ OPÇÃO 3: DEPLOY EM CLOUD (AWS, Azure, Google Cloud)

### AWS EC2 - Quick Setup

```bash
# 1. Criar instância EC2
# - AMI: Ubuntu 20.04 LTS
# - Tipo: t2.micro (free tier)
# - Security Group: permitir PORT 8000

# 2. Conectar via SSH
ssh -i key.pem ubuntu@ip-da-instancia

# 3. Instalar dependências
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv git

# 4. Clonar projeto (ou copiar via SCP)
git clone https://seu-repositorio.git calendario-gmud
cd calendario-gmud

# 5. Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Ngnix + Gunicorn (Para produção)

```bash
# Instalar Nginx
sudo apt-get install nginx gunicorn

# Criar arquivo de config (/etc/nginx/sites-available/calendario-gmud)
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Ativar
sudo ln -s /etc/nginx/sites-available/calendario-gmud /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Rodar Gunicorn em background
gunicorn -w 4 -b 0.0.0.0:8000 main:app &
```

---

## 📍 ENCONTRAR O IP DA VM

### Windows
```powershell
ipconfig
# Procurar por "IPv4 Address" (Ex: 192.168.1.50)
```

### Linux
```bash
ip addr show
# ou
hostname -I
```

### Mac
```bash
ifconfig | grep inet
```

---

## 🌐 ACESSAR DO TIME

### 1. Descobrir IP da VM
```
IP: 192.168.1.50 (exemplo)
```

### 2. Compartilhar URL com o Time
```
http://192.168.1.50:8000
```

### 3. Cada membro acessa no navegador
```
Chrome, Firefox, Edge, Safari...
```

---

## 📄 NOVO: GERAÇÃO DE DOCUMENTOS

Quando usuários clicam no botão **"📄 Baixar"** na tabela de manutenções:

1. ✅ Sistema gera documento Word automaticamente
2. 📥 Arquivo baixa com dados preenchidos
3. 🖨️ Gestor pode imprimir diretamente

**Arquivo gerado**: `GMUD_[ID]_[EQUIPAMENTO].docx`

### O que é Incluído:
- ✓ Informações da manutenção
- ✓ Equipamento e data
- ✓ Descrição e justificativa
- ✓ Nível de risco
- ✓ Status
- ✓ **Espaço para assinaturas**
- ✓ Formatação profissional para impressão

---

## 🔒 SEGURANÇA EM VM

### 1. Firewall
```powershell
# Windows - Permitir porta 8000
New-NetFirewallRule -DisplayName "GMUD App" -Direction Inbound `
  -Action Allow -Protocol TCP -LocalPort 8000

# Linux
sudo ufw allow 8000
```

### 2. Credenciais
```
# NUNCA comitar .env para Git
# NUNCA deixar senhas em código
# USAR variáveis de ambiente
```

### 3. Acesso Restrito (Opcional)
```
# Se apenas rede interna deve acessar:
# Configurar firewall para bloquear de fora
```

### 4. SSL/HTTPS (Produção)
```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Gerar certificado
sudo certbot certonly --standalone -d seu-dominio.com

# Configurar Nginx para HTTPS
# (Arquivo de config do nginx deve ter ssl_certificate e ssl_key)
```

---

## 🛠️ TROUBLESHOOTING

### ❌ Erro: "Porta 8000 já em uso"
```powershell
# Windows
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Linux
lsof -i :8000
kill -9 [PID]
```

### ❌ Erro: "ModuleNotFoundError"
```bash
# Verificar se requirements instalados
pip list

# Reinstalar
pip install -r requirements.txt --force-reinstall
```

### ❌ Erro: "Connection refused"
```
✓ Verificar firewall permite porta 8000
✓ Verificar servidor está rodando
✓ Verificar IP correto
✓ Verificar máquinas estão na mesma rede
```

### ❌ Documento não baixa
```
✓ Verificar python-docx instalado: pip install python-docx
✓ Verificar espaço em disco disponível
✓ Verificar permissões de arquivo
```

---

## 📊 MONITORAMENTO

### Ver Log da Aplicação
```bash
# Windows PowerShell
Get-Content -Path app.log -Tail 50

# Linux
tail -f app.log
```

### Status do Docker
```bash
docker ps
docker logs calendario-gmud
```

### Performance
```bash
# Ver uso de recursos
docker stats
```

---

## 🔄 BACKUP & RESTAURAÇÃO

### Backup do Banco de Dados
```bash
# Copiar arquivo de banco
cp gmuds.db gmuds.backup.db

# Ou com data
cp gmuds.db "backup/gmuds_$(date +%Y-%m-%d).db"
```

### Restaurar do Backup
```bash
cp gmuds.backup.db gmuds.db
```

### Backup Automatizado (Cron Linux)
```bash
# Adicionar ao crontab: crontab -e
0 3 * * * cp /opt/calendario-gmud/gmuds.db /backups/gmuds_$(date +\%Y-\%m-\%d).db
```

---

## 📞 SUPORTE E PRÓXIMOS PASSOS

### Agora que o Sistema Está Rodando:

1. **Teste de Acesso**
   - Acesse de outra máquina
   - Crie uma GMUD de teste
   - Baixe o documento
   - Teste impressão

2. **Integração GLPI** (Opcional)
   - Verificar `app/config.py`
   - Configurar `GLPI_URL` e `GLPI_API_TOKEN`

3. **Treinamento do Time**
   - Compartilhe GUIA_RAPIDO.md
   - Mostre como criar GMUD
   - Mostre como baixar documento
   - Mostre como imprimir

4. **Monitoramento Contínuo**
   - Verifique logs regularmente
   - Faça backups periódicos
   - Atualize sistema operacional
   - Mantenha Python/Docker atualizados

---

## 📚 ARQUIVOS RELACIONADOS

- [GUIA_RAPIDO.md](GUIA_RAPIDO.md) - Guia de uso para o team
- [ACESSO_REDE.md](ACESSO_REDE.md) - Troubleshooting de rede
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment geral
- [README.md](README.md) - Documentação técnica
- [COMECE_AQUI.txt](COMECE_AQUI.txt) - Início rápido

---

## ✅ CHECKLIST PRÉ-PRODUÇÃO

- [ ] VM criada e acessível
- [ ] Python/Docker instalado
- [ ] Projeto copiado para VM
- [ ] Dependências instaladas
- [ ] .env configurado
- [ ] Servidor inicia sem erros
- [ ] Banco de dados criado
- [ ] Acesso de outra máquina testado
- [ ] GMUD criada e funcionando
- [ ] Documento gerado e baixado com sucesso
- [ ] Documento impresso com sucesso
- [ ] Team pode acessar URL
- [ ] Backup automático configurado

---

## 🎉 SUCESSO!

Seu sistema GMUD está pronto para toda a equipe usar em produção!

**URL de Acesso**: `http://[IP-DA-VM]:8000`

Qualquer dúvida, consulte os guias complementares ou verifique os logs.

---

**Desenvolvido com ❤️ para sua equipe de manutenção**

*Última atualização: Abril 2026*
