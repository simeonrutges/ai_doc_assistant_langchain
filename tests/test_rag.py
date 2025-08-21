import os
from ai_doc_assistant_langchain.ingest import ingest_documents
from ai_doc_assistant_langchain.rag_chain import (
    build_rag_chain,
    ask_question,
)
from unittest.mock import patch
from langchain_core.embeddings import Embeddings


class FakeEmbeddings(Embeddings):
    def __init__(self, model=None):
        self.model = model

    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]

    def embed_query(self, text):
        return [0.1] * 1536


@patch("ai_doc_assistant_langchain.ingest.OllamaEmbeddings", new=FakeEmbeddings)
def test_full_rag_pipeline(tmp_path):
    # Stap 0: Maak tijdelijk testdocument aan
    test_file = tmp_path / "test.txt"
    test_file.write_text("Dit is een testdocument over AI en taalmodellen.")

    # Stap 1: Index bouwen
    vectorstore = ingest_documents(str(tmp_path))

    # Stap 2: Retriever ophalen
    retriever = vectorstore.as_retriever()

    # Stap 3: Chain bouwen
    chain = build_rag_chain(retriever)

    # Stap 4: Vraag stellen
    question = "Wat is het onderwerp van het document?"
    answer = ask_question(question, chain)

    # Stap 5: Validatie
    assert "result" in answer
    assert isinstance(answer["result"], str)
    assert len(answer["result"].strip()) > 10

