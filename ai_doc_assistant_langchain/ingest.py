from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from ai_doc_assistant_langchain.utils import load_text_from_file
import os

def ingest_documents(folder: str, persist_path: str = "vectorstore") -> FAISS:
    docs = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        raw_text = load_text_from_file(filepath)
        docs.append(Document(page_content=raw_text, metadata={"source": filename}))

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="llama3")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(persist_path)
    return db

# Doel:
# Bestanden inlezen (bijv. met load_text_from_file() of LangChain loaders)

# Splitsen met RecursiveCharacterTextSplitter

# Vectorstore bouwen (bijv. FAISS of Chroma)

# Opslaan/herladen van store naar disk

