import os
import fitz  # PyMuPDF
from docx import Document
import csv

def load_text_from_file(filepath: str) -> str:
    """
    Leest de inhoud van een bestand (.pdf, .docx, .txt, .csv, .md) en geeft de ruwe tekst terug.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Bestand bestaat niet: {filepath}")

    extension = os.path.splitext(filepath)[1].lower()

    if extension == '.pdf':
        return _load_pdf(filepath)
    elif extension == '.docx':
        return _load_docx(filepath)
    elif extension == '.txt':
        return _load_txt(filepath)
    elif extension == '.csv':
        return _load_csv(filepath)
    elif extension == '.md':
        return _load_md(filepath)
    else:
        raise ValueError(f"Niet-ondersteund bestandstype: {extension}")


def _load_pdf(filepath: str) -> str:
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text

def _load_docx(filepath: str) -> str:
    doc = Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

def _load_txt(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def _load_csv(filepath: str) -> str:
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(", ".join(row))
    return "\n".join(rows)

def _load_md(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()
