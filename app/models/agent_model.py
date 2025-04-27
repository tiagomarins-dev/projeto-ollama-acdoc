from pydantic import BaseModel

class Agent(BaseModel):
    perfil: str
    instrucoes: str