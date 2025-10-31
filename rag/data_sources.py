"""
Data Sources Module - Simple Implementation

Handles basic data ingestion from files and text sources for the RAG system.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DataSource:
    """Simple data source handler for files and text"""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.knowledge_base_path.mkdir(exist_ok=True)
    
    def load_text_files(self) -> List[Dict[str, Any]]:
        """Load all text files from knowledge base"""
        documents = []
        
        for file_path in self.knowledge_base_path.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                documents.append({
                    "content": content,
                    "source": str(file_path),
                    "type": "text_file",
                    "filename": file_path.name
                })
                logger.info(f"Loaded {file_path.name}")
                
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
        
        return documents
    
    def add_text_document(self, content: str, filename: str) -> bool:
        """Add a new text document to knowledge base"""
        try:
            file_path = self.knowledge_base_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Added document: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error adding document {filename}: {e}")
            return False
    
    def get_document_count(self) -> int:
        """Get count of documents in knowledge base"""
        return len(list(self.knowledge_base_path.glob("*.txt")))
