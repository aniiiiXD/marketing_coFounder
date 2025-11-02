#!/usr/bin/env python3
"""
Test script for ChromaDB vector store functionality
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import VectorStore
sys.path.append(str(Path(__file__).parent.parent))

from rag.vector_store import VectorStore

def test_vector_store():
    print("\n=== Testing Vector Store ===")
    
    # Initialize the vector store
    print("\n1. Initializing vector store...")
    vector_store = VectorStore(persist_directory="./chroma_db")
    
    # Test adding documents
    print("\n2. Testing document addition...")
    test_docs = [
        "Marketing is the process of creating value for customers.",
        "Content marketing focuses on creating valuable content to attract customers.",
        "Social media is a powerful channel for digital marketing."
    ]
    
    metadatas = [
        {"source": "test", "type": "test_data", "chunk_id": 0},
        {"source": "test", "type": "test_data", "chunk_id": 1},
        {"source": "test", "type": "test_data", "chunk_id": 2}
    ]
    
    ids = [f"test_doc_{i}" for i in range(len(test_docs))]
    
    # Add test documents
    vector_store.add_documents(test_docs, metadatas, ids)
    print(f"✓ Added {len(test_docs)} test documents")
    
    # Test search functionality
    print("\n3. Testing search functionality...")
    query = "What is marketing about?"
    results = vector_store.search(query, n_results=2)
    
    print(f"\nSearch results for: '{query}'")
    print("-" * 50)
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Document: {result['document']}")
        print(f"Metadata: {result['metadata']}")
        print(f"Distance: {result['distance']:.4f}")
    
    # Test collection info
    print("\n4. Testing collection information...")
    info = vector_store.get_collection_info()
    print(f"Collection name: {info['collection_name']}")
    print(f"Total documents: {info['document_count']}")
    
    print("\n✓ All tests completed successfully!")

if __name__ == "__main__":
    test_vector_store()
