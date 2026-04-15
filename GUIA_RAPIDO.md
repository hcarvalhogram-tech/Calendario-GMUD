# 🚀 GMUD - Guia Rápido para o Time

## 3 Formas de Usar

### ✅ FORMA 1: Simples (Windows)
```
1. Abra a pasta GMUD
2. Clique em INICIAR.bat
3. Espere a mensagem com o link
4. Compartilhe o link com o time
5. Pronto!
```

### ✅ FORMA 2: Docker (Mais Fácil)
```bash
docker-compose up -d
```
Acesse: `http://seu_ip:8000`

### ✅ FORMA 3: Manual
```bash
python -m venv venv
venv\Scripts\pip install -r requirements.txt
python main.py
```

---

## 🔗 Como Acessar

### Servidor ON
```
Local:  http://localhost:8000
Rede:   http://192.168.1.X:8000
```

**Substitua `192.168.1.X` pelo IP verdadeiro**

---

## 📋 O que Você Pode Fazer

- 📊 **Dashboard** - Ver estatísticas
- 📆 **Calendário** - Visualizar manutenções
- 📝 **Adicionar** - Agendar nova manutenção
- 🔍 **Filtrar** - Por equipamento/status
- 🗑️ **Deletar** - Remover manutenções

---

## 🔧 Encontrar IP

**Windows:**
```
windows + r
ipconfig
Procure: IPv4 Address
```

**Linux/Mac:**
```
hostname -I
ifconfig
```

---

## 📱 Dica: Compartilhe com o Time

```
"Acesse http://[IP]:8000 no navegador"
```

Exemplo:
```
"Acesse http://192.168.1.50:8000 no navegador"
```

---

E pronto! 🎉
