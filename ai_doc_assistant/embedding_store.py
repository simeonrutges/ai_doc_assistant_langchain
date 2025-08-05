import os
import faiss
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from typing import List

CHUNK_SIZE = 500  # aantal tekens per chunk (voor nu)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

class EmbeddingStore:
    def __init__(self, model_name=EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.text_chunks = []

    def add_text(self, text: str):
        chunks = self.chunk_text(text)
        self.build_index(chunks)

    def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE) -> List[str]:
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def build_index(self, chunks: List[str]):
        self.text_chunks = chunks
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def save(self, path: str):
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))
        with open(os.path.join(path, "chunks.pkl"), "wb") as f:
            pickle.dump(self.text_chunks, f)

    @classmethod
    def load(cls, path: str):
        instance = cls()
        index_path = os.path.join(path, "index.faiss")
        chunks_path = os.path.join(path, "chunks.pkl")

        instance.index = faiss.read_index(index_path)
        with open(chunks_path, "rb") as f:
            instance.text_chunks = pickle.load(f)

        return instance

    def query(self, query_text: str, top_k: int = 3) -> List[str]:
        query_embedding = self.model.encode([query_text])
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.text_chunks[i] for i in indices[0]]
