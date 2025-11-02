"""
Complete RAG System - Ready to Use

This is the main RAG system that combines all components for marketing assistance.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .vector_store import VectorStore
from .data_sources import DataSource
from .llm_service import LLMService
from .storage import StorageService

logger = logging.getLogger(__name__)

class MarketingRAGSystem:
    """Complete RAG system for marketing assistance"""
    
    def __init__(self):
        """Initialize all RAG components"""
        self.vector_store = VectorStore()
        self.data_source = DataSource()
        self.llm_service = LLMService()
        self.storage = StorageService()
        
        logger.info("Marketing RAG System initialized")
    
    def setup_knowledge_base(self) -> Dict[str, Any]:
        """Load and index all available documents"""
        try:
            # Load documents from knowledge base
            documents = self.data_source.load_text_files()
            
            if not documents:
                logger.warning("No documents found in knowledge base")
                return {"status": "warning", "message": "No documents found", "count": 0}
            
            # Prepare for vector store
            texts = []
            metadatas = []
            ids = []
            
            for i, doc in enumerate(documents):
                # Split document into chunks
                chunks = self._chunk_text(doc["content"])
                
                for j, chunk in enumerate(chunks):
                    texts.append(chunk)
                    metadatas.append({
                        "source": doc["source"],
                        "filename": doc["filename"],
                        "chunk_id": j,
                        "type": doc["type"],
                        "indexed_at": datetime.now().isoformat()
                    })
                    ids.append(f"{doc['filename']}_{j}")
            
            # Add to vector store
            self.vector_store.add_documents(texts, metadatas, ids)
            
            result = {
                "status": "success",
                "message": f"Indexed {len(documents)} documents into {len(texts)} chunks",
                "document_count": len(documents),
                "chunk_count": len(texts)
            }
            
            logger.info(result["message"])
            return result
            
        except Exception as e:
            error_msg = f"Error setting up knowledge base: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
    
    def ask_question(self, question: str, filters: Optional[Dict[str, Any]] = None, save_output: bool = True) -> Dict[str, Any]:
        """Ask a marketing question with enhanced search and context"""
        try:
            # Search for relevant context with optional filters
            relevant_docs = self.vector_store.search(question, n_results=5, filters=filters)
            
            # Extract context and rank by relevance
            context_pieces = []
            sources = []
            relevance_scores = []
            
            for doc in relevant_docs:
                context_pieces.append(doc["document"])
                sources.append(doc["metadata"].get("filename", doc["metadata"].get("source", "unknown")))
                relevance_scores.append(doc.get("relevance_score", 0))
            
            # Generate response
            response = self.llm_service.analyze_with_context(question, context_pieces)
            
            # Prepare enhanced result
            result = {
                "question": question,
                "answer": response,
                "context_used": len(context_pieces),
                "sources": sources,
                "relevance_scores": relevance_scores,
                "avg_relevance": sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0,
                "filters_applied": filters or {},
                "timestamp": datetime.now().isoformat()
            }
            
            # Save output if requested
            if save_output:
                filename = f"qa_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                output_content = f"Question: {question}\n\nAnswer: {response}\n\nSources: {', '.join(sources)}\nAverage Relevance: {result['avg_relevance']:.3f}"
                self.storage.save_output(output_content, filename)
            
            logger.info(f"Answered question using {len(context_pieces)} context pieces (avg relevance: {result['avg_relevance']:.3f})")
            return result
            
        except Exception as e:
            error_msg = f"Error answering question: {e}"
            logger.error(error_msg)
            return {
                "question": question,
                "answer": f"I apologize, but I encountered an error: {error_msg}",
                "error": True
            }
    
    def generate_marketing_content(
        self, 
        content_type: str, 
        topic: str, 
        target_audience: str,
        additional_params: Optional[Dict[str, Any]] = None,
        save_output: bool = True
    ) -> Dict[str, Any]:
        """Generate marketing content with company context"""
        try:
            # Search for relevant company context
            search_query = f"{topic} {target_audience} {content_type}"
            relevant_docs = self.vector_store.search(search_query, n_results=3)
            context = [doc["document"] for doc in relevant_docs]
            
            # Generate content
            content = self.llm_service.generate_marketing_content(
                content_type=content_type,
                topic=topic,
                target_audience=target_audience,
                context=context,
                additional_params=additional_params
            )
            
            result = {
                "content_type": content_type,
                "topic": topic,
                "target_audience": target_audience,
                "content": content,
                "context_used": len(context),
                "sources": [doc["metadata"]["filename"] for doc in relevant_docs],
                "timestamp": datetime.now().isoformat()
            }
            
            # Save output if requested
            if save_output:
                filename = f"{content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                self.storage.save_output(content, filename)
                self.storage.save_json(result, f"metadata_{filename}")
            
            logger.info(f"Generated {content_type} content for {topic}")
            return result
            
        except Exception as e:
            error_msg = f"Error generating content: {e}"
            logger.error(error_msg)
            return {
                "content_type": content_type,
                "topic": topic,
                "content": f"Error generating content: {error_msg}",
                "error": True
            }
    
    def add_company_document(self, content: str, filename: str) -> Dict[str, Any]:
        """Add a new document to the knowledge base"""
        try:
            # Save to data source
            success = self.data_source.add_text_document(content, filename)
            
            if success:
                # Re-index the knowledge base
                setup_result = self.setup_knowledge_base()
                return {
                    "status": "success",
                    "message": f"Added document {filename} and re-indexed knowledge base",
                    "setup_result": setup_result
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to add document {filename}"
                }
                
        except Exception as e:
            error_msg = f"Error adding document: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
    
    def update_document(self, filename: str, new_content: str) -> Dict[str, Any]:
        """Update an existing document in the knowledge base"""
        try:
            # Update in data source
            success = self.data_source.update_text_document(new_content, filename)
            
            if success:
                # Remove old chunks and add new ones
                self.vector_store.delete_by_source(filename)
                
                # Re-chunk and add updated content
                chunks = self._chunk_text(new_content)
                texts, metadatas, ids = [], [], []
                
                for i, chunk in enumerate(chunks):
                    texts.append(chunk)
                    metadatas.append({
                        "source": filename,
                        "filename": filename,
                        "chunk_id": i,
                        "type": "text_file",
                        "indexed_at": datetime.now().isoformat()
                    })
                    ids.append(f"{filename}_{i}")
                
                self.vector_store.add_documents(texts, metadatas, ids)
                
                return {
                    "status": "success",
                    "message": f"Updated document {filename} with {len(chunks)} chunks"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to update document {filename}"
                }
                
        except Exception as e:
            error_msg = f"Error updating document: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
    
    def remove_document(self, filename: str) -> Dict[str, Any]:
        """Remove a document from the knowledge base"""
        try:
            # Remove from vector store
            self.vector_store.delete_by_source(filename)
            
            # Remove from data source
            success = self.data_source.remove_text_document(filename)
            
            return {
                "status": "success" if success else "partial",
                "message": f"Removed document {filename} from knowledge base"
            }
                
        except Exception as e:
            error_msg = f"Error removing document: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
    
    def create_backup(self) -> Dict[str, Any]:
        """Create a backup of the entire knowledge base"""
        try:
            backup_path = self.vector_store.create_backup()
            return {
                "status": "success",
                "message": f"Backup created successfully",
                "backup_path": backup_path
            }
        except Exception as e:
            error_msg = f"Error creating backup: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
    
    def search_documents(self, query: str, filters: Optional[Dict[str, Any]] = None, n_results: int = 10) -> Dict[str, Any]:
        """Search documents with detailed results"""
        try:
            results = self.vector_store.search(query, n_results=n_results, filters=filters)
            
            return {
                "query": query,
                "filters": filters or {},
                "results_count": len(results),
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error searching documents: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            vector_info = self.vector_store.get_collection_info()
            document_count = self.data_source.get_document_count()
            outputs = self.storage.list_outputs()
            
            return {
                "knowledge_base": {
                    "source_documents": document_count,
                    "indexed_chunks": vector_info["document_count"],
                    "unique_sources": vector_info.get("unique_sources", 0),
                    "content_types": vector_info.get("content_types", []),
                    "backup_count": vector_info.get("backup_count", 0)
                },
                "outputs": {
                    "count": len(outputs),
                    "recent": outputs[-5:] if outputs else []
                },
                "capabilities": {
                    "document_management": True,
                    "semantic_search": True,
                    "backup_restore": True,
                    "content_filtering": True,
                    "relevance_scoring": True
                },
                "status": "operational",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Enhanced semantic text chunking with overlap"""
        # First try to split by paragraphs for better semantic coherence
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
            para_words = para.split()
            para_size = len(para_words)
            
            # If single paragraph is too large, split it
            if para_size > chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_size = 0
                
                # Split large paragraph with overlap
                for i in range(0, para_size, chunk_size - overlap):
                    chunk_words = para_words[i:i + chunk_size]
                    if chunk_words:
                        chunks.append(' '.join(chunk_words))
            else:
                # Check if adding this paragraph exceeds chunk size
                if current_size + para_size > chunk_size and current_chunk:
                    chunks.append(' '.join(current_chunk))
                    # Keep overlap from previous chunk
                    if overlap > 0 and current_size > overlap:
                        overlap_words = current_chunk[-overlap:]
                        current_chunk = overlap_words
                        current_size = len(overlap_words)
                    else:
                        current_chunk = []
                        current_size = 0
                
                current_chunk.extend(para_words)
                current_size += para_size
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks if chunks else [text]