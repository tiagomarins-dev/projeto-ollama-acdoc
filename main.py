from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/gerar")
def gerar_texto(
    req: PromptRequest,
    modelo: str = Query("mistral"),
    tokens: int = Query(300)  # Novo parâmetro 'tokens' na query string
):
    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": modelo,
            "prompt": req.prompt,
            "stream": False,
            "num_predict": tokens   # Usando o valor de tokens recebido
        }
    )
    return response.json()



