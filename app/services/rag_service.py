# app/services/rag_service.py
from app.models.agent_model import Agent
from app.services.index_service import criar_index, buscar_contexto
import os
import json
import requests

# Funções auxiliares para agentes
def carregar_agente(perfil: str) -> Agent:
    caminho = f"agents/{perfil}.json"
    if not os.path.exists(caminho):
        return None
    with open(caminho, "r") as f:
        data = json.load(f)
        return Agent(**data)

def carregar_todos_arquivos(perfil: str, max_tokens: int = 5000):
    dir_path = f"docs/{perfil}"
    contexto = ""
    if os.path.exists(dir_path):
        for file_name in os.listdir(dir_path):
            if file_name.endswith(".txt"):
                with open(os.path.join(dir_path, file_name), "r") as f:
                    texto = f.read()
                    contexto += texto + "\n\n"
    # Corta o contexto se ultrapassar max_tokens caracteres aproximados
    if len(contexto.split()) > max_tokens:
        contexto = " ".join(contexto.split()[:max_tokens])
    return contexto.strip()

# Função para chamar o modelo Ollama
def chamar_modelo(prompt_completo, modelo="mistral", tokens=300, stream=False):
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": modelo,
            "prompt": prompt_completo,
            "stream": stream,
            "num_predict": tokens
        },
        stream=stream  # importante: stream=True no requests também
    )
    response.raise_for_status()

    if stream:
        resposta = ""
        for linha in response.iter_lines():
            if linha:
                parte = json.loads(linha.decode("utf-8"))
                resposta += parte.get("response", "")
        return resposta
    else:
        data = response.json()
        return data.get("response", "")

# Função principal de busca de resposta
def buscar_resposta(perfil: str, pergunta: str, modelo: str = "mistral", tokens: int = 300, stream: bool = False, embeddings: bool = True):
    agente = carregar_agente(perfil)
    if not agente:
        return {"error": "Perfil não encontrado."}

    if embeddings:
        contexto = buscar_contexto(perfil, pergunta)
        if not contexto:
            return {"error": "Perfil ainda não indexado."}
    else:
        contexto = carregar_todos_arquivos(perfil)
        if not contexto:
            return {"error": "Nenhum conteúdo encontrado para este perfil."}

    instrucoes = agente.instrucoes if hasattr(agente, "instrucoes") else ""

    prompt_completo = f"{instrucoes}\n\nContexto:\n{contexto}\n\nPergunta:\n{pergunta}"

    resposta = chamar_modelo(prompt_completo, modelo=modelo, tokens=tokens, stream=stream)

    return resposta