#!/usr/bin/env python3
"""
Simple Marketing Assistant - Text-Only Interface

A simple command-line interface to interact with your marketing RAG system.
Perfect for quick marketing questions and content generation.
"""

import os
import asyncio
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

from rag.rag_system import MarketingRAGSystem

class SimpleMarketingAssistant:
    """Simple text-based marketing assistant"""
    
    def __init__(self):
        """Initialize the assistant"""
        print("🚀 Initializing Marketing Assistant...")
        try:
            self.rag_system = MarketingRAGSystem()
            print("✅ Marketing Assistant ready!")
        except Exception as e:
            print(f"❌ Error initializing: {e}")
            exit(1)
    
    def setup_knowledge_base(self):
        """Setup and index knowledge base"""
        print("\n📚 Setting up knowledge base...")
        result = self.rag_system.setup_knowledge_base()
        
        if result["status"] == "success":
            print(f"✅ {result['message']}")
        elif result["status"] == "warning":
            print(f"⚠️  {result['message']}")
            print("💡 Add .txt files to knowledge_base/ directory for better responses")
        else:
            print(f"❌ {result['message']}")
    
    def ask_question(self):
        """Interactive Q&A session"""
        print("\n💬 Ask me anything about marketing!")
        print("Type 'quit' to exit, 'menu' to return to main menu")
        
        while True:
            question = input("\n❓ Your question: ").strip()
            
            if question.lower() == 'quit':
                break
            elif question.lower() == 'menu':
                return
            elif not question:
                continue
            
            print("🤔 Thinking...")
            result = self.rag_system.ask_question(question)
            
            print(f"\n💡 Answer:")
            print(result["answer"])
            
            if result.get("sources"):
                print(f"\n📄 Sources: {', '.join(result['sources'])}")
    
    def generate_content(self):
        """Interactive content generation"""
        print("\n✍️  Content Generation")
        
        content_types = [
            "blog post", "newsletter", "social media post", 
            "campaign strategy", "email sequence", "landing page copy"
        ]
        
        print("Available content types:")
        for i, ct in enumerate(content_types, 1):
            print(f"  {i}. {ct.title()}")
        
        try:
            choice = int(input("\nSelect content type (1-6): ")) - 1
            if choice < 0 or choice >= len(content_types):
                print("❌ Invalid choice")
                return
            
            content_type = content_types[choice]
            
        except ValueError:
            print("❌ Please enter a number")
            return
        
        topic = input("📝 Topic: ").strip()
        if not topic:
            print("❌ Topic is required")
            return
        
        target_audience = input("🎯 Target audience: ").strip()
        if not target_audience:
            target_audience = "general audience"
        
        # Optional parameters
        additional_params = {}
        
        if content_type == "newsletter":
            tone = input("🎨 Tone (professional/casual/friendly) [professional]: ").strip()
            if tone:
                additional_params["tone"] = tone
        
        print("🎨 Generating content...")
        result = self.rag_system.generate_marketing_content(
            content_type=content_type,
            topic=topic,
            target_audience=target_audience,
            additional_params=additional_params if additional_params else None
        )
        
        print(f"\n📄 Generated {content_type.title()}:")
        print("=" * 50)
        print(result["content"])
        print("=" * 50)
        
        if result.get("sources"):
            print(f"\n📚 Based on: {', '.join(result['sources'])}")
        
        print(f"\n💾 Content saved to storage/outputs/")
    
    def add_document(self):
        """Add a new document to knowledge base"""
        print("\n📄 Add New Document")
        
        filename = input("📝 Filename (with .txt extension): ").strip()
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        print("📝 Enter your document content (press Ctrl+D when done):")
        print("=" * 50)
        
        content_lines = []
        try:
            while True:
                line = input()
                content_lines.append(line)
        except EOFError:
            pass
        
        content = '\n'.join(content_lines)
        
        if not content.strip():
            print("❌ No content provided")
            return
        
        print("💾 Adding document...")
        result = self.rag_system.add_company_document(content, filename)
        
        if result["status"] == "success":
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['message']}")
    
    def show_status(self):
        """Show system status"""
        print("\n📊 System Status")
        status = self.rag_system.get_system_status()
        
        if status["status"] == "operational":
            kb = status["knowledge_base"]
            outputs = status["outputs"]
            
            print(f"📚 Knowledge Base: {kb['documents']} documents, {kb['indexed_chunks']} chunks")
            print(f"📄 Generated Outputs: {outputs['count']} files")
            
            if outputs["recent"]:
                print(f"📝 Recent outputs: {', '.join(outputs['recent'])}")
        else:
            print(f"❌ System error: {status['message']}")
    
    def main_menu(self):
        """Main interactive menu"""
        print("\n" + "="*50)
        print("🎯 MARKETING ASSISTANT")
        print("="*50)
        
        while True:
            print("\nWhat would you like to do?")
            print("1. 💬 Ask a marketing question")
            print("2. ✍️  Generate marketing content")
            print("3. 📄 Add document to knowledge base")
            print("4. 📊 Show system status")
            print("5. 📚 Refresh knowledge base")
            print("6. 🚪 Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                self.ask_question()
            elif choice == '2':
                self.generate_content()
            elif choice == '3':
                self.add_document()
            elif choice == '4':
                self.show_status()
            elif choice == '5':
                self.setup_knowledge_base()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")

def main():
    """Main function"""
    # Check environment
    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ Error: GOOGLE_API_KEY not found in environment")
        print("Please add your Google API key to the .env file")
        return
    
    # Initialize assistant
    assistant = SimpleMarketingAssistant()
    
    # Setup knowledge base
    assistant.setup_knowledge_base()
    
    # Start interactive session
    assistant.main_menu()

if __name__ == "__main__":
    main()