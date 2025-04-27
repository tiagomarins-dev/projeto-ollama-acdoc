import requests
from app.models.prompt_request import PromptRequest

def gerar(req: PromptRequest, modelo: str, tokens: int):
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