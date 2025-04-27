import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

BASE_DIR = "docs"
EMBEDDINGS = {}

def carregar_documentos(perfil):
    textos = []
    pasta = os.path.join(BASE_DIR, perfil)
    if not os.path.exists(pasta):
        return None
    for filename in os.listdir(pasta):
        path = os.path.join(pasta, filename)
        with open(path, "r", encoding="utf-8") as f:
            textos.append(f.read())
    return textos

def criar_index(perfil):
    textos = carregar_documentos(perfil)
    if not textos:
        return None
    embeddings = model.encode(textos)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    EMBEDDINGS[perfil] = (index, textos)

def buscar_resposta(perfil, pergunta):
    if perfil not in EMBEDDINGS:
        criar_index(perfil)
    if perfil not in EMBEDDINGS:
        return "Perfil não encontrado."
    
    index, textos = EMBEDDINGS[perfil]
    pergunta_emb = model.encode([pergunta])
    D, I = index.search(np.array(pergunta_emb), k=1)
    resposta = textos[I[0][0]]
    return resposta