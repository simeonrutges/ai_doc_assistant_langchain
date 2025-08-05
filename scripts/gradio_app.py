import os
import gradio as gr
from ai_doc_assistant.document_loader import load_text_from_file
from ai_doc_assistant.embedding_store import EmbeddingStore
from ai_doc_assistant.llm_interface import ask_llm
from scripts.ask_docs import stel_vraag_aan_document

DOCUMENTS_DIR = "documents"
VECTORSTORE_DIR = "vectorstore"
SUMMARIES_DIR = "summaries"

def beschikbare_documenten():
    return [
        f for f in os.listdir(DOCUMENTS_DIR)
        if f.lower().endswith((".pdf", ".txt", ".docx", ".md", ".csv"))
    ]

def herindexeer_documenten():
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    for filename in beschikbare_documenten():
        path = os.path.join(DOCUMENTS_DIR, filename)
        name = os.path.splitext(filename)[0]
        text = load_text_from_file(path)
        store = EmbeddingStore()
        store.add_text(text)
        store.save(os.path.join(VECTORSTORE_DIR, f"{name}.faiss"))
    return "✅ Index opnieuw opgebouwd."

def beantwoord_vraag(vraag, document):
    name = os.path.splitext(document)[0]
    vectorstore_path = os.path.join(VECTORSTORE_DIR, f"{name}.faiss")
    store = EmbeddingStore.load(vectorstore_path)
    context = store.query(vraag)
    return ask_llm(vraag, context)

def genereer_samenvatting(document):
    name = os.path.splitext(document)[0]
    vectorstore_path = os.path.join(VECTORSTORE_DIR, f"{name}.faiss")
    store = EmbeddingStore.load(vectorstore_path)
    context = store.query("Geef een samenvatting van het document.")
    prompt = "Vat het document samen in één alinea:\n\n" + "\n\n".join(context)
    summary = ask_llm(prompt, context)
    os.makedirs(SUMMARIES_DIR, exist_ok=True)
    output_path = os.path.join(SUMMARIES_DIR, f"{name}.summary.txt")
    with open(output_path, "w") as f:
        f.write(summary)
    return summary

def upload_document(file):
    if file is None:
        return "⚠️ Geen bestand geüpload."
    filename = os.path.basename(file.name)
    dest_path = os.path.join(DOCUMENTS_DIR, filename)
    with open(dest_path, "wb") as f:
        f.write(file.read())
    return f"✅ Bestand '{filename}' opgeslagen."

def start_gradio():
    with gr.Blocks(theme=gr.themes.Default) as demo:
        gr.Markdown("# 📄 AI Documentassistent")

        with gr.Row():
            vraag = gr.Textbox(label="Stel je vraag")
            document = gr.Dropdown(choices=beschikbare_documenten(), label="Kies een document")

        antwoord = gr.Textbox(label="Antwoord", lines=5)
        context_output = gr.Textbox(label="Bronfragmenten", lines=10, interactive=False)

        def beantwoord_met_context(vraag, document):
            antwoord, contextfragmenten = stel_vraag_aan_document(vraag, os.path.splitext(document)[0])
            context_tekst = "\n\n".join(
                [f"📚 Fragment {i+1}:\n{fragment}" for i, fragment in enumerate(contextfragmenten)]
            )
            return antwoord, context_tekst

        gr.Button("Beantwoord vraag").click(
            beantwoord_met_context, inputs=[vraag, document], outputs=[antwoord, context_output]
        )

        gr.Markdown("---")

        gr.Markdown("## 📄 Samenvatting")
        samenvatting_output = gr.Textbox(label="Samenvatting")
        gr.Button("Genereer samenvatting").click(
            genereer_samenvatting, inputs=document, outputs=samenvatting_output
        )

        gr.Markdown("---")

        gr.Markdown("## 📁 Upload nieuw document")
        upload = gr.File(label="Upload hier een bestand")
        upload_output = gr.Textbox(label="Upload status")
        gr.Button("Upload").click(upload_document, inputs=upload, outputs=upload_output)

        gr.Markdown("---")

        gr.Button("🔄 Herbouw alle indices").click(
            herindexeer_documenten, outputs=gr.Textbox(label="Index status")
        )

    demo.launch()

if __name__ == "__main__":
    start_gradio()

