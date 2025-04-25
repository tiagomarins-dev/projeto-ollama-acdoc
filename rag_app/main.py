from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests
import faiss
import numpy as np
import os
import glob

app = FastAPI()

DIM = 768  # Dimensão dos embeddings do nomic-embed-text
index = faiss.IndexFlatL2(DIM)
documents = []
embeddings = []

class QueryRequest(BaseModel):
    pergunta: str

def carregar_documentos():
    arquivos = glob.glob("/docs/*.txt")
    for arquivo in arquivos:
        with open(arquivo, "r", encoding="utf-8") as f:
            texto = f.read()
            documents.append(texto)
            emb_response = requests.post(
                "http://ollama:11434/api/embeddings",
                json={
                    "model": "nomic-embed-text",
                    "prompt": texto
                }
            )
            emb = np.array(emb_response.json()["embedding"]).astype('float32')
            embeddings.append(emb)
    index.add(np.array(embeddings).astype('float32'))

@app.on_event("startup")
def iniciar():
    carregar_documentos()

@app.post("/rag")
def responder_rag(req: QueryRequest, modelo: str = Query("mistral")):
    pergunta = req.pergunta
    pergunta_emb_response = requests.post(
        "http://ollama:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": pergunta
        }
    )
    pergunta_emb = np.array(pergunta_emb_response.json()["embedding"]).astype('float32')

    D, I = index.search(np.array([pergunta_emb]), k=1)
    trecho = documents[I[0][0]]

    prompt = f"""Use o contexto abaixo para responder a pergunta:

Contexto:
{trecho}

Pergunta: {pergunta}
"""

    resposta = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": modelo,
            "prompt": prompt,
            "stream": False
        }
    )
    return resposta.json()