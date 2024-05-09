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
    """Reads content from a markdown file and returns the title and the entire content."""
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
    """Splits content into chunks based on markdown headers and then into smaller chunks."""
    try:
        md_split_texts = markdown_splitter.split_text(content)
        token_split_texts = []
        for text in md_split_texts:
            token_split_texts += token_splitter.split_text(text.page_content)
        return token_split_texts
    except Exception as e:
        logging.error(f"Error splitting text: {e}")
        return []


def prepare_metadata(token_split_texts, base_filename, title):
    """Prepares metadata for the chunks."""
    try:
        return [{"filename": base_filename, "title": title} for _ in token_split_texts]
    except Exception as e:
        logging.error(f"Error preparing metadata: {e}")
        return []


def ingest_chunks(ids, documents, metadatas, collection):
    """Adds chunks to the ChromaDB collection."""
    try:
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
    except Exception as e:
        logging.error(f"Failed to ingest chunks into the collection: {e}")


def parse_arguments():
    """Parses command-line arguments."""
    import argparse
    try:
        parser = argparse.ArgumentParser(description="Ingest markdown documentation into ChromaDB.")
        parser.add_argument("--data-path", type=str, required=True, help="Glob path to markdown files for ingestion.")
        return parser.parse_args()
    except Exception as e:
        logging.error(f"Error parsing arguments: {e}")
        raise

def setup_markdown_splitter():
    """Sets up the Markdown header splitter with specific headers."""
    try:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3")
        ]
        return MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    except Exception as e:
        logging.error(f"Error setting up Markdown splitter: {e}")
        raise

def setup_token_splitter():
    """Sets up the token text splitter with specified chunk parameters."""
    try:
        return SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)
    except Exception as e:
        logging.error(f"Error setting up token splitter: {e}")
        raise

def setup_chromadb():
    """Sets up the ChromaDB client and collection."""
    try:
        embedding_function = SentenceTransformerEmbeddingFunction()
        chroma_client = chromadb.PersistentClient(path="./chromadb")
        return chroma_client.get_or_create_collection("mojo", embedding_function=embedding_function)
    except Exception as e:
        logging.error(f"Error setting up ChromaDB collection: {e}")
        raise

def process_file(file_path, markdown_splitter, token_splitter, collection, total_chunks_added):
    """Processes a single file and ingests its chunks into the ChromaDB collection."""
    try:
        title, file_content = read_file_content(file_path)
        if file_content is None:
            return total_chunks_added

        token_split_texts = split_text(file_content, markdown_splitter, token_splitter)
        base_filename = os.path.basename(file_path)
        metadatas = prepare_metadata(token_split_texts, base_filename, title)
        ids = [f"{base_filename}_{i}" for i in range(total_chunks_added, total_chunks_added + len(token_split_texts))]
        ingest_chunks(ids, token_split_texts, metadatas, collection)
        return total_chunks_added + len(token_split_texts)
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return total_chunks_added

def main():
    """Main function orchestrating the ingestion of markdown files into ChromaDB."""
    try:
        args = parse_arguments()
        file_path_list = glob.glob(args.data_path)

        markdown_splitter = setup_markdown_splitter()
        token_splitter = setup_token_splitter()
        chroma_collection = setup_chromadb()

        total_chunks_added = 0
        for file_path in tqdm(file_path_list):
            total_chunks_added = process_file(file_path, markdown_splitter, token_splitter, chroma_collection, total_chunks_added)

        logging.info(f"Total chunks added: {total_chunks_added}")
    except Exception as e:
        logging.error(f"Error ingesting files: {e}")


if __name__ == "__main__":
    main()