from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/gerar")
def gerar_texto(req: PromptRequest, modelo: str = Query("mistral"), tokens: int = Query(300)):
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": modelo,
            "prompt": req.prompt,
            "stream": False,
            "num_predict": tokens
        }
    )
    return response.json()



