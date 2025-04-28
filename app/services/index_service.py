# app/services/index_service.py
import os
import pickle
from sentence_transformers import SentenceTransformer

model_embedder = SentenceTransformer('all-MiniLM-L6-v2')

def criar_index(perfil: str):
    dir_path = f"docs/{perfil}"
    textos = []

    if not os.path.exists(dir_path):
        return {"error": "Perfil não encontrado."}

    for file_name in os.listdir(dir_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(dir_path, file_name), "r") as f:
                textos.append(f.read())

    if not textos:
        return {"error": "Nenhum texto encontrado."}

    embeddings = model_embedder.encode(textos, convert_to_tensor=True)

    index = {
        "texts": textos,
        "embeddings": embeddings
    }

    with open(os.path.join(dir_path, "index.pkl"), "wb") as f:
        pickle.dump(index, f)

    return {"message": f"Index criado para o perfil {perfil}."}