#!/bin/bash

echo "Instalando os modelos mais populares no Ollama..."
ollama pull mistral
# ollama pull llama2
# ollama pull llama3
ollama pull llama3:8b
ollama pull llama3:70b
ollama pull deepseek-coder
ollama pull deepseek-r1:7b
ollama pull deepseek-r1:14b
# ollama pull gemma:2b
# ollama pull gemma3
ollama pull phi
ollama pull phi4
ollama pull phi3
ollama pull phi3.5
#ollama pull qwen2.5:7b
#ollama pull qwen2.5:14b
#ollama pull qwen2.5-coder:7b
#ollama pull mixtral:8x7b
#ollama pull mixtral:8x22b
ollama pull dolphin-llama3:8b
ollama pull starcoder2:7b
ollama pull codellama:7b
ollama pull command-r
#ollama pull wizardlm2:7b
ollama pull tinyllama
echo "Todos os modelos foram baixados com sucesso!"
