# GMUD - Guia de Acesso em Rede

## 🚀 Acessar a Aplicação

### 1️⃣ Servidor Iniciado

O servidor está rodando em **http://0.0.0.0:8000** e aceita conexões de qualquer lugar.

### 2️⃣ Acesso Local (Mesma Máquina)

```
http://localhost:8000
http://127.0.0.1:8000
```

### 3️⃣ Acesso Pela Rede (Outro Computador)

**Substitua `SEU_IP` pelo IP da máquina que está rodando o servidor:**

```
http://SEU_IP:8000
```

#### Como encontrar o IP do servidor:

**Windows:**
```powershell
ipconfig
```
Procure por "IPv4 Address" e use esse número

**Linux/Mac:**
```bash
ifconfig
hostname -I
```

#### Exemplo:
Se o IP for `192.168.1.100`, acesse:
```
http://192.168.1.100:8000
```

---

## 📋 URLs Úteis

| Recurso | URL |
|---------|-----|
| **Dashboard** | `http://SEU_IP:8000` |
| **API Docs** | `http://SEU_IP:8000/docs` |
| **ReDoc** | `http://SEU_IP:8000/redoc` |
| **Health Check** | `http://SEU_IP:8000/health` |

---

## 🔑 Passos para o Time Acessar

### 1. Server está rodando
```
INICIAR.bat (Windows)
./INICIAR.sh (Linux/Mac)
```

### 2. Pegue o IP da máquina do servidor
```
Ele aparecerá na tela ao iniciar
```

### 3. Compartilhe com o time
```
"Acesse http://192.168.1.100:8000 no seu navegador"
```

### 4. Time acessa
```
Todos na rede podem usar a aplicação normalmente
```

---

## 🛡️ Segurança

⚠️ **Atenção:** O servidor está acessível na rede local. Se estiver em uma rede pública/internet:

1. **Use um firewall** para bloquear acesso não autorizado
2. **Adicione autenticação** (usuário/senha)
3. **Use SSL/HTTPS** se expor na internet
4. **Considere usar VPN** para acesso remoto seguro

---

## 🐳 Deploy com Docker (Produção)

Se quiser facilitar o deploy, use Docker:

```bash
docker build -t gmud-app .
docker run -p 8000:8000 gmud-app
```

Todos no time podem acessar sem precisar de Python instalado!

---

## 📞 Troubleshooting

### "Conexão recusada"
- Verifique se o servidor está rodando
- Confirme que o IP está correto
- Verifique firewall/antivírus

### "Página branca/erro"
- Limpe cache do navegador
- Tente em navegador diferente
- Verifique console (`F12`) para erros

### "Não consigo acessar de outra máquina"
- Ping no IP: `ping 192.168.1.100`
- Verifique firewall do Windows: Permitir porta 8000
- Verifique se estão na mesma rede

---

## 💡 Dicas

✅ Deixe o servidor rodando em uma máquina 24/7 para acesso constante
✅ Use o mesmo IP/porta sempre para facilitar os acessos
✅ Documente o IP em um local acessível para o time
✅ Teste o acesso antes de usar em produção
