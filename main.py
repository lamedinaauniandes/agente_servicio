from fastapi import (
    FastAPI,
)
import uvicorn
from app_agent.agent import (
    state_machine,
)
from langchain_core.messages import HumanMessage,ToolMessage
from app.routers import chat

app = FastAPI()

app.include_router(chat.router)

@app.get("/health")
def healt():
    return {"message":"hola mundo, estoy saludable"}

if __name__=="__main__":
    uvicorn.run("main:app",port=8000,reload=True)