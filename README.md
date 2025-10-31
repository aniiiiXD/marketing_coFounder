# Marketing Agent System

An AI-powered marketing automation system designed for marketing co-founders and teams. Get intelligent content creation, campaign analysis, and strategic insights using specialized AI agents that understand your business context.

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

## 🔧 Adding Your Marketing Data

### Method 1: Text Files
1. Add `.txt` files to `knowledge_base/` directory
2. Run `python data_onboarding.py` to index them
3. Agents will automatically use this knowledge

### Method 2: Structured Data
```python
from data_onboarding import DataOnboarder

onboarder = DataOnboarder()
onboarder.onboard_marketing_data({
    "campaign_name": "Q4 Launch",
    "target_ctr": "2.5%",
    "budget": "$50000"
}, "campaign_data")
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

### Generate a Content Campaign
```python
from agents.orchestrator import Orchestrator

orchestrator = Orchestrator()

result = await orchestrator.execute_workflow(
    "content_campaign",
    campaign_topic="Remote Work Productivity",
    target_audience="Freelancers and digital nomads, 25-40",
    timeframe="30 days"
)
```

### Analyze Campaign Performance
```python
analysis = await orchestrator.execute_workflow(
    "analyze_campaign_performance",
    campaign_data={
        "impressions": 100000,
        "clicks": 5000,
        "conversions": 250,
        "revenue": 50000
    }
)
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

## 🤝 Support

For marketing co-founders who need help:
1. Check the troubleshooting section above
2. Review the example usage patterns
3. Start with the quick setup script: `python data_onboarding.py`

## 📈 Next Steps

1. **Add More Data**: Drop marketing documents into `knowledge_base/`
2. **Customize Agents**: Edit configurations in `config/`
3. **Integrate APIs**: Connect your CRM, analytics tools, and social media
4. **Scale Up**: Use the Kubernetes deployment for production

Built for marketing teams who want AI that understands their business context and delivers actionable results.
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