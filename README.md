# Ollama Multi-Model API (com Setup Manual)

Este projeto permite rodar múltiplos modelos LLM localmente com **Ollama** e expor uma API simples via **FastAPI**.  
Agora também disponível com **instalação completa via script `.sh`**.

---

## 🚀 Funcionalidades

- Executa modelos locais com Ollama
- API unificada para múltiplos modelos
- Totalmente dockerizado
- Setup 100% automatizado com script bash
- Ideal para uso com FastAPI + RAG

---

## 📦 Requisitos

- Ubuntu Server 20.04+ ou superior
- Permissões de root para instalar pacotes

---

## 🛠️ Instalação Automática

1. Faça login no seu servidor via SSH.
2. Clone este repositório ou crie o arquivo `setup-ollama-server.sh`.
3. Dê permissão de execução:

```bash
chmod +x setup-ollama-server.sh
```

4. Execute:

```bash
./setup-ollama-server.sh
```

5. Acesse a API:

```
http://SEU_IP:8000/docs
```

---

## 📡 Como usar a API

### Endpoint `/gerar`

**Método:** `POST`

**URL:** 
```
/gerar?modelo=mistral&tokens=200
```

**Body JSON:**

```json
{
  "prompt": "Explique a inteligência artificial."
}
```

**Parâmetros disponíveis:**
- `modelo` (query param) — Exemplo: `mistral`, `llama2`, `deepseek-chat`
- `tokens` (query param) — Limite de geração de tokens (opcional, padrão 300)

---

## 📁 Estrutura do Projeto

```
├── main.py              # API FastAPI
├── Dockerfile           # Ambiente Python
├── docker-compose.yml   # Orquestra API + Ollama
├── requirements.txt     # Dependências Python
├── setup-ollama-server.sh # Script de instalação completa
└── README.md            # Este arquivo
```


---

## 📚 Modelos disponíveis para uso na API

Todos os modelos abaixo podem ser usados assim:

```
POST /gerar?modelo=nome-do-modelo&tokens=200
```

**Exemplo:**
```
/gerar?modelo=phi4&tokens=300
```

### ✅ Modelos instalados com o script:

- `mistral` → `?modelo=mistral`
- `llama2` → `?modelo=llama2`
- `llama3` → `?modelo=llama3`
- `llama3:8b` → `?modelo=llama3`
- `llama3:70b` → `?modelo=llama3`
- `deepseek-coder` → `?modelo=deepseek-coder`
- `deepseek-r1:7b` → `?modelo=deepseek-r1`
- `deepseek-r1:14b` → `?modelo=deepseek-r1`
- `gemma:2b` → `?modelo=gemma`
- `gemma3` → `?modelo=gemma3`
- `phi` → `?modelo=phi`
- `phi4` → `?modelo=phi4`
- `phi3` → `?modelo=phi3`
- `phi3.5` → `?modelo=phi3.5`
- `qwen2.5:7b` → `?modelo=qwen2.5`
- `qwen2.5:14b` → `?modelo=qwen2.5`
- `qwen2.5-coder:7b` → `?modelo=qwen2.5-coder`
- `mixtral:8x7b` → `?modelo=mixtral`
- `mixtral:8x22b` → `?modelo=mixtral`
- `dolphin-llama3:8b` → `?modelo=dolphin-llama3`
- `starcoder2:7b` → `?modelo=starcoder2`
- `codellama:7b` → `?modelo=codellama`
- `command-r` → `?modelo=command-r`
- `wizardlm2:7b` → `?modelo=wizardlm2`
- `tinyllama` → `?modelo=tinyllama`

---

## ✨ Autor

Criado por Tiago Marins.
