from time import perf_counter

from app.schemas import (
    ChatRequest,
    ChatResponse    
)

from fastapi import (
    APIRouter,
    status,
    HTTPException,
)
from fastapi.concurrency import run_in_threadpool
from app_agent.agent import state_machine
from langchain_core.messages import HumanMessage, ToolMessage

router = APIRouter(
    prefix="/consultar",
    tags=["consultar"]
)

agent = None

@router.on_event("startup")
def startup():
    global agent
    agent = state_machine.compile()


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def consulta(request: ChatRequest):
    try:
        pregunta_user = request.pregunta.strip()

        inicio = perf_counter()

        res = await run_in_threadpool(
            agent.invoke,
            {"messages": [HumanMessage(content=pregunta_user)]}
        )

        fin = perf_counter()
        tiempo_ms = int((fin - inicio) * 1000)

        messages = res["messages"]
        respuesta_agente = getattr(messages[-1], "content", None)

        fuentes_rag = []
        for msg in messages:
            if isinstance(msg, ToolMessage):
                if msg.artifact:
                    for doc in msg.artifact:
                        fuentes_rag.append(doc.page_content)

        return ChatResponse(
            respuesta=respuesta_agente,
            fuentes=fuentes_rag,
            tiempo_ms=tiempo_ms
        )

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"un fallo en la llamada del agent {ex}"
        )