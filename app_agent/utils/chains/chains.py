import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_ollama import ChatOllama
from app_agent.utils.chains.templates import (
    agent_role,
    agent_template,
)
from app_agent.utils.tools.tool_rag import (
    retrieve_docs_acuerdos_servicios,
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.output_parsers.openai_tools import PydanticToolsParser

path_directory = Path(os.getcwd())
path_env = os.path.join(path_directory, ".env")
load_dotenv(override=True, dotenv_path=path_env)


class Respuesta(BaseModel): 
    respuesta: str = Field(description="respuesta al usuario")
    fuentes: list[str] = Field(description="documentos recuperados")

parser_pydantic_response = PydanticToolsParser(tools=[Respuesta])

print("debug 1 \n",os.getenv("OLLAMA_MODEL_LLM"),"\n",path_env)

llm = ChatOllama(model=os.getenv("OLLAMA_MODEL_LLM"))

agent_reasoning_prompt = ChatPromptTemplate.from_messages([
    ("system", agent_template),
    MessagesPlaceholder(variable_name="messages"),
]).partial(role=agent_role)

agent_reasoning_chain = agent_reasoning_prompt | llm.bind_tools(
    tools=[Respuesta,retrieve_docs_acuerdos_servicios],
)

if __name__ == "__main__": 
    print("testingn")