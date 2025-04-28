# app/services/index_service.py

import os
import json
from sentence_transformers import SentenceTransformer, util

# Carregar modelo de embeddings
model_embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Estrutura de index simples (em memória)
indexes = {}

# Funções auxiliares para embeddings
def gerar_embedding(texto: str):
    return model_embedder.encode(texto, convert_to_tensor=True)

# Criar ou atualizar o índice de um perfil
def criar_index(perfil: str):
    dir_path = f"docs/{perfil}"
    if not os.path.exists(dir_path):
        return {"error": "Perfil de documentos não encontrado."}

    documentos = []
    embeddings = []

    for file_name in os.listdir(dir_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(dir_path, file_name), "r") as f:
                conteudo = f.read()
                documentos.append(conteudo)
                embeddings.append(gerar_embedding(conteudo))

    indexes[perfil] = {
        "documentos": documentos,
        "embeddings": embeddings
    }

    return {"message": f"Index criado para o perfil {perfil}."}

# Buscar resposta baseada em similaridade de embeddings
def buscar_no_index(perfil: str, pergunta: str):
    if perfil not in indexes:
        return {"error": "Perfil ainda não indexado."}

    pergunta_embedding = gerar_embedding(pergunta)
    documentos = indexes[perfil]["documentos"]
    embeddings = indexes[perfil]["embeddings"]

    # Calcular similaridade
    scores = util.cos_sim(pergunta_embedding, embeddings)[0]
    melhor_indice = scores.argmax().item()

    return documentos[melhor_indice]
