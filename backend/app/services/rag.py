import fitz
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings

DATASHEET_DIR = "data/datasheets"
CHROMADB_DIR = "data/chromadb"


# extrak pdf
def load_pdf(pdf_path:str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# text to cank
def split_text(text: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return splitter.split_text(text)


# main proses
def index_datasheet(component_name:str, pdf_path:str):
    print(f"Indexing {component_name}")
    
    text = load_pdf(pdf_path) #pake fungsi load_pdf
    
    chunks = split_text(text) # pake fungsi split_text
    print(f" -> {len(chunks)} chunks")
    
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        google_api_key=setting.gemini_api_key # api
    )
    
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        parsists_directory=CHROMADB_DIR,
        collection_name=component_name.lower()
    )
    
    print(f" -> Indexed {component_name} succesfully!")
    return len(chunks)