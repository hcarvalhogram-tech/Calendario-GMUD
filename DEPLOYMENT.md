# GMUD - Deployment Guide

## 📦 Opção 1: Deployment Local (Recomendado para começar)

### Pré-requisitos
- Python 3.10+
- Windows/Linux/Mac

### Passos

1. **Extraia o projeto**
```bash
cd Calendario GMUD
```

2. **Execute o script de inicialização**
```bash
# Windows
INICIAR.bat

# Linux/Mac
chmod +x INICIAR.sh
./INICIAR.sh
```

3. **Acesse a aplicação**
```
http://SEU_IP:8000
```

---

## 🐳 Opção 2: Deployment com Docker (Produção)

### Pré-requisitos
- Docker instalado
- Docker Compose (opcional)

### Passos

1. **Build da imagem**
```bash
docker build -t gmud-app:latest .
```

2. **Rodar container**
```bash
docker run -d \
  --name gmud \
  -p 8000:8000 \
  -v gmud_db:/app \
  gmud-app:latest
```

3. **Acessar**
```
http://SEU_IP:8000
```

### Docker Compose

```bash
docker-compose up -d
```

---

## 🌐 Opção 3: Deploy em Servidor Remoto

### VPS/Cloud (AWS, Azure, DigitalOcean, etc)

1. **SSH na máquina**
```bash
ssh usuario@seu_servidor
```

2. **Clone/Upload do projeto**
```bash
git clone seu_repo
# ou
scp -r Calendario\ GMUD usuario@servidor:/home/app/
```

3. **Instale Python (se não tiver)**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

4. **Inicie**
```bash
cd Calendario\ GMUD
chmod +x INICIAR.sh
./INICIAR.sh
```

5. **Configure Nginx como proxy reverso**

```nginx
server {
    listen 80;
    server_name seu_dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔒 Segurança em Produção

### 1. Firewall
```bash
# Linux
sudo ufw allow 8000/tcp

# Windows
netsh advfirewall firewall add rule name="GMUD" dir=in action=allow protocol=tcp localport=8000
```

### 2. SSL/HTTPS
```bash
# Com Let's Encrypt (Nginx)
sudo certbot certonly --nginx -d seu_dominio.com
```

### 3. Autenticação
Configure em `.env`:
```env
DEBUG=False
ALLOWED_ORIGINS=["https://seu_dominio.com"]
```

### 4. Banco de Dados
Use PostgreSQL em produção (mais robusto):
```env
DATABASE_URL=postgresql://user:pass@localhost/gmuds
```

---

## 📊 Monitoramento

### Logs
```bash
# Ver logs do container
docker logs -f gmud

# Arquivo de log
tail -f logs/app.log
```

### Health Check
```bash
curl http://seu_ip:8000/health
```

---

## 🆘 Troubleshooting

| Erro | Solução |
|------|---------|
| Port already in use | `lsof -i :8000` e mude porta em `.env` |
| DB locked | Delete `gmuds.db` para resetar |
| Permission denied | `chmod +x *.sh` |
| Module not found | `pip install -r requirements.txt` |

---

## 📈 Performance

- **Usuários simultâneos**: Para 50+, use Gunicorn + Nginx
- **Banco de dados**: PostgreSQL para produção
- **Cache**: Redis para cache de dashboard
- **Load Balancer**: Nginx/HAProxy para múltiplas instâncias

---

## 🚀 Próximos Passos

1. Teste em ambiente de desenvolvimento
2. Configure backup do banco de dados
3. Configure SSL/HTTPS
4. Implante em servidor dedicado
5. Configure CI/CD para updates automáticos
