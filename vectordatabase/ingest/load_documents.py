from dotenv import load_dotenv
from pathlib import Path
import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document 

path_base_directory = Path(os.getcwd())

path_env = os.path.join(path_base_directory,".env")
load_dotenv(override=True,dotenv_path=path_env)
persist_directory = os.path.join(path_base_directory,os.getenv("CHROMA_PERSIST_DIRECTORY"))

def ingest_embeddigns_chroma(path_document: str,persist_directory:str ) -> bool: 
    """
    Función para insertar los documentos a chroma, usa el modelo OllamaEmbeddings para la representación 
    vectorial del documento 
    
    args: 
      path_document: path al documento a insertar 
    
    """

    try: 
        
        embeddings = OllamaEmbeddings(model=os.getenv("CHROMA_MODEL_EMBEDDINGS")) ### modelo de embeddings

        docs = [] 
        with open(path_document,"r",encoding="utf-8") as f: 
            for line in f: 
                docs.append(Document(page_content=line.strip()))  ### los chuncks los tomo como si fuera cada linea, no necesito una clase como RecursiveCharacterTextSplitter para textos cortos   

        vectorstore = Chroma.from_documents(
            documents = docs,
            embedding= embeddings, 
            collection_name= "acuerdos_nivel_servicio", 
            persist_directory = persist_directory,       ### la memoria queda persistente en disco duro
        )
        return True
    except Exception as ex: 
        raise ValueError(f"Ocurrió un exepción en la ingesta de embeddings en la base de datos vectorial")

if __name__ == "__main__": 
    path_file = r".\docs\CONTRATO_SLA.txt"
    persist_directory = Path("../chroma_db")
    ingest_embeddigns_chroma(path_document=path_file,persist_directory= persist_directory)

