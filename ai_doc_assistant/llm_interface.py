import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:instruct"

def ask_llm(question: str, context: str) -> str:
    prompt = f"""Beantwoord de volgende vraag zo duidelijk mogelijk op basis van de context hieronder.

Context:
{context}

Vraag:
{question}

Antwoord:"""

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        raise RuntimeError(f"Ollama gaf een fout terug: {response.text}")

    return response.json()["response"]
