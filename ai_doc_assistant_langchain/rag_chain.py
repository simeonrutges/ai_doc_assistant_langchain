from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.retriever import BaseRetriever


def load_vectorstore(
    persist_path: str = "vectorstore", model_name: str = "llama3"
) -> FAISS:
    """
    Laadt een opgeslagen FAISS vectorstore vanaf schijf.
    """
    embeddings = OllamaEmbeddings(model=model_name)
    return FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)


def build_rag_chain(
    retriever: BaseRetriever, model_name: str = "llama3"
) -> RetrievalQA:
    """
    Bouwt een RetrievalQA-chain op basis van een retriever en LLM.
    """
    llm = OllamaLLM(model=model_name)
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain


def ask_question(question: str, chain: RetrievalQA) -> str:
    """
    Vraagt iets aan de RetrievalQA-chain en retourneert het antwoord.
    """
    return chain.invoke(question)
