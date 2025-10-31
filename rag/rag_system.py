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
    
    def ask_question(self, question: str, save_output: bool = True) -> Dict[str, Any]:
        """Ask a marketing question and get context-aware answer"""
        try:
            # Search for relevant context
            relevant_docs = self.vector_store.search(question, n_results=5)
            
            # Extract context
            context = [doc["document"] for doc in relevant_docs]
            
            # Generate response
            response = self.llm_service.analyze_with_context(question, context)
            
            # Prepare result
            result = {
                "question": question,
                "answer": response,
                "context_used": len(context),
                "sources": [doc["metadata"]["filename"] for doc in relevant_docs],
                "timestamp": datetime.now().isoformat()
            }
            
            # Save output if requested
            if save_output:
                filename = f"qa_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                output_content = f"Question: {question}\n\nAnswer: {response}\n\nSources: {', '.join(result['sources'])}"
                self.storage.save_output(output_content, filename)
            
            logger.info(f"Answered question using {len(context)} context pieces")
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
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        try:
            vector_info = self.vector_store.get_collection_info()
            document_count = self.data_source.get_document_count()
            outputs = self.storage.list_outputs()
            
            return {
                "knowledge_base": {
                    "documents": document_count,
                    "indexed_chunks": vector_info["document_count"]
                },
                "outputs": {
                    "count": len(outputs),
                    "recent": outputs[-5:] if outputs else []
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
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            if chunk_words:
                chunks.append(' '.join(chunk_words))
        
        return chunks if chunks else [text]