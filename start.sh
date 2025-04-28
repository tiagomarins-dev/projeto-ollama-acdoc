#!/bin/bash

# Nome das sessões
API_SESSION="minhaapi"
OLLAMA_SESSION="ollama"

echo "🚀 Iniciando ambientes..."

# Ativa o ambiente virtual
source venv/bin/activate

# Subindo Ollama no screen separado
echo "🐳 Subindo Ollama no screen '$OLLAMA_SESSION'..."
if screen -list | grep -q "$OLLAMA_SESSION"; then
    echo "Sessão Ollama existente encontrada. Matando..."
    screen -S "$OLLAMA_SESSION" -X quit
fi
screen -dmS "$OLLAMA_SESSION" bash -c "
    ollama serve
"

# Aguarda o Ollama iniciar
echo "⏳ Aguardando Ollama iniciar..."
sleep 10

# Subindo API no screen separado
echo "🔧 Subindo API no screen '$API_SESSION'..."
if screen -list | grep -q "$API_SESSION"; then
    echo "Sessão API existente encontrada. Matando..."
    screen -S "$API_SESSION" -X quit
fi
screen -dmS "$API_SESSION" bash -c "
    source venv/bin/activate
    echo 'Matando processos na porta 9000...'
    if command -v fuser &> /dev/null; then
        fuser -k 9000/tcp
    else
        lsof -ti tcp:9000 | xargs kill -9
    fi
    echo '⏳ Inicializando Indexação RAG...'
    python3 app/scripts/reindex_all.py
    echo '🚀 Subindo servidor Uvicorn...'
    uvicorn app.main:app --host 0.0.0.0 --port 9000 --proxy-headers --forwarded-allow-ips '*' --reload
"

sleep 10
echo "✅ Tudo rodando!"
echo "👉 API logs:    screen -r $API_SESSION"
echo "👉 Ollama logs: screen -r $OLLAMA_SESSION"