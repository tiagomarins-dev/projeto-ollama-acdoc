# app/services/index_service.py

import os
import pickle
from sentence_transformers import SentenceTransformer, util

# Carrega o modelo de embeddings uma vez
model_embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Cria o index.pkl para o perfil
def criar_index(perfil: str):
    dir_path = f"docs/{perfil}"
    if not os.path.exists(dir_path):
        return {"error": "Diretório de documentos não encontrado."}

    textos = []
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(dir_path, file_name), "r") as f:
                textos.append(f.read())

    if not textos:
        return {"error": "Nenhum documento .txt encontrado para indexar."}

    embeddings = model_embedder.encode(textos, convert_to_tensor=True)

    index_data = {
        "textos": textos,
        "embeddings": embeddings
    }

    with open(os.path.join(dir_path, "index.pkl"), "wb") as f:
        pickle.dump(index_data, f)

    return {"message": f"Index criado para o perfil {perfil}."}

# Busca o melhor contexto para uma pergunta
def buscar_contexto(perfil: str, pergunta: str, k: int = 3):
    index_path = f"docs/{perfil}/index.pkl"

    if not os.path.exists(index_path):
        return None

    with open(index_path, "rb") as f:
        index_data = pickle.load(f)

    textos = index_data["textos"]
    embeddings = index_data["embeddings"]

    pergunta_embedded = model_embedder.encode(pergunta, convert_to_tensor=True)

    hits = util.semantic_search(pergunta_embedded, embeddings, top_k=k)

    melhores_trechos = [textos[hit["corpus_id"]] for hit in hits[0]]

    return "\n\n".join(melhores_trechos)