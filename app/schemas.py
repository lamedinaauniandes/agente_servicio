from pydantic import BaseModel,Field


class ChatRequest(BaseModel): 
    pregunta: str =  Field(...,min_length=1)


class ChatResponse(BaseModel):
    respuesta: str
    fuentes: list[str]
    tiempo_ms: int
