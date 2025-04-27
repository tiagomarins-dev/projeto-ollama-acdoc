#!/bin/bash

echo "🚀 Atualizando sistema..."
apt update && apt upgrade -y

echo "🐙 Instalando dependências básicas (git, Python, venv)..."
apt install -y git python3 python3-pip python3.8-venv curl

echo "📁 Criando diretórios do projeto..."
mkdir -p /home/projetos
cd /home/projetos

echo "📥 Clonando repositório do projeto..."
git clone https://github.com/tiagomarins-dev/projeto-ollama-acdoc.git
cd projeto-ollama-acdoc

echo "🐍 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

echo "⬆️ Atualizando pip e instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt
pip install fastapi uvicorn requests numpy

echo "📥 Instalando Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo "✅ Setup concluído! Ambiente pronto para rodar o servidor."
echo "👉 Para iniciar o servidor, execute:"
echo "source venv/bin/activate && ./start.sh"