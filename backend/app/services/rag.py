import fitz
import time
import os
from google import genai as google_genai 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from app.core.config import settings


DATASHEET_DIR = "data/datasheets"
CHROMADB_DIR = "data/chromadb"


def load_pdf(pdf_path:str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text



def split_text(text: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return splitter.split_text(text)



def index_datasheet(component_name:str, pdf_path:str):
    print(f"Indexing {component_name}")
    
    text = load_pdf(pdf_path) 
    
    chunks = split_text(text) 
    print(f" -> {len(chunks)} chunks")
    
    import chromadb
    client = chromadb.PersistentClient(path=CHROMADB_DIR)
    collection = client.get_or_create_collection(name=component_name.lower())
    
    collection.add(
        documents=chunks,
        ids=[f"{component_name}_{i}" for i in range(len(chunks))]
    )
    
    print(f" -> Indexed {component_name} succesfully!")
    return len(chunks)


def query_datasheet(component_name:str, question:str) -> str:
    import chromadb
    client = chromadb.PersistentClient(path=CHROMADB_DIR)
    collection = client.get_or_create_collection(name=component_name.lower())
    
    result = collection.query(
        query_texts=[question],
        n_results=3
    )
    
    chunks = result["documents"][0]
    context = "\n\n".join(chunks)
    
    return context


def ask_component(component_name: str, question:str) ->str:
    context = query_datasheet(component_name, question)
    
    client = google_genai.Client(api_key=settings.gemini_api_key)

    
    prompt = f"""you are a helpful electronic assistant.
    answer the question bases ONLY on the datasheet context below.
    IF the answer is not in the context, say 'I don't have that information in the datasheet.'
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text