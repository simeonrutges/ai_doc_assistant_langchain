from langchain.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OllamaEmbeddings

def load_qa_chain(vectorstore_path="vectorstore"):
    embeddings = OllamaEmbeddings(model="llama3")
    db = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    llm = Ollama(model="llama3")
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain

def ask_question(question: str, chain: RetrievalQA):
    return chain.run(question)
