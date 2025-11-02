"""
Vector Store Implementation using ChromaDB for RAG system
Enhanced with document management, backup, and improved search
"""

import chromadb
from chromadb.config import Settings
import os  
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB vector store"""
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="marketing_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
        self.backup_dir = Path(persist_directory).parent / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        logger.info(f"Vector store initialized at {persist_directory}")
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """Add documents to the vector store with duplicate detection"""
        try:
            # Check for existing documents
            existing_ids = self.get_existing_ids()
            new_docs, new_metas, new_ids = [], [], []
            
            for doc, meta, doc_id in zip(documents, metadatas, ids):
                if doc_id not in existing_ids:
                    new_docs.append(doc)
                    new_metas.append({**meta, "last_updated": datetime.now().isoformat()})
                    new_ids.append(doc_id)
                else:
                    logger.debug(f"Skipping duplicate document: {doc_id}")
            
            if new_docs:
                self.collection.add(
                    documents=new_docs,
                    metadatas=new_metas,
                    ids=new_ids
                )
                logger.info(f"Added {len(new_docs)} new documents to vector store")
            else:
                logger.info("No new documents to add")
                
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def search(self, query: str, n_results: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Enhanced search with filtering and better ranking"""
        try:
            # Build where clause for filtering
            where_clause = {}
            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        where_clause[key] = {"$in": value}
                    else:
                        where_clause[key] = {"$eq": value}
            
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause if where_clause else None
            )
            
            # Format results with enhanced metadata
            formatted_results = []
            for i in range(len(results['documents'][0])):
                result = {
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i],
                    'id': results['ids'][0][i],
                    'relevance_score': 1 - results['distances'][0][i]  # Convert distance to relevance
                }
                formatted_results.append(result)
            
            # Sort by relevance score (higher is better)
            formatted_results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def update_document(self, doc_id: str, document: str, metadata: Dict[str, Any]):
        """Update an existing document"""
        try:
            metadata["last_updated"] = datetime.now().isoformat()
            self.collection.update(
                ids=[doc_id],
                documents=[document],
                metadatas=[metadata]
            )
            logger.info(f"Updated document: {doc_id}")
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {e}")
            raise
    
    def delete_documents(self, ids: List[str]):
        """Delete documents by IDs"""
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents")
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            raise
    
    def delete_by_source(self, source: str):
        """Delete all documents from a specific source"""
        try:
            self.collection.delete(where={"source": {"$eq": source}})
            logger.info(f"Deleted all documents from source: {source}")
        except Exception as e:
            logger.error(f"Error deleting documents from source {source}: {e}")
            raise
    
    def get_existing_ids(self) -> Set[str]:
        """Get all existing document IDs"""
        try:
            results = self.collection.get()
            return set(results['ids'])
        except Exception as e:
            logger.error(f"Error getting existing IDs: {e}")
            return set()
    
    def export_data(self, export_path: str) -> Dict[str, Any]:
        """Export all data to JSON file"""
        try:
            results = self.collection.get()
            export_data = {
                "documents": results['documents'],
                "metadatas": results['metadatas'],
                "ids": results['ids'],
                "exported_at": datetime.now().isoformat(),
                "collection_name": self.collection.name
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported {len(results['documents'])} documents to {export_path}")
            return {"status": "success", "count": len(results['documents']), "path": export_path}
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return {"status": "error", "message": str(e)}
    
    def import_data(self, import_path: str) -> Dict[str, Any]:
        """Import data from JSON file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.collection.add(
                documents=data['documents'],
                metadatas=data['metadatas'],
                ids=data['ids']
            )
            
            logger.info(f"Imported {len(data['documents'])} documents from {import_path}")
            return {"status": "success", "count": len(data['documents'])}
        except Exception as e:
            logger.error(f"Error importing data: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_backup(self) -> str:
        """Create a backup of the current vector store"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}.json"
            
            result = self.export_data(str(backup_path))
            if result["status"] == "success":
                logger.info(f"Backup created: {backup_path}")
                return str(backup_path)
            else:
                raise Exception(result["message"])
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get comprehensive information about the collection"""
        try:
            count = self.collection.count()
            results = self.collection.get(limit=1)  # Get sample for metadata analysis
            
            # Analyze metadata
            sources = set()
            content_types = set()
            if results['metadatas']:
                for meta in results['metadatas']:
                    if 'source' in meta:
                        sources.add(meta['source'])
                    if 'type' in meta:
                        content_types.add(meta['type'])
            
            return {
                "document_count": count,
                "collection_name": self.collection.name,
                "unique_sources": len(sources),
                "content_types": list(content_types),
                "backup_count": len(list(self.backup_dir.glob("backup_*.json")))
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {"document_count": 0, "collection_name": self.collection.name}