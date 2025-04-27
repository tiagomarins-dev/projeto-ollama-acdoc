# Ollama Multi-Model API + RAG (Setup Manual Atualizado)

Este projeto permite rodar múltiplos modelos LLM localmente com **Ollama**, expor uma API completa via **FastAPI** e utilizar **RAG** para consultas inteligentes em documentos.  
Agora também disponível com **upload remoto de documentos** e **instruções de agentes personalizados**.

---

## 🚀 Funcionalidades

- Executa modelos locais via Ollama
- API para gerar textos (`/gerar`)
- API para consultar documentos (`/rag`)
- Upload remoto de documentos (`/upload_doc`)
- Cadastro remoto de instruções de agentes (`/upload_instrucoes`)
- RAG (Retrieval-Augmented Generation) integrado
- Setup 100% automatizado
- Pronto para produção
- Scripts de watchdog (auto-restart) e start rápido

---

## 📦 Requisitos

- Ubuntu Server 20.04+ ou superior
- Python 3.8+
- Permissões de root
- Docker (opcional para quem quiser rodar com docker-compose)
- Ollama instalado

---

## 🛠️ Instalação

### 1. Baixar projeto

```bash
git clone https://github.com/seurepo/projeto-ollama-acdoc.git
cd projeto-ollama-acdoc
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Instalar Ollama

```bash
curl https://ollama.com/install.sh | sh
```

### 5. Baixar modelo necessário

```bash
ollama pull mistral
```

### 6. Iniciar API

```bash
./start.sh
```

---

## 📡 Endpoints disponíveis

### 1. Gerar texto com modelo LLM

**POST** `/gerar`

**Query Params:**
- `modelo` (obrigatório): nome do modelo (ex: `mistral`)
- `tokens` (opcional): limite de tokens gerados (default = 300)

**Body:**
```json
{
  "prompt": "Explique a inteligência artificial."
}
```

---

### 2. Consultar documentos (RAG)

**POST** `/rag`

**Body:**
```json
{
  "prompt": "Qual o tema principal dos documentos enviados?"
}
```

---

### 3. Upload de documento para RAG

**POST** `/upload_doc`

**Form-Data:**
- `file`: Arquivo `.txt` para adicionar ao RAG

---

### 4. Upload de instruções de agente

**POST** `/upload_instrucoes`

**Form-Data:**
- `file`: Arquivo `.txt` contendo instruções específicas do agente

---

## 📁 Estrutura do Projeto

```
├── app/
│   ├── __init__.py
│   ├── main.py              # API principal
│   ├── services/
│   │   ├── ollama_service.py   # Geração via Ollama
│   │   └── rag_service.py      # Mecanismo RAG
│   ├── models/
│   │   └── prompt_request.py   # Modelo de requisição FastAPI
│   └── storage/
│       ├── documentos/         # Documentos enviados
│       └── instrucoes/          # Instruções de agentes
├── start.sh                   # Start automático
├── watchdog.sh                # Watchdog auto-restart
├── requirements.txt
├── README.md
```

---

## 📚 Como Monitorar com Watchdog

Para garantir que o servidor UVicorn reinicie se cair:

```bash
./watchdog.sh
```

---

## 📚 Modelos compatíveis

- `mistral`
- `llama2`
- `llama3`
- `deepseek-coder`
- `gemma`
- `phi`
- `phi4`
- `mixtral`
- `command-r`
- `wizardlm2`
- `tinyllama`
- Outros modelos compatíveis com Ollama...

---

## ✨ Autor

Criado com ❤️ por **Tiago Marins**.

---

