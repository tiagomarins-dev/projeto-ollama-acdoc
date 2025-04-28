# app/services/ollama_service.py
import requests
import json

def gerar_texto(prompt_request, modelo="mistral", tokens=300):
    try:
        # URL do Ollama baseado no ambiente (container vs local)
        ollama_url = "http://ollama:11434/api/generate"
        
        # Fallback para URL local se a primeira falhar
        urls_to_try = [ollama_url, "http://127.0.0.1:11434/api/generate"]
        
        last_error = None
        for url in urls_to_try:
            try:
                print(f"Tentando conectar a: {url}")
                resposta = requests.post(
                    url,
                    json={
                        "model": modelo,
                        "prompt": prompt_request.prompt,
                        "num_predict": tokens
                    },
                    timeout=60
                )
                resposta.raise_for_status()
                json_resposta = resposta.json()
                return {"resposta": json_resposta.get("response", "")}
                
            except Exception as e:
                print(f"Erro ao gerar texto em {url}: {e}")
                last_error = e
                continue  # Tenta a próxima URL
        
        # Se chegou aqui, todas as URLs falharam
        return {"error": f"Erro ao gerar texto: {str(last_error)}"}
        
    except Exception as e:
        print(f"Erro geral em gerar_texto: {e}")
        return {"error": f"Erro ao processar requisição: {str(e)}"}