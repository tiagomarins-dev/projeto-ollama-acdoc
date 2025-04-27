#!/bin/bash

# Ativa o ambiente virtual
source venv/bin/activate

# Mata qualquer processo travado na porta 9000
echo "Matando processos na porta 9000..."
fuser -k 9000/tcp

# Sobe o servidor FastAPI
echo "Subindo servidor Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port 9000 --proxy-headers --forwarded-allow-ips '*' --reload