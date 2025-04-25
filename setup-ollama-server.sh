#!/bin/bash

echo "🚀 Atualizando sistema..."
apt update && apt upgrade -y

echo "🐳 Instalando Docker e Docker Compose..."
apt install -y docker.io docker-compose curl git

echo "🔧 Habilitando e iniciando Docker..."
systemctl enable docker
systemctl start docker

echo "📥 Instalando Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo "📦 Puxando modelos do Ollama..."
ollama pull mistral
ollama pull llama2
ollama pull deepseek-chat

echo "📁 Criando diretório do projeto..."
mkdir -p /opt/projeto-ollama-acdoc
cd /opt/projeto-ollama-acdoc

echo "📥 Clonando repositório da API..."
git clone https://github.com/tiagomarins-dev/projeto-ollama-acdoc.git .

echo "🔨 Subindo containers com Docker Compose..."
docker-compose up -d

echo "✅ Setup concluído com sucesso!"
