# app/services/rag_service.py
from app.models.agent_model import Agent
from app.services.index_service import buscar_contexto
import os
import json
import requests

# Funções auxiliares para agentes
def carregar_agente(perfil: str) -> Agent:
    caminho = f"agents/{perfil}.json"
    if not os.path.exists(caminho):
        return None
    try:
        with open(caminho, "r") as f:
            data = json.load(f)
            return Agent(**data)
    except Exception as e:
        print(f"Erro ao carregar agente {perfil}: {e}")
        return None

def carregar_todos_arquivos(perfil: str, max_tokens: int = 5000):
    dir_path = f"docs/{perfil}"
    contexto = ""
    if os.path.exists(dir_path):
        for file_name in os.listdir(dir_path):
            if file_name.endswith(".txt"):
                try:
                    with open(os.path.join(dir_path, file_name), "r") as f:
                        texto = f.read()
                        contexto += texto + "\n\n"
                except Exception as e:
                    print(f"Erro ao ler arquivo {file_name}: {e}")
    if len(contexto.split()) > max_tokens:
        contexto = " ".join(contexto.split()[:max_tokens])
    return contexto.strip()

# Função para chamar o modelo Ollama
def chamar_modelo(prompt_completo, modelo="mistral", tokens=300, stream=False):
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": modelo,
                "prompt": prompt_completo,
                "stream": stream,
                "num_predict": tokens
            },
            stream=stream,
            timeout=60  # Adicionar timeout para evitar espera infinita
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
    except Exception as e:
        print(f"Erro ao chamar modelo: {e}")
        return f"Erro ao gerar resposta: {str(e)}"

# Função principal de busca de resposta
def buscar_resposta(
    perfil: str,
    pergunta: str,
    modelo: str = "mistral",
    tokens: int = 300,
    stream: bool = False,
    embeddings: bool = True
):
    try:
        # Verificar se o agente existe
        agente = carregar_agente(perfil)
        if not agente:
            return {"error": "Perfil não encontrado."}

        # Buscar contexto por embeddings ou texto completo
        contexto = None
        if embeddings:
            contexto = buscar_contexto(perfil, pergunta)
            
        # Fallback para texto completo se embeddings falhar
        if contexto is None:
            print(f"Fallback para texto completo para o perfil {perfil}")
            contexto = carregar_todos_arquivos(perfil)
            if not contexto:
                return {"error": "Nenhum conteúdo encontrado para este perfil."}

        # Obter instruções do agente
        instrucoes = agente.instrucoes if hasattr(agente, "instrucoes") else ""

        # Montar prompt completo
        prompt_completo = f"{instrucoes}\n\nContexto:\n{contexto}\n\nPergunta:\n{pergunta}"

        # Chamar o modelo
        resposta = chamar_modelo(prompt_completo, modelo=modelo, tokens=tokens, stream=stream)

        # Retornar resposta estruturada
        return {
            "instrucoes": instrucoes,
            "contexto_usado": contexto,
            "prompt_usuario": pergunta,
            "prompt_final_enviado": prompt_completo,
            "resposta": resposta
        }
    except Exception as e:
        print(f"Erro em buscar_resposta: {e}")
        return {"error": f"Erro ao processar requisição: {str(e)}"}