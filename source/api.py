import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

import chromadb
from sentence_transformers import CrossEncoder

from models import Message
from services import get_answer
from evaluation import evaluate_rag
import os
print(os.environ.get('PYTHONPATH'))

logging.basicConfig(level=logging.ERROR, filename='api_errors.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma_client = chromadb.PersistentClient(path="./chromadb")
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions."""
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred"}
    )

@app.get("/", tags=["Test"])
def home():
    """A simple test endpoint."""
    return {"Nothing": "to see here"}

@app.post("/api/chat", tags=["Chat"])
async def chat(message: Message):
    """Endpoint to receive chat messages and return responses."""
    response = get_answer(message.message, chroma_client, cross_encoder)
    return response

@app.get("/evaluate", tags=["Evaluate"])
def get_rag_evaluation():
    """Endpoint to evaluate the most recent response."""
    evaluation = evaluate_rag()
    return {"evaluation":str(evaluation)}
