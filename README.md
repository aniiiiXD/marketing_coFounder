# Marketing Agent System

An AI-powered marketing automation system designed for marketing co-founders and teams. Get intelligent content creation, campaign analysis, and strategic insights using specialized AI agents that understand your business context.

## ✨ Enhanced Features

- **Smart Document Management**: Add, update, and remove documents dynamically
- **Semantic Search**: Advanced search with relevance scoring and filtering
- **Automatic Backups**: Built-in backup and export capabilities
- **Duplicate Prevention**: Intelligent detection prevents re-adding same content
- **Enhanced Chunking**: Semantic text splitting preserves context and meaning
- **Metadata Filtering**: Search by content type, source, or custom attributes

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
 
### 2. Set Up Your Knowledge Base
```bash
python data_onboarding.py
```
This interactive script will:
- Collect your company information
- Set up your marketing knowledge base
- Index any existing marketing documents

### 3. Start Using the Assistant
```bash
python simple_marketing_assistant.py
```

**OR** run the full agent system:
```bash
python main.py
```

That's it! Your marketing assistant is ready to help with questions and content generation.

## 🎯 What You Can Do

### Content Campaign Generation
Create complete marketing campaigns including:
- Content strategy and ideas
- Newsletter content
- Marketing presentations
- All tailored to your specific business and audience

### Campaign Performance Analysis
- Upload campaign data
- Get detailed performance insights
- Receive actionable recommendations
- Generate executive summary presentations

### Knowledge-Aware Marketing
All agents use your company data to provide:
- Brand-consistent content
- Industry-specific insights
- Competitor-aware strategies
- Audience-targeted messaging

## 📁 Project Structure

```
marketing-agent/
├── agents/                 # Specialized AI agents
│   ├── analytics_agent.py
│   ├── content_planning_agent.py
│   ├── newsletter_agent.py
│   └── presentation_agent.py
├── rag/                   # Knowledge retrieval system
├── knowledge_base/        # Your marketing documents (add files here)
├── config/               # Agent configurations
├── data_onboarding.py    # Easy data setup script
└── main.py              # Run this to start
```

## 🔧 Managing Your Marketing Data

### Adding Documents
```python
from data_onboarding import DataOnboarder

onboarder = DataOnboarder()

# Method 1: Text files (automatic indexing)
onboarder.onboard_text_files(["knowledge_base/strategy.txt", "knowledge_base/brand_guide.txt"])

# Method 2: Structured data
onboarder.onboard_marketing_data({
    "campaign_name": "Q4 Launch",
    "target_ctr": "2.5%",
    "budget": "$50000"
}, "campaign_data")

# Method 3: Company information
onboarder.onboard_company_info({
    "name": "Your Company",
    "industry": "SaaS",
    "target_audience": "Small businesses"
})
```

### Document Management
```python
# Update existing document
onboarder.update_document("knowledge_base/strategy.txt")

# Remove document
onboarder.remove_document("knowledge_base/old_strategy.txt")

# Create backup
backup_path = onboarder.create_backup()
print(f"Backup saved to: {backup_path}")

# Check status
status = onboarder.get_status()
print(f"Knowledge base: {status['document_count']} documents from {status['unique_sources']} sources")
```

## 🎛️ Configuration

### Environment Setup
Edit `.env` file:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### Agent Customization
Edit `config/agents_config.json` to modify agent behavior and capabilities.

## 💡 Example Usage

### Enhanced RAG System
```python
from rag.rag_system import MarketingRAGSystem

rag = MarketingRAGSystem()

# Ask questions with filtering
result = rag.ask_question(
    "How should I price my SaaS product?",
    filters={"type": "company_info", "source": "pricing_strategy.txt"}
)
print(f"Answer: {result['answer']}")
print(f"Relevance: {result['avg_relevance']:.3f}")
print(f"Sources: {result['sources']}")

# Search documents with detailed results
search_results = rag.search_documents(
    "content marketing strategy",
    filters={"type": "text_file"},
    n_results=5
)

# Generate content with context
content = rag.generate_marketing_content(
    content_type="blog_post",
    topic="Remote Work Productivity",
    target_audience="Freelancers and digital nomads, 25-40"
)
```

