#!/bin/bash
echo "Iniciando API..."
cd /home/projetos/projeto-ollama-acdoc
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 9000 --proxy-headers --forwarded-allow-ips '*'