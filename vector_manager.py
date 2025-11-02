#!/usr/bin/env python3
"""
Vector Store Manager - Fresh Initialization and Data Loading

This module handles fresh vector store initialization, data loading, and integration.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manages vector store initialization and data loading"""
    
    def __init__(self, chroma_path: str = "./chroma_db", output_dir: str = "./outputs"):
        self.chroma_path = Path(chroma_path)
        self.output_dir = Path(output_dir)
        self.knowledge_base_dir = Path("knowledge_base")
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.rag_system = None
        self.vector_store = None
        
    def clear_vector_store(self):
        """Clear existing vector store completely"""
        try:
            if self.chroma_path.exists():
                shutil.rmtree(self.chroma_path)
                logger.info(f"✅ Cleared existing vector store at {self.chroma_path}")
            else:
                logger.info("ℹ️  No existing vector store found")
                
        except Exception as e:
            logger.error(f"❌ Error clearing vector store: {e}")
            raise
    
    def initialize_fresh_vector_store(self):
        """Initialize a completely fresh vector store"""
        try:
            # Clear existing store
            self.clear_vector_store()
            
            # Import and initialize RAG system
            from rag.rag_system import MarketingRAGSystem
            self.rag_system = MarketingRAGSystem()
            self.vector_store = self.rag_system.vector_store
            
            logger.info("✅ Fresh vector store initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing vector store: {e}")
            return False
    
    def load_knowledge_base_data(self):
        """Load all data from knowledge base into vector store"""
        try:
            logger.info("📊 Loading knowledge base data...")
            
            # Setup knowledge base
            setup_result = self.rag_system.setup_knowledge_base()
            
            if setup_result["status"] == "success":
                logger.info(f"✅ Loaded {setup_result['document_count']} documents into {setup_result['chunk_count']} chunks")
                
                # Save loading report
                self.save_output({
                    "operation": "knowledge_base_loading",
                    "timestamp": datetime.now().isoformat(),
                    "result": setup_result
                }, "knowledge_base_loading_report.json")
                
                return setup_result
            else:
                logger.warning(f"⚠️  Knowledge base loading: {setup_result['message']}")
                return setup_result
                
        except Exception as e:
            logger.error(f"❌ Error loading knowledge base: {e}")
            return {"status": "error", "message": str(e)}
    
    def verify_data_loading(self):
        """Verify that data was loaded correctly"""
        try:
            logger.info("🔍 Verifying data loading...")
            
            # Get collection info
            info = self.vector_store.get_collection_info()
            
            # Test search functionality
            test_results = self.vector_store.search("company", n_results=3)
            
            verification = {
                "collection_info": info,
                "test_search_results": len(test_results),
                "sample_documents": [r["document"][:100] + "..." for r in test_results[:2]],
                "verification_status": "success" if info["document_count"] > 0 else "failed"
            }
            
            logger.info(f"✅ Verification complete: {info['document_count']} documents indexed")
            
            # Save verification report
            self.save_output(verification, "data_verification_report.json")
            
            return verification
            
        except Exception as e:
            logger.error(f"❌ Error verifying data: {e}")
            return {"verification_status": "error", "message": str(e)}
    
    def get_rag_system(self):
        """Get the initialized RAG system"""
        return self.rag_system
    
    def save_output(self, data: Any, filename: str):
        """Save output data to file"""
        try:
            output_path = self.output_dir / filename
            
            if isinstance(data, dict) or isinstance(data, list):
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            
            logger.info(f"💾 Saved output to {output_path}")
            
        except Exception as e:
            logger.error(f"❌ Error saving output: {e}")
    
    def print_status(self):
        """Print current system status"""
        try:
            if not self.rag_system:
                print("❌ RAG system not initialized")
                return
            
            status = self.rag_system.get_system_status()
            
            print("\n" + "="*60)
            print("📊 VECTOR STORE STATUS")
            print("="*60)
            print(f"📁 Source Documents: {status['knowledge_base']['source_documents']}")
            print(f"🔍 Indexed Chunks: {status['knowledge_base']['indexed_chunks']}")
            print(f"📂 Unique Sources: {status['knowledge_base']['unique_sources']}")
            print(f"📄 Output Files: {status['outputs']['count']}")
            print(f"🟢 Status: {status['status']}")
            print("="*60)
            
            # Save status report
            self.save_output(status, "system_status_report.json")
            
        except Exception as e:
            logger.error(f"❌ Error getting status: {e}")

def main():
    """Main function for testing vector store manager"""
    print("🚀 Vector Store Manager - Fresh Initialization")
    print("="*60)
    
    manager = VectorStoreManager()
    
    # Step 1: Initialize fresh vector store
    print("\n📋 Step 1: Initializing fresh vector store...")
    if manager.initialize_fresh_vector_store():
        print("✅ Vector store initialized successfully")
    else:
        print("❌ Failed to initialize vector store")
        return
    
    # Step 2: Load knowledge base data
    print("\n📋 Step 2: Loading knowledge base data...")
    load_result = manager.load_knowledge_base_data()
    if load_result["status"] == "success":
        print(f"✅ Loaded {load_result['document_count']} documents")
    else:
        print(f"⚠️  Loading result: {load_result['message']}")
    
    # Step 3: Verify data loading
    print("\n📋 Step 3: Verifying data loading...")
    verification = manager.verify_data_loading()
    if verification["verification_status"] == "success":
        print("✅ Data verification successful")
    else:
        print("❌ Data verification failed")
    
    # Step 4: Print status
    print("\n📋 Step 4: System status...")
    manager.print_status()
    
    print("\n🎉 Vector store setup complete!")

if __name__ == "__main__":
    main()