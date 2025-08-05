import os
from ai_doc_assistant.document_loader import load_text_from_file
from ai_doc_assistant.llm_interface import ask_llm

DOCUMENTS_DIR = "documents"
SUMMARIES_DIR = "summaries"

def main():
    os.makedirs(SUMMARIES_DIR, exist_ok=True)

    files = [
        f for f in os.listdir(DOCUMENTS_DIR)
        if f.lower().endswith(('.pdf', '.txt', '.docx', '.csv', '.md'))
    ]

    if not files:
        print("⚠️ Geen documenten gevonden in 'documents/'")
        return

    for filename in files:
        name = os.path.splitext(filename)[0]
        input_path = os.path.join(DOCUMENTS_DIR, filename)
        output_path = os.path.join(SUMMARIES_DIR, f"{name}.summary.txt")

        print(f"\n📝 Samenvatten: {filename}")
        text = load_text_from_file(input_path)

        prompt = (
            "Vat onderstaande tekst samen in maximaal 10 zinnen.\n\n"
            f"{text}"
        )
        summary = ask_llm(prompt, "")

        with open(output_path, "w") as f:
            f.write(summary.strip())

        print(f"✅ Samenvatting opgeslagen in: {output_path}")

if __name__ == "__main__":
    main()


