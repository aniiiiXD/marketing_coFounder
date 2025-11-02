from rag.rag_system import MarketingRAGSystem

# Quick test
rag = MarketingRAGSystem()
result = rag.ask_question("What is Eterna?")
print("Answer:", result['answer'][:200])
print("Sources:", result['sources'])