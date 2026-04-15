from app_agent.utils.chains.chains import (
    agent_reasoning_chain,
)
from app_agent.utils.tools.tool_rag import (
 retrieve_docs_acuerdos_servicios   
)


from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,ToolMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode 
from langgraph.graph import END

#### la clase MessageGraph es el estado del grafo o máquina de estados 
class MessageGraph(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]


def reasoning_node(state:MessageGraph): 
    """
    Nodo de razonamiento para el agente, toma la
    desición si investigar o responder
    """
    print("-"*50,"reasoning_node 2")
    
    response = agent_reasoning_chain.invoke({
        "messages":state["messages"]
    })
    print(response)
    return {"messages":[response]}

def debe_investigar(state:MessageGraph):
     print("-"*50,"debe investigar")
     if state["messages"][-1].tool_calls: 
          print("redirigiendo tool node ...")
          return "tool_node"
     print("redirigiendo end ...")
     return END


tool_node = ToolNode([retrieve_docs_acuerdos_servicios])