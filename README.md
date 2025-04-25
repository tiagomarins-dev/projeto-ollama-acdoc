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

## ✨ Autor

Criado por Tiago Marins.
