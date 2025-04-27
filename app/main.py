from fastapi import FastAPI, UploadFile, File
from app.services.agent_service import salvar_agente, carregar_agente
from app.services.rag_service import buscar_resposta, criar_index
from app.services.ollama_service import gerar_texto
from app.models.prompt_request import PromptRequest
from app.models.agent_model import Agent
import os

app = FastAPI()

@app.post("/upload/{perfil}")
async def upload_documento(perfil: str, file: UploadFile = File(...)):
    dir_path = f"docs/{perfil}"
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    criar_index(perfil)
    return {"message": f"Arquivo {file.filename} salvo no perfil {perfil}."}

@app.post("/agent")
def cadastrar_agente(agent: Agent):
    salvar_agente(agent.perfil, agent.instrucoes)
    return {"message": f"Agente {agent.perfil} salvo com sucesso."}

@app.get("/agent/{perfil}")
def consultar_agente(perfil: str):
    agent = carregar_agente(perfil)
    if not agent:
        return {"error": "Perfil não encontrado."}
    return agent

@app.post("/rag/{perfil}")
def usar_rag(perfil: str, req: PromptRequest, tokens: int = 300, modelo: str = "mistral"):
    resposta = buscar_resposta(perfil, req.prompt, modelo=modelo, tokens=tokens)
    return {"resposta": resposta}

@app.post("/gerar")
def gerar(req: PromptRequest, modelo: str = "mistral", tokens: int = 100):
    return gerar_texto(req, modelo, tokens)

@app.post("/reindexar/{perfil}")
def reindexar(perfil: str):
    criar_index(perfil)
    return {"message": f"Índice do perfil {perfil} recriado com sucesso."}