#!/usr/bin/env python3
"""
Data Onboarding Script for Marketing Co-founder

This script helps you quickly onboard your marketing data into the RAG system.
Supports: PDFs, text files, URLs, and structured data.
"""

import os
import asyncio
from pathlib import Path
from typing import List, Dict, Any
import logging 
from datetime import datetime
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from rag.vector_store import VectorStore

class DataOnboarder:
    def __init__(self):
        self.vector_store = VectorStore()
        self.knowledge_base_dir = Path("knowledge_base")
        self.knowledge_base_dir.mkdir(exist_ok=True)
    
    def onboard_text_files(self, file_paths: List[str]):
        """Onboard text files into the knowledge base"""
        documents = []
        metadatas = []
        ids = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Split into chunks (simple approach)
                chunks = self._chunk_text(content, chunk_size=1000)
                
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({
                        "source": file_path,
                        "chunk_id": i,
                        "type": "text_file",
                        "uploaded_at": datetime.now().isoformat()
                    })
                    ids.append(f"{file_path}_{i}")
                
                logger.info(f"Processed {file_path}: {len(chunks)} chunks")
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
        
        if documents:
            self.vector_store.add_documents(documents, metadatas, ids)
            logger.info(f"Successfully onboarded {len(documents)} text chunks")
    
    def onboard_marketing_data(self, data: Dict[str, Any], source_name: str):
        """Onboard structured marketing data"""
        documents = []
        metadatas = []
        ids = []
        
        # Convert structured data to searchable text
        for key, value in data.items():
            if isinstance(value, (str, int, float)):
                text = f"{key}: {value}"
                documents.append(text)
                metadatas.append({
                    "source": source_name,
                    "data_type": key,
                    "type": "structured_data",
                    "uploaded_at": datetime.now().isoformat()
                })
                ids.append(f"{source_name}_{key}_{datetime.now().timestamp()}")
        
        if documents:
            self.vector_store.add_documents(documents, metadatas, ids)
            logger.info(f"Onboarded {len(documents)} data points from {source_name}")
    
    def onboard_company_info(self, company_data: Dict[str, Any]):
        """Quick onboarding for company information"""
        company_text = f"""
        Company: {company_data.get('name', 'Unknown')}
        Industry: {company_data.get('industry', 'Unknown')}
        Target Audience: {company_data.get('target_audience', 'Unknown')}
        Value Proposition: {company_data.get('value_proposition', 'Unknown')}
        Key Products/Services: {company_data.get('products_services', 'Unknown')}
        Brand Voice: {company_data.get('brand_voice', 'Professional')}
        Competitors: {company_data.get('competitors', 'Unknown')}
        """
        
        self.vector_store.add_documents(
            documents=[company_text],
            metadatas=[{
                "source": "company_profile",
                "type": "company_info",
                "uploaded_at": datetime.now().isoformat()
            }],
            ids=[f"company_profile_{datetime.now().timestamp()}"]
        )
        logger.info("Company information onboarded successfully")
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Enhanced semantic text chunking with overlap"""
        # First try to split by paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if not paragraphs:
            # Fallback to sentence splitting
            import re
            sentences = re.split(r'[.!?]+', text)
            paragraphs = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for para in paragraphs:
            para_size = len(para)
            
            # If single paragraph is too large, split it
            if para_size > chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_size = 0
                
                # Split large paragraph by sentences
                sentences = [s.strip() + '.' for s in para.split('.') if s.strip()]
                for sentence in sentences:
                    if current_size + len(sentence) > chunk_size and current_chunk:
                        chunks.append(' '.join(current_chunk))
                        # Keep overlap
                        if overlap > 0 and len(current_chunk) > 1:
                            overlap_words = ' '.join(current_chunk).split()[-overlap:]
                            current_chunk = overlap_words
                            current_size = sum(len(w) for w in overlap_words)
                        else:
                            current_chunk = []
                            current_size = 0
                    
                    current_chunk.append(sentence)
                    current_size += len(sentence)
            else:
                # Check if adding this paragraph exceeds chunk size
                if current_size + para_size > chunk_size and current_chunk:
                    chunks.append(' '.join(current_chunk))
                    # Keep overlap
                    if overlap > 0 and len(current_chunk) > 1:
                        overlap_words = ' '.join(current_chunk).split()[-overlap:]
                        current_chunk = overlap_words
                        current_size = sum(len(w) for w in overlap_words)
                    else:
                        current_chunk = []
                        current_size = 0
                
                current_chunk.append(para)
                current_size += para_size
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks if chunks else [text]
    
    def update_document(self, file_path: str, force_update: bool = False):
        """Update an existing document in the knowledge base"""
        try:
            # Delete existing chunks from this source
            self.vector_store.delete_by_source(file_path)
            
            # Re-add the document
            self.onboard_text_files([file_path])
            logger.info(f"Updated document: {file_path}")
            
        except Exception as e:
            logger.error(f"Error updating document {file_path}: {e}")
            raise
    
    def remove_document(self, file_path: str):
        """Remove a document from the knowledge base"""
        try:
            self.vector_store.delete_by_source(file_path)
            logger.info(f"Removed document: {file_path}")
        except Exception as e:
            logger.error(f"Error removing document {file_path}: {e}")
            raise
    
    def create_backup(self) -> str:
        """Create a backup of the knowledge base"""
        return self.vector_store.create_backup()
    
    def get_status(self):
        """Get comprehensive knowledge base status"""
        info = self.vector_store.get_collection_info()
        logger.info(f"Knowledge base contains {info['document_count']} documents from {info['unique_sources']} sources")
        return info

# Quick setup function for marketing co-founders
def quick_setup():
    """Interactive setup for marketing co-founders"""
    print("🚀 Marketing Agent Data Onboarding")
    print("=" * 40)
    
    onboarder = DataOnboarder()
    
    # Get company info
    print("\n📊 Let's start with your company information:")
    company_data = {
        'name': input("Company name: "),
        'industry': input("Industry: "),
        'target_audience': input("Target audience: "),
        'value_proposition': input("Value proposition: "),
        'products_services': input("Key products/services: "),
        'brand_voice': input("Brand voice (professional/casual/friendly): ") or "professional",
        'competitors': input("Main competitors: ")
    }
    
    onboarder.onboard_company_info(company_data)
    
    # Check for existing files
    print("\n📁 Looking for marketing files in knowledge_base/...")
    kb_files = list(Path("knowledge_base").glob("*.txt"))
    if kb_files:
        print(f"Found {len(kb_files)} text files. Onboarding...")
        onboarder.onboard_text_files([str(f) for f in kb_files])
    else:
        print("No text files found. You can add .txt files to knowledge_base/ directory later.")
    
    # Show status
    status = onboarder.get_status()
    print(f"\n✅ Setup complete! Knowledge base now contains {status['document_count']} documents")
    print("\nYou can now run: python main.py")

if __name__ == "__main__":
    quick_setup()