# RAG Portfolio Assistant

A locally-hosted RAG (Retrieval-Augmented Generation) chatbot that answers questions about Sarika S Shirolkar's portfolio — built with Python, Ollama, and Streamlit.

No cloud APIs. No API keys. Runs entirely on your machine.

---

## How it works

1. A question comes in from the Streamlit UI
2. The backend tokenizes it and scores it against a portfolio knowledge base (experience, projects, skills, education, leadership)
3. The top matching documents are retrieved and passed as context to a local LLM via Ollama
4. The LLM generates a grounded answer — only from the provided context

```
User question
     │
     ▼
Token-based retrieval (local knowledge base)
     │
     ▼
Top-k docs → context
     │
     ▼
Ollama LLM (llama3.2:3b)
     │
     ▼
Answer + sources
```

---

## Stack

| Layer     | Tech                        |
|-----------|-----------------------------|
| Frontend  | Streamlit                   |
| Backend   | Python (stdlib HTTP server) |
| LLM       | Ollama (`llama3.2:3b`)      |
| Retrieval | Token-based scoring (no embeddings) |

---

## Setup

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed and running

### 1. Clone the repo

```bash
git clone https://github.com/sarikashirolkar/RAG-portfolio.git
cd RAG-portfolio
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull the model

```bash
ollama pull llama3.2:3b
```

### 5. Start the backend (Terminal 1)

```bash
python local_chat_server.py
# Running on http://127.0.0.1:8008
```

### 6. Start the frontend (Terminal 2)

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Configuration

The backend reads these environment variables (all optional):

| Variable      | Default                    | Description              |
|---------------|----------------------------|--------------------------|
| `OLLAMA_URL`  | `http://127.0.0.1:11434/api/generate` | Ollama endpoint |
| `OLLAMA_MODEL`| `llama3.2:3b`              | Model to use             |
| `CHAT_HOST`   | `127.0.0.1`                | Backend host             |
| `CHAT_PORT`   | `8008`                     | Backend port             |

Example with a different model:

```bash
OLLAMA_MODEL=mistral python local_chat_server.py
```

---

## Project structure

```
RAG-portfolio/
├── app.py                  # Streamlit frontend
├── local_chat_server.py    # RAG backend (retrieval + Ollama)
├── requirements.txt
└── README.md
```

---

## Sample questions to try

- *What is Sarika currently working on?*
- *Tell me about the IEEE paper*
- *What are her skills?*
- *What did she do at Bharat Electronics?*
- *What projects has she built?*

---

Built by [Sarika S Shirolkar](https://github.com/sarikashirolkar)
