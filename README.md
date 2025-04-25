# Ollama Multi-Model API

Este projeto permite rodar múltiplos modelos LLM localmente com **Ollama** e expor uma API simples via **FastAPI**.  
Você pode consultar modelos como `mistral`, `llama2` e `deepseek-chat` usando um único endpoint HTTP.

---

## 🚀 Funcionalidades

- Executa modelos locais com Ollama
- API unificada para múltiplos modelos
- Totalmente dockerizado
- Ideal para uso com FastAPI + RAG

---

## 📦 Requisitos

- Docker
- Docker Compose
- Ollama (instalado via container)

---

## 🧪 Como usar

### 1. Suba os containers:

```bash
docker-compose up --build -d
```

Isso iniciará a API em `http://localhost:8000` e o Ollama em `http://localhost:11434`.

### 2. Faça uma requisição POST:

**Endpoint:**

```
POST /gerar?modelo=mistral
```

**Body JSON:**

```json
{
  "prompt": "Explique a teoria da relatividade."
}
```

Você pode substituir `modelo` por:
- `mistral`
- `llama2`
- `deepseek-chat`

---

## 🛠 Arquitetura

- **FastAPI** para expor a API
- **Ollama** para gerar as respostas localmente
- **Docker Compose** para orquestrar tudo

---

## 📁 Estrutura

```
├── main.py              # API FastAPI
├── Dockerfile           # Ambiente Python
├── docker-compose.yml   # Orquestra API + Ollama
├── requirements.txt     # Dependências Python
└── README.md            # Este arquivo
```

---

## 🧠 Dica

Se estiver usando cloud-init (como na Hetzner), clone este repositório automaticamente e execute o `docker-compose up` no boot do servidor.

---

## ✨ Autor

Criado por Tiago com ❤️ e LLMs.