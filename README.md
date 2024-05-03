![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)

# Mojo Documentation Assistant


## Introduction

This is a first draft on what aims to be a template for creating RAG assistants using markdown-based data.

Ask something about Mojo, and the chatbot will provide an answer, citing the sources used to construct the response and, depending on the amount of data related to the subject, suggesting further reading relevant to your query.

## Usage

Clone the repo:

```bash
git clone https://github.com/hc8sea/MojoRAG
cd MojoRAG
```

Setup the vector store:

```bash
python3 source/data_ingestor.py --data-path '../data/mojo/docs/*.md'
```

Setup the server:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn source.main:app --reload
```
Query something:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "Why Mojo?"}' \
  http://localhost:8000/api/chat
```

Perform evaluation on the most recent query:
```bash
curl http://localhost:8000/evaluate
```

## Technologies Employed

| Component                | Technology                                | Description                                                       |
|--------------------------|-------------------------------------------|-------------------------------------------------------------------|
| **Vector Store**         | ChromaDB                                  | Manages the storage and retrieval of vectors for quick access.    |
| **Pre-chunking**         | Langchain's MarkdownHeaderTextSplitter    | Splits documents based on Markdown headers.                       |
| **Chunking**             | all-mpnet-base-v2 Sentence Transformer    | Token-count based splitting.                                      |
| **Embedding Model**      | all-MiniLM-L6-v2 Sentence Transformer     | Lightweight embedding model. Should be the same embedding model.  |
| **Vector Similarity**    | Hierarchical Navigable Small Worlds (HNSW)| High-performance algorithm for nearest neighbor search            |
| **Re-Ranking**           | ms-marco-MiniLM-L-6-v2                    | Text Classification model to rank the most relevant chunks        |
| **Large Language Model** | OpenAI's gpt-3.5-turbo                    | Utilized for generating human-like text and understanding queries.|
| **Evaluation**           | Ragas                                     | Measures metrics such as Answer Relevancy and Context Utilization |
| **Databases**            | SQLite                                    | Handles data storage and management locally.                      |
