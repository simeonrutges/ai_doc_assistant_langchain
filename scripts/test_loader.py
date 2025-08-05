from ai_doc_assistant.document_loader import load_text_from_file

def main():
    filepath = "documents/sample.pdf"
    try:
        text = load_text_from_file(filepath)
        print("✅ Tekst geladen uit PDF:")
        print("-" * 50)
        print(text[:1000])  # Print de eerste 1000 tekens
    except Exception as e:
        print(f"❌ Fout bij laden van bestand: {e}")

if __name__ == "__main__":
    main()