import os
import faiss
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from app.services.ollama_service import gerar_texto
from app.models.prompt_request import PromptRequest
from app.services.agent_service import carregar_agente

# Embeddings model
model_embedding = SentenceTransformer('all-MiniLM-L6-v2')

# Cache de índices carregados por agente
cache_indices = {}

def carregar_documentos(perfil: str) -> List[str]:
    """Carrega documentos do perfil"""
    path = f"docs/{perfil}"
    textos = []
    if not os.path.exists(path):
        return textos
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
                textos.append(f.read())
    return textos

def criar_index(perfil: str):
    """Cria ou carrega o índice FAISS do perfil"""
    if perfil in cache_indices:
        return cache_indices[perfil]
    
    textos = carregar_documentos(perfil)
    if not textos:
        raise ValueError(f"Nenhum documento encontrado para o perfil {perfil}.")
    
    embeddings = model_embedding.encode(textos)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings, dtype='float32'))
    
    cache_indices[perfil] = (index, textos)
    return index, textos


def buscar_resposta(perfil: str, pergunta: str, modelo: str = "mistral"):
    # Carrega o agente e as instruções
    agent = carregar_agente(perfil)
    instrucoes = agent.instrucoes if agent else ""

    # Carrega o índice FAISS e textos
    if perfil not in cache_indices:
        criar_index(perfil)
    index, textos = cache_indices[perfil]

    # Vetoriza a pergunta
    pergunta_embedding = model_embedding.encode([pergunta])
    
    # Busca o contexto mais próximo
    D, I = index.search(np.array(pergunta_embedding, dtype='float32'), k=1)
    contexto = textos[I[0][0]] if I[0][0] != -1 else ""

    # Monta o prompt completo
    prompt_completo = f"{instrucoes}\n\nContexto:\n{contexto}\n\nPergunta:\n{pergunta}"

    # Chama o modelo especificado
    resposta = chamar_modelo(prompt_completo, modelo=modelo)
    
    return resposta

def chamar_modelo(prompt: str, modelo: str = "mistral"):
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": modelo,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

