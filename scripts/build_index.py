import os
from ai_doc_assistant.document_loader import load_text_from_file
from ai_doc_assistant.embedding_store import EmbeddingStore

DOCUMENTS_DIR = "documents"
VECTORSTORE_DIR = "vectorstore"
TOP_K = 3  # eventueel gebruikt in query/debug

def main():
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    files = [
        f for f in os.listdir(DOCUMENTS_DIR)
        if f.lower().endswith(('.pdf', '.txt', '.docx'))
    ]

    if not files:
        print("⚠️ Geen documenten gevonden in de 'documents/' map.")
        return

    for filename in files:
        path = os.path.join(DOCUMENTS_DIR, filename)
        name = os.path.splitext(filename)[0]
        print(f"\n📄 Verwerken: {filename}")

        text = load_text_from_file(path)
        print("🔪 Opdelen in chunks...")

        store = EmbeddingStore()
        store.add_text(text)

        output_path = os.path.join(VECTORSTORE_DIR, f"{name}.faiss")
        print(f"💾 Opslaan van index in: {output_path}")
        store.save(output_path)

    print("\n✅ Alle documenten zijn geïndexeerd.")

if __name__ == "__main__":
    main()

