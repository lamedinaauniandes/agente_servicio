from app_agent.utils.nodes.nodes import (
    MessageGraph,
    reasoning_node, 
    tool_node, 
    debe_investigar,
)
from langgraph.graph import StateGraph,START,END

TOOL_NODE = "tool_node"
REASONING_NODE = "reasoning_node"

state_machine = StateGraph(MessageGraph)

state_machine.add_node(REASONING_NODE,reasoning_node)
state_machine.add_node(TOOL_NODE,tool_node)

state_machine.add_edge(START,REASONING_NODE)

state_machine.add_conditional_edges(
    REASONING_NODE,
    debe_investigar,
    [END,TOOL_NODE]
)

state_machine.add_edge(TOOL_NODE,REASONING_NODE)

if __name__=="__main__":
    print("testing agent ...")
    from langchain_core.messages import HumanMessage
    agent = state_machine.compile()
    response = agent.invoke({
        "messages":HumanMessage(content="Cuanto es el tiempo de respuesta para incidencias criticas?")
    })

    print(response)