### Document Management
```python
# Add new document
rag.add_company_document("Our new product strategy...", "product_strategy_2024.txt")

# Update existing document
rag.update_document("old_strategy.txt", "Updated strategy content...")

# Remove document
rag.remove_document("outdated_info.txt")

# Create backup
backup_result = rag.create_backup()
print(f"Backup created: {backup_result['backup_path']}")

# Get comprehensive status
status = rag.get_system_status()
print(f"System status: {status['status']}")
print(f"Capabilities: {status['capabilities']}")
```

### Advanced Search Features
```python
from rag.vector_store import VectorStore

vector_store = VectorStore()

# Search with filters and relevance scoring
results = vector_store.search(
    "pricing strategy",
    n_results=10,
    filters={"type": ["company_info", "text_file"], "source": "strategy.txt"}
)

for result in results:
    print(f"Relevance: {result['relevance_score']:.3f}")
    print(f"Source: {result['metadata']['source']}")
    print(f"Content: {result['document'][:100]}...")

# Export data for backup
export_result = vector_store.export_data("backup_2024.json")
print(f"Exported {export_result['count']} documents")
```

## 🚀 Production Deployment

### Docker (Recommended)
```bash
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f infra/k8s/
```

## 🔍 Troubleshooting

**"No module named 'chromadb'"**
- Run: `pip install -r requirements.txt`

**"GOOGLE_API_KEY not set"**
- Add your Google API key to the `.env` file

**Empty knowledge base**
- Run `python data_onboarding.py` to add your company data
- Add `.txt` files to `knowledge_base/` directory

**Duplicate documents**
- The system automatically prevents duplicates based on document IDs
- Use `update_document()` instead of re-adding existing files

**Low relevance scores**
- Check if your query matches the content in your knowledge base
- Use filters to narrow search to specific content types
- Add more relevant documents to improve context

**Backup/restore issues**
- Backups are stored in `./backups/` directory
- Use `vector_store.export_data()` for manual exports
- Import with `vector_store.import_data()` to restore

## 🤝 Support

For marketing co-founders who need help:
1. Check the troubleshooting section above
2. Review the example usage patterns
3. Start with the quick setup script: `python data_onboarding.py`

## 📈 Advanced Features

### Knowledge Base Management
- **Smart Chunking**: Semantic text splitting preserves context across chunks
- **Relevance Scoring**: Every search result includes confidence scores
- **Metadata Filtering**: Search by content type, source, date, or custom attributes
- **Duplicate Prevention**: Automatic detection prevents re-indexing same content
- **Version Control**: Track document updates with timestamps

### Search & Retrieval
- **Hybrid Search**: Combines semantic similarity with metadata filtering  
- **Context Preservation**: Overlapping chunks maintain meaning across boundaries
- **Source Attribution**: Every answer includes source documents and relevance scores
- **Query Expansion**: Enhanced search understanding for better results

### Data Management
- **CRUD Operations**: Add, update, delete documents without rebuilding
- **Backup & Export**: Automatic backups with JSON export/import
- **Status Monitoring**: Comprehensive system health and usage analytics
- **Batch Processing**: Efficient handling of multiple document operations

### Production Features
- **Error Handling**: Graceful degradation with detailed error messages
- **Logging**: Comprehensive logging for debugging and monitoring
- **Performance**: Optimized chunking and search for large knowledge bases
- **Scalability**: Designed for growing document collections

## 📈 Next Steps

1. **Enhance Knowledge Base**: Use the new document management features to keep content fresh
2. **Leverage Filtering**: Use metadata filters for more precise search results
3. **Monitor Performance**: Check relevance scores to optimize your content
4. **Create Backups**: Set up regular backups using the built-in export functionality
5. **Scale Intelligently**: Use the enhanced chunking for better context preservation

Built for marketing teams who want AI that understands their business context and delivers actionable results with enterprise-grade reliability.
## 🎯
 Simple Text-Only Usage

For immediate marketing assistance without complexity:

```bash
python simple_marketing_assistant.py
```

This gives you:
- **Interactive Q&A**: Ask any marketing question
- **Content Generation**: Create blogs, newsletters, social posts, campaigns
- **Knowledge-Aware**: Uses your company data for context
- **Text Output**: Clean, ready-to-use content
- **Local Storage**: All outputs saved to `storage/outputs/`

### Example Session:
```
🎯 MARKETING ASSISTANT
1. 💬 Ask a marketing question
2. ✍️  Generate marketing content

❓ Your question: How should I position our SaaS product for small businesses?

💡 Answer: Based on your company information, here's how to position your SaaS product for small businesses...

📄 Sources: company_profile.txt, marketing_best_practices.txt
```