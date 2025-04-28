# app/services/rag_service.py
from app.models.agent_model import Agent
import os
import json
import requests
from sentence_transformers import SentenceTransformer, util

# Carregar modelo de embeddings
model_embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Funções auxiliares para agentes
def carregar_agente(perfil: str) -> Agent:
    caminho = f"agents/{perfil}.json"
    if not os.path.exists(caminho):
        return None
    with open(caminho, "r") as f:
        data = json.load(f)
        return Agent(**data)  # 👈 monta um Agent de verdade

# Funções auxiliares para contexto

def carregar_contexto(perfil):
    dir_path = f"docs/{perfil}"
    contexto = []
    if os.path.exists(dir_path):
        for file_name in os.listdir(dir_path):
            if file_name.endswith(".txt") and file_name != "agent.json":
                with open(os.path.join(dir_path, file_name), "r") as f:
                    contexto.append(f.read())
    return "\n".join(contexto)

# Função para chamar o modelo Ollama
def chamar_modelo(prompt_completo, modelo="mistral", tokens=300, stream=False):
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": modelo,
            "prompt": prompt_completo,
            "stream": stream,
            "num_predict": tokens
        }
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", "")

# Função principal de busca de resposta

def buscar_resposta(perfil: str, pergunta: str, modelo: str = "mistral", tokens: int = 300, stream: bool = False):
    agente = carregar_agente(perfil)
    if not agente:
        return {"error": "Perfil não encontrado."}

    contexto = carregar_contexto(perfil)
    if not contexto:
        return {"error": "Nenhum contexto encontrado para este perfil."}

    instrucoes = agente.get("instrucoes", "")

    prompt_completo = f"{instrucoes}\n\nContexto:\n{contexto}\n\nPergunta:\n{pergunta}"

    resposta = chamar_modelo(prompt_completo, modelo=modelo, tokens=tokens, stream=stream)

    return resposta

# Opcional: futura criação de embeddings

def criar_index(perfil):
    # Implementar aqui se quiser gerar embeddings dos documentos (opcional)
    pass
