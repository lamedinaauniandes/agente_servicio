import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

path_directory = Path(os.getcwd())

path_env = os.path.join(path_directory,".env")
load_dotenv(override=True,dotenv_path=path_env)

embeddings = OllamaEmbeddings(model="embeddinggemma")

persist_directory = os.path.join(path_directory,os.getenv("CHROMA_PERSIST_DIRECTORY"))


vectorstore = Chroma( 
    collection_name = os.getenv("CHROMA_COLLECTION"),
    embedding_function = embeddings, 
    persist_directory=persist_directory,
)


@tool(response_format="content_and_artifact")
def retrieve_docs_acuerdos_servicios(query:str):
    """ 
    Función para la recuperación de documentos para acuerdos de servicio.
    Args: 
        query tipo string pregunta para la recuperación de documentos
    """
    print("-"*50,"tool_node    4")
    try:
        resultados = vectorstore.similarity_search(query,k=int(os.getenv("CRHOMA_K_RETRIEVE")))
    except Exception as exc:
        print(exc)
    print("debug 3 ")
    serialized = "\n\n".join(
        (f"contenido del documento {i}: {doc.page_content} ") for i,doc in enumerate(resultados)
    )
    print("debug 4")

    print("*"*20,resultados)
    return serialized,resultados


if __name__=="__main__":
    print(f"testeando ..., \n path_directory: {path_directory}, \n persist_directory: {persist_directory}")
    query = "cual es el tiempo de respuesta para dos horas?"
    resultados = vectorstore.similarity_search(query,k=1)
    print(resultados)





