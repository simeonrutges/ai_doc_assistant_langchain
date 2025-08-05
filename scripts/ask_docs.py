import sys
import os
from ai_doc_assistant.document_loader import load_text_from_file
from ai_doc_assistant.embedding_store import EmbeddingStore
from ai_doc_assistant.llm_interface import ask_llm

VECTORSTORE_DIR = "vectorstore"
TOP_K = 3

def stel_vraag_aan_document(vraag: str, naam: str) -> tuple[str, list[str]]:
    base_name = os.path.splitext(naam)[0]
    vectorstore_path = os.path.join(VECTORSTORE_DIR, f"{base_name}.faiss")
    if not os.path.exists(vectorstore_path):
        raise FileNotFoundError(f"❌ Bestand niet gevonden: {vectorstore_path}")

    print(f"📦 Laden van vectorstore voor '{naam}'...")
    store = EmbeddingStore.load(vectorstore_path)

    print("🔍 Relevante tekst ophalen...")
    context = store.query(vraag, top_k=TOP_K)

    antwoord = ask_llm(vraag, context)
    return antwoord, context

def main():
    if len(sys.argv) < 2:
        print("Gebruik: python ask_docs.py \"Wat is je vraag?\" [optioneel: bestandsnaam zonder extensie]")
        sys.exit(1)

    vraag = sys.argv[1]
    target_doc = sys.argv[2] if len(sys.argv) > 2 else None

    if target_doc:
        antwoord, context = stel_vraag_aan_document(vraag, target_doc)
    else:
        print("❌ Geef voor deze versie een documentnaam mee als tweede argument.")
        sys.exit(1)

    print("\n📚 🔎 Contextfragmenten:")
    for i, chunk in enumerate(context, 1):
        print(f"\n--- Fragment {i} ---\n{chunk}\n")

    print("🤖 Antwoord genereren via LLM...")
    print("\n✅ Antwoord:")
    print(antwoord)

if __name__ == "__main__":
    main()
