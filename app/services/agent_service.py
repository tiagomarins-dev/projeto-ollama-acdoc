import json
import os

AGENTS_DIR = "agents"

def salvar_agente(perfil: str, instrucoes: str):
    if not os.path.exists(AGENTS_DIR):
        os.makedirs(AGENTS_DIR)
    with open(f"{AGENTS_DIR}/{perfil}.json", "w", encoding="utf-8") as f:
        json.dump({"perfil": perfil, "instrucoes": instrucoes}, f)

def carregar_agente(perfil: str):
    try:
        with open(f"{AGENTS_DIR}/{perfil}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None