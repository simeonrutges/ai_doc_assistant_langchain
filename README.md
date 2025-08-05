# AI Document Assistant

![CI](https://github.com/simeonrutges/ai_doc_assistant/actions/workflows/ci.yml/badge.svg)

**AI Document Assistant** is een lokaal Python-project waarin ik werk aan een lokale AI-documentassistent.  
Het is opgezet als persoonlijk oefenproject om ervaring op te doen met document parsing, chunking, embeddings en Retrieval-Augmented Generation (RAG) met een lokaal draaiende Large Language Model via [Ollama](https://ollama.com). In plaats van het gebruiken van frameworks zoals LangChain is bewust gekozen om de kernfunctionaliteit (zoals chunking, opslag en retrieval) zelf te bouwen.

Het project draait volledig lokaal waarbij rekening is gehouden met privacy, modulariteit en uitbreidbaarheid. De huidige versie is te starten via de command line en is verder te bedienen via een simpele webinterface (Gradio).

---

## Huidige functionaliteit

- **Ondersteuning voor meerdere bestandsformaten**  
  Inlezen van `.pdf`, `.txt`, `.docx`, `.csv` en `.md` bestanden.

- **Chunking & vectorstore**  
  Documenttekst wordt opgesplitst in beheersbare stukken (chunks), voorzien van embeddings, en opgeslagen in een FAISS-vectorstore.

- **RAG-gebaseerde vraagbeantwoording**  
  Je kunt vragen stellen over documenten via de CLI. De assistent zoekt relevante context en laat een lokaal LLM een antwoord genereren.

- **Automatische document-samenvattingen**  
  Alle documenten in de `documents/`-map kunnen automatisch worden samengevat. De resultaten worden opgeslagen in `summaries/`.

- **Modulaire opzet met professioneel versiebeheer**  
  Duidelijke structuur (`core/`, `scripts/`, enz.), dependency management met Poetry, en werken met feature branches in Git.

---

## Mogelijke vervolgstappen

- REST API bouwen met FastAPI   
- Vragen stellen over meerdere documenten tegelijk  
- Contextuele of hoofdstukgerichte samenvattingen  
- Feedback-logging en evaluatie van gegenereerde antwoorden

---

## Installatie en starten

Zorg dat je Python 3.11 (niet hoger dan 3.12) en [Poetry](https://python-poetry.org/docs/#installation) hebt geïnstalleerd.

Kloon de repository en installeer de afhankelijkheden:

```bash
git clone https://github.com/simeonrutges/ai_doc_assistant
cd ai_doc_assistant
poetry install --with dev
```
Installeer en start een lokaal taalmodel via Ollama:

```bash
ollama run llama3
```



## Hoe gebruik je de documentassistent

### Start de interface

Je kunt de Gradio-interface starten op twee manieren:

#### Optie 1: via `poetry run` (aanbevolen)

Als je nog **niet** in de virtuele omgeving zit:

```bash
poetry run env PYTHONPATH=. python scripts/gradio_app.py 
```
### Optie 2: binnen een geactiveerde virtuele omgeving
```bash
export PYTHONPATH=.
python scripts/gradio_app.py
```
## Functionaliteiten van de Gradio-interface

De interface biedt volledige functionaliteit voor lokale documentanalyse:

### Upload nieuw document
- Upload een PDF, DOCX, TXT, CSV of Markdown-bestand.
- Bestanden worden automatisch opgeslagen in de `documents/`-map.
- druk op de knop **Herbouw alle indices** 


### Herbouw alle indices
- Splitst documenten in tekstchunks.
- Genereert embeddings en slaat deze op in `vectorstore/`.
- Noodzakelijke stap voordat vragen of samenvattingen kunnen worden gegenereerd.

### Stel een vraag
- Kies een document in de dropdown.
- Typ een vraag in natuurlijke taal.
- Ontvang een antwoord gegenereerd door het lokale LLM.
- Bekijk ook de bijbehorende bronfragmenten uit het document.

### Genereer samenvatting
- Vat het geselecteerde document samen in één beknopte alinea.
- Samenvatting wordt ook opgeslagen in de map `summaries/`.

---
