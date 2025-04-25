from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/gerar")
def gerar_texto(req: PromptRequest, modelo: str = Query("mistral")):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": modelo,
            "prompt": req.prompt,
            "stream": False
        }
    )
    return response.json()