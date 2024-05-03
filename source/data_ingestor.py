#!/usr/bin/env python3
"""
Script for ingesting markdown files into a ChromaDB database.
This script reads markdown files, splits them into chunks, and ingests them into a specified ChromaDB collection.
Usage:
    python3 source/data_ingestor.py --data-path '../data/mojo/docs/*.md'
"""

import config
import argparse
import glob
import os
import logging
from tqdm import tqdm
import chromadb
from langchain.text_splitter import SentenceTransformersTokenTextSplitter, MarkdownHeaderTextSplitter
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_lines = file.readlines()
        title = file_lines[0].strip()
        content = "".join(file_lines)
        return title, content
    except Exception as e:
        logging.error(f"Failed to read {file_path}: {e}")
        return None, None


def split_text(content, markdown_splitter, token_splitter):
    md_split_texts = markdown_splitter.split_text(content)
    print(md_split_texts)
    token_split_texts = []
    for text in md_split_texts:
        token_split_texts += token_splitter.split_text(text.page_content)
    return token_split_texts


def prepare_metadata(token_split_texts, base_filename, title):
    return [{"filename": base_filename, "title": title} for _ in token_split_texts]


def ingest_chunks(ids, documents, metadatas, collection):
    collection.add(ids=ids, documents=documents, metadatas=metadatas)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Ingest markdown documentation into ChromaDB.")
    parser.add_argument("--data-path", type=str, required=True, help="Glob path to markdown files for ingestion.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    file_path_list = glob.glob(args.data_path)

    headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)
    embedding_function = SentenceTransformerEmbeddingFunction()
    chroma_client = chromadb.PersistentClient(path="./chromadb")
    chroma_collection = chroma_client.get_or_create_collection("mojo", embedding_function=embedding_function)

    total_chunks_added = 0

    for file_path in tqdm(file_path_list):
        title, file_content = read_file_content(file_path)
        if file_content is None:
            continue

        token_split_texts = split_text(file_content, markdown_splitter, token_splitter)
        base_filename = os.path.basename(file_path)
        metadatas = prepare_metadata(token_split_texts, base_filename, title)
        ids = [f"{base_filename}_{i}" for i in range(total_chunks_added, total_chunks_added + len(token_split_texts))]
        ingest_chunks(ids, token_split_texts, metadatas, chroma_collection)
        total_chunks_added += len(token_split_texts)

    logging.info(f"Total chunks added: {total_chunks_added}")


if __name__ == "__main__":
    main()