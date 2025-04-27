from fastapi import FastAPI
from app.ollama_service import gerar_texto
from app.rag_service import consultar_documento

app = FastAPI()

@app.post("/gerar")
def gerar(req: gerar_texto.PromptRequest, modelo: str = "mistral", tokens: int = 200):
    return gerar_texto.gerar(req, modelo, tokens)

@app.post("/rag")
def rag(req: consultar_documento.RagRequest):
    return consultar_documento.rag(req)