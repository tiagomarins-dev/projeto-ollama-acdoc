#!/bin/bash

# Nome da sessão do screen
SESSION_NAME="minhaapi"

# Ativa o ambiente virtual e sobe o servidor dentro do screen
echo "Iniciando servidor no screen '$SESSION_NAME'..."

# Se já existir uma sessão com esse nome, mata ela primeiro
if screen -list | grep -q "$SESSION_NAME"; then
    echo "Sessão existente encontrada. Matando..."
    screen -S "$SESSION_NAME" -X quit
fi

# Cria nova sessão de screen rodando os comandos
screen -dmS "$SESSION_NAME" bash -c "
    source venv/bin/activate
    echo 'Matando processos na porta 9000...'
    if command -v fuser &> /dev/null; then
        fuser -k 9000/tcp
    else
        lsof -ti tcp:9000 | xargs kill -9
    fi
    echo 'Iniciando Ollama...'
    ollama serve &
    sleep 5
    echo 'Subindo servidor Uvicorn...'
    uvicorn app.main:app --host 0.0.0.0 --port 9000 --proxy-headers --forwarded-allow-ips '*' --reload
"

echo "Servidor iniciado dentro do screen '$SESSION_NAME'."
echo "Use 'screen -r $SESSION_NAME' para ver os logs."