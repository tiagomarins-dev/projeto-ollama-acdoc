# services/rag_service.py

import os
import numpy as np
import faiss
from services.ollama_service import gerar_texto
from models.prompt_request import PromptRequest

# Inicializa o índice FAISS
INDEX = None
DOCUMENTOS = []

def carregar_documentos():
    global INDEX, DOCUMENTOS
    DOCUMENTOS = []
    docs_dir = "docs"

    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    arquivos = [f for f in os.listdir(docs_dir) if f.endswith(".txt")]
    vetores = []

    for arquivo in arquivos:
        caminho = os.path.join(docs_dir, arquivo)
        with open(caminho, "r", encoding="utf-8") as file:
            conteudo = file.read()
            DOCUMENTOS.append(conteudo)
            emb_response = gerar_texto(PromptRequest(prompt=conteudo), modelo="nomic-embed-text", embed=True)
            vetor = np.array(emb_response["embedding"], dtype='float32')
            vetores.append(vetor)

    if vetores:
        dim = vetores[0].shape[0]
        INDEX = faiss.IndexFlatL2(dim)
        INDEX.add(np.array(vetores))

def buscar_documentos(query: str, k: int = 1):
    if INDEX is None:
        raise Exception("Índice FAISS não carregado.")

    emb_response = gerar_texto(PromptRequest(prompt=query), modelo="nomic-embed-text", embed=True)
    vetor_query = np.array(emb_response["embedding"], dtype='float32').reshape(1, -1)

    distancias, indices = INDEX.search(vetor_query, k)
    resultados = []

    for idx in indices[0]:
        if idx < len(DOCUMENTOS):
            resultados.append(DOCUMENTOS[idx])

    return resultados

def responder_pergunta(req: PromptRequest):
    documentos_encontrados = buscar_documentos(req.prompt, k=1)
    contexto = "\n\n".join(documentos_encontrados)
    prompt_final = f"Com base no seguinte contexto, responda a pergunta:\n\n{contexto}\n\nPergunta: {req.prompt}"
    resposta = gerar_texto(PromptRequest(prompt=prompt_final), modelo="mistral")
    return resposta