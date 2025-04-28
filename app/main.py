from fastapi import FastAPI, UploadFile, File
from fastapi import Query
from app.services.agent_service import salvar_agente, carregar_agente
from app.services.rag_service import buscar_resposta
from app.services.index_service import criar_index
from app.services.ollama_service import gerar_texto
from app.models.prompt_request import PromptRequest
from app.models.agent_model import Agent
import os

app = FastAPI()

@app.post("/upload/{perfil}")
async def upload_documento(perfil: str, file: UploadFile = File(...)):
    try:
        dir_path = f"docs/{perfil}"
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        result = criar_index(perfil)
        return {"message": f"Arquivo {file.filename} salvo no perfil {perfil}.", "index_result": result}
    except Exception as e:
        return {"error": f"Erro ao processar upload: {str(e)}"}

@app.post("/agent")
def cadastrar_agente(agent: Agent):
    try:
        os.makedirs("agents", exist_ok=True)
        result = salvar_agente(agent.perfil, agent.instrucoes)
        return {"message": f"Agente {agent.perfil} salvo com sucesso.", "result": result}
    except Exception as e:
        return {"error": f"Erro ao cadastrar agente: {str(e)}"}

@app.get("/agent/{perfil}")
def consultar_agente(perfil: str):
    agent = carregar_agente(perfil)
    if not agent:
        return {"error": "Perfil não encontrado."}
    return agent

@app.post("/rag/{perfil}")
def usar_rag(
    perfil: str,
    req: PromptRequest,
    modelo: str = "mistral",
    tokens: int = 300,
    stream: bool = False,
    embeddings: bool = Query(True)
):
    try:
        resposta = buscar_resposta(
            perfil,
            req.prompt,
            modelo=modelo,
            tokens=tokens,
            stream=stream,
            embeddings=embeddings
        )
        return {"resposta": resposta}
    except Exception as e:
        return {"error": f"Erro na busca RAG: {str(e)}"}

@app.post("/gerar")
def gerar(req: PromptRequest, modelo: str = "mistral", tokens: int = 300):
    return gerar_texto(req, modelo, tokens)

@app.get("/agents")
def listar_agentes():
    agentes = []
    try:
        os.makedirs("agents", exist_ok=True)
        for file_name in os.listdir("agents"):
            if file_name.endswith(".json"):
                agentes.append(file_name.replace(".json", ""))
        return {"agentes": agentes}
    except Exception as e:
        return {"error": f"Erro ao listar agentes: {str(e)}", "agentes": []}