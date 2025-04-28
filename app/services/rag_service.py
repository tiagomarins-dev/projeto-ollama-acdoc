# app/services/rag_service.py
from app.models.agent_model import Agent
import os
import json
import requests
from sentence_transformers import SentenceTransformer, util
from app.services.index_service import criar_index, buscar_no_index

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

    # Novo trecho: buscar contexto pelo índice
    index_path = f"docs/{perfil}/index.pkl"
    if not os.path.exists(index_path):
        return {"error": "Perfil ainda não indexado."}

    with open(index_path, "rb") as f:
        index = pickle.load(f)

    # Realiza a busca semântica
    question_embedding = model_embedder.encode(pergunta, convert_to_tensor=True)
    hits = util.semantic_search(question_embedding, index["embeddings"], top_k=5)
    hits = hits[0]  # semantic_search retorna uma lista dentro de uma lista

    trechos_relevantes = [index["texts"][hit["corpus_id"]] for hit in hits]
    contexto = "\n\n".join(trechos_relevantes)

    instrucoes = agente.instrucoes if isinstance(agente, Agent) else agente.get("instrucoes", "")

    prompt_completo = f"{instrucoes}\n\nContexto:\n{contexto}\n\nPergunta:\n{pergunta}"

    resposta = chamar_modelo(prompt_completo, modelo=modelo, tokens=tokens, stream=stream)

    return resposta

# Função para criar índices de documentos de um perfil (manual ou após upload)

def criar_index_para_perfil(perfil):
    criar_index(perfil)