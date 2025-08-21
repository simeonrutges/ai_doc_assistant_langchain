from ai_doc_assistant_langchain.ingest import ingest_documents
from ai_doc_assistant_langchain.rag_chain import (
    build_rag_chain,
    ask_question,
)
from unittest.mock import patch
from langchain_core.embeddings import Embeddings


# FakeEmbeddings vervangt OllamaEmbeddings in tests
class FakeEmbeddings(Embeddings):
    def __init__(self, model=None):
        self.model = model

    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]

    def embed_query(self, text):
        return [0.1] * 1536


@patch("ai_doc_assistant_langchain.ingest.OllamaEmbeddings", new=FakeEmbeddings)
def test_full_rag_pipeline():
    # Stap 1: Index bouwen (of hergebruiken als reeds aanwezig)
    vectorstore = ingest_documents("documents")

    # Stap 2: Retriever ophalen uit vectorstore
    retriever = vectorstore.as_retriever()

    # Stap 3: Chain bouwen met LLM + retriever
    chain = build_rag_chain(retriever)

    # Stap 4: Vraag stellen aan de chain
    question = "Wat is het onderwerp van het document?"
    answer = ask_question(question, chain)

    # Stap 5: Valideer antwoord
    assert "result" in answer
    assert isinstance(answer["result"], str)
    assert len(answer["result"].strip()) > 10