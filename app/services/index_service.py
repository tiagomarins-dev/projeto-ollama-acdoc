# app/services/index_service.py

import os
import pickle
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Carrega o modelo de embeddings uma vez
model_embedder = None
try:
    model_embedder = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Erro ao carregar modelo de embeddings: {e}")

# Cria o index.pkl para o perfil
def criar_index(perfil: str):
    dir_path = f"docs/{perfil}"
    if not os.path.exists(dir_path):
        return {"error": "Diretório de documentos não encontrado."}

    if model_embedder is None:
        return {"error": "Modelo de embeddings não disponível."}

    textos = []
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".txt"):
            try:
                with open(os.path.join(dir_path, file_name), "r") as f:
                    textos.append(f.read())
            except Exception as e:
                print(f"Erro ao ler arquivo {file_name}: {e}")

    if not textos:
        return {"error": "Nenhum documento .txt encontrado para indexar."}

    try:
        # Converter para numpy array para melhor serialização
        embeddings = model_embedder.encode(textos, convert_to_tensor=False)
        
        index_data = {
            "textos": textos,
            "embeddings": embeddings
        }

        with open(os.path.join(dir_path, "index.pkl"), "wb") as f:
            pickle.dump(index_data, f)

        return {"message": f"Index criado para o perfil {perfil}."}
    except Exception as e:
        print(f"Erro ao criar index: {e}")
        return {"error": f"Falha ao criar index: {str(e)}"}

# Busca o melhor contexto para uma pergunta
def buscar_contexto(perfil: str, pergunta: str, k: int = 3, threshold: float = 0.3):
    index_path = f"docs/{perfil}/index.pkl"

    if not os.path.exists(index_path):
        print(f"Index não encontrado para o perfil {perfil}")
        return None

    if model_embedder is None:
        print("Modelo de embeddings não disponível")
        return None

    try:
        with open(index_path, "rb") as f:
            index_data = pickle.load(f)

        textos = index_data["textos"]
        embeddings = index_data["embeddings"]

        if len(textos) == 0:
            print("Nenhum texto encontrado no index")
            return None

        # Converter para numpy array se não for
        if isinstance(embeddings, list):
            embeddings = np.array(embeddings)

        pergunta_embedded = model_embedder.encode(pergunta, convert_to_tensor=False)
        
        hits = util.semantic_search(pergunta_embedded, embeddings, top_k=k)
        
        if not hits or not hits[0]:
            print("Nenhum resultado encontrado na busca semântica")
            return None
            
        # Filtrar por threshold de similaridade
        filtered_hits = [hit for hit in hits[0] if hit["score"] >= threshold]
        
        if not filtered_hits:
            print(f"Nenhum resultado com similaridade acima de {threshold}")
            return "\n\n".join(textos[:1])  # Retorna pelo menos o primeiro texto

        melhores_trechos = [textos[hit["corpus_id"]] for hit in filtered_hits]
        
        return "\n\n".join(melhores_trechos)
    except Exception as e:
        print(f"Erro ao buscar contexto: {e}")
        return None