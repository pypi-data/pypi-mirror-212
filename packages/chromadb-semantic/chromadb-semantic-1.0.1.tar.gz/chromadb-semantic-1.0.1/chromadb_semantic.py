#!/usr/bin/env python
# chromadb_semantic.py

import os
from typing import List, Dict

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


def embedding_function(text: str):
    return model.encode(text).tolist()


def create_chromadb_client() -> chromadb.Client:
    os.makedirs("./data", exist_ok=True)
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./data"  # Optional, defaults to .chromadb/ in the current directory
    ))
    return client


def create_collection(client: chromadb.Client, collection_name: str):
    return client.create_collection(name=collection_name, embedding_function=embedding_function)


def add_documents_to_collection(collection, documents: List[str], metadatas: List[Dict],
                                ids: List[str]):
    collection.add(documents=documents, metadatas=metadatas, ids=ids)


def query_collection(collection, query_text: str, n_results: int = 10):
    query_embedding = embedding_function(query_text)
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    return results


def example_usage():
    client = create_chromadb_client()

    collection_name = 'my_sentence_transformer_collection'
    collection = create_collection(client, collection_name)

    documents = ["This is a sample document.", "玉里鎮的月亮比較大顆", "This is a test document."]
    ids = ["doc1", "doc2", "doc3"]
    metadatas = [{"type": "sample"}, {"type": "example"}, {"type": "test"}]

    add_documents_to_collection(collection, documents, metadatas, ids)

    query_text = "哪一個鄉鎮的月亮比較圓"
    results = query_collection(collection, query_text, n_results=2)

    print(f"Results for query: {query_text}")
    print(results)


if __name__ == "__main__":
    example_usage()
