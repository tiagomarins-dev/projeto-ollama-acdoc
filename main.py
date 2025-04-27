from fastapi import FastAPI
from services.ollama_service import gerar_texto
from services.rag_service import responder_pergunta
from models.prompt_request import PromptRequest

app = FastAPI()

@app.post("/gerar")
def gerar(req: PromptRequest, modelo: str = "mistral", tokens: int = 100):
    return gerar_texto(req, modelo, tokens)

@app.post("/rag")
def rag(req: PromptRequest):
    return responder_pergunta(req)