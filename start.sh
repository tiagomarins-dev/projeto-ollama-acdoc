#!/bin/bash

# Nome das sessões do screen
API_SESSION="minhaapi"
OLLAMA_SESSION="ollama"

# Ativa o ambiente virtual e sobe o servidor dentro do screen
echo "🚀 Iniciando ambientes..."

# Mata sessões antigas, se existirem
for SESSION in "$API_SESSION" "$OLLAMA_SESSION"; do
    if screen -list | grep -q "$SESSION"; then
        echo "⚡ Matando sessão antiga '$SESSION'..."
        screen -S "$SESSION" -X quit
    fi
done

# Subir o Ollama em screen separado
echo "🐳 Subindo Ollama no screen '$OLLAMA_SESSION'..."
screen -dmS "$OLLAMA_SESSION" bash -c "
    ollama serve
"

# Aguarda Ollama subir
echo "⏳ Aguardando Ollama iniciar..."
sleep 5

# Subir a API no outro screen
echo "🔧 Subindo API no screen '$API_SESSION'..."
screen -dmS "$API_SESSION" bash -c "
    source venv/bin/activate
    echo '🔪 Matando processos na porta 9000...'
    if command -v fuser &> /dev/null; then
        fuser -k 9000/tcp
    else
        lsof -ti tcp:9000 | xargs kill -9
    fi
    uvicorn app.main:app --host 0.0.0.0 --port 9000 --proxy-headers --forwarded-allow-ips '*' --reload
"

echo "✅ Tudo rodando!"
echo "👉 API logs:    screen -r $API_SESSION"
echo "👉 Ollama logs: screen -r $OLLAMA_SESSION"