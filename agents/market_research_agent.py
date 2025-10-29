"""
Market Research Agent

Responsible for gathering and analyzing market data, including:
- Competitor analysis and benchmarking
- Industry trend identification
- Market segmentation and targeting
- Customer behavior analysis
- Sentiment analysis from social media and reviews

This agent uses Google's Gemini model to provide actionable market insights
that inform content strategy and campaign decisions.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from .base_agent import BaseAgent
from .models import MarketAnalysisResponse, Trend, Insight, Recommendation

class MarketResearchAgent(BaseAgent[MarketAnalysisResponse]):
    """
    Market Research Agent
    
    A specialized AI agent for conducting comprehensive market research and analysis.
    Uses Google's Gemini model to generate insights from market data.
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash", 
                 temperature: float = 0.3, 
                 max_tokens: int = 2000):
        """
        Initialize the Market Research Agent.
        
        Args:
            model_name: The name of the Gemini model to use
            temperature: Controls randomness in the response (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate in the response
        """
        super().__init__(model_name, temperature, max_tokens)
    
    def get_system_instruction(self) -> str:
        """
        Define the system instruction for the market research agent.
        """
        return """
        You are an expert market research analyst with deep knowledge of market trends,
        competitive analysis, and consumer behavior. Your role is to provide 
        data-driven insights and strategic recommendations based on market research.
        
        Your responses must be structured as valid JSON objects that follow the 
        MarketAnalysisResponse schema. Include all required fields and ensure 
        proper formatting of dates, numbers, and nested objects.
        """
        
    def get_response_model(self) -> type[MarketAnalysisResponse]:
        """
        Return the response model for this agent.
        """
        return MarketAnalysisResponse
    
    def analyze_market(self, query: str, **kwargs) -> MarketAnalysisResponse:
        """
        Conduct comprehensive market analysis based on the given query.
        
        Args:
            query: Market research question or topic to analyze
            **kwargs: Additional arguments to override default config
            
        Returns:
            MarketAnalysisResponse: Structured market analysis with trends, insights, and recommendations
            
        Example:
            {
                "executive_summary": "...",
                "market_size": {"value": 1000000000, "unit": "USD", "growth_rate": 0.12},
                "trends": [
                    {
                        "name": "Trend 1",
                        "description": "...",
                        "impact": "...",
                        "confidence": 0.9
                    }
                ],
                "key_players": [{"name": "Company A", "market_share": 0.25}],
                "opportunities": ["...", "..."],
                "challenges": ["...", "..."],
                "recommendations": [
                    {
                        "action": "...",
                        "rationale": "...",
                        "priority": "high",
                        "expected_impact": "..."
                    }
                ],
                "sources": ["source1.com", "source2.org"]
            }
        """
        response_format = {
            "type": "object",
            "properties": {
                "executive_summary": {"type": "string"},
                "market_size": {
                    "type": "object",
                    "properties": {
                        "value": {"type": "number"},
                        "unit": {"type": "string"},
                        "growth_rate": {"type": "number"}
                    },
                    "required": ["value", "unit"]
                },
                "trends": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "impact": {"type": "string"},
                            "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                        },
                        "required": ["name", "description", "impact", "confidence"]
                    }
                },
                "key_players": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "market_share": {"type": "number"},
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "weaknesses": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["name"]
                    }
                },
                "opportunities": {"type": "array", "items": {"type": "string"}},
                "challenges": {"type": "array", "items": {"type": "string"}},
                "recommendations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string"},
                            "rationale": {"type": "string"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                            "expected_impact": {"type": "string"}
                        },
                        "required": ["action", "rationale", "priority", "expected_impact"]
                    }
                },
                "sources": {"type": "array", "items": {"type": "string"}}
            },
            "required": [
                "executive_summary", "market_size", "trends", "key_players",
                "opportunities", "challenges", "recommendations", "sources"
            ]
        }
        
        prompt = f"""
        Conduct a comprehensive market analysis for: {query}
        
        Your analysis should include:
        1. Executive summary of key findings
        2. Market size and growth projections
        3. Current and emerging market trends
        4. Analysis of key players and competitive landscape
        5. Identified opportunities and challenges
        6. Strategic recommendations
        7. List of sources and references
        
        Be specific, data-driven, and provide actionable insights.
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def generate_research_report(self, topic: str, context: str = None, **kwargs) -> dict:
        """
        Generate a comprehensive market research report on the given topic.
        
        Args:
            topic: The main topic of the research
            context: Optional additional context or specific aspects to focus on
            **kwargs: Additional arguments to override default config
            
        Returns:
            dict: Structured research report with detailed sections
            
        Example:
            {
                "executive_summary": "Brief summary of the report",
                "market_overview": "Detailed market analysis",
                "competitive_analysis": "Analysis of competitors",
                "consumer_insights": "Key consumer behavior insights",
                "trends": ["Trend 1", "Trend 2", ...],
                "opportunities": ["Opportunity 1", ...],
                "challenges": ["Challenge 1", ...],
                "recommendations": ["Recommendation 1", ...],
                "conclusion": "Summary of findings and final thoughts"
            }
        """
        response_format = {
            "type": "object",
            "properties": {
                "executive_summary": {"type": "string"},
                "market_overview": {"type": "string"},
                "competitive_analysis": {"type": "string"},
                "consumer_insights": {"type": "string"},
                "trends": {"type": "array", "items": {"type": "string"}},
                "opportunities": {"type": "array", "items": {"type": "string"}},
                "challenges": {"type": "array", "items": {"type": "string"}},
                "recommendations": {"type": "array", "items": {"type": "string"}},
                "conclusion": {"type": "string"}
            },
            "required": [
                "executive_summary", "market_overview", "competitive_analysis",
                "consumer_insights", "trends", "opportunities", "challenges",
                "recommendations", "conclusion"
            ]
        }
        
        prompt = f"""
        Generate a comprehensive market research report about: {topic}
        """
        
        if context:
            prompt += f"\nFocus specifically on: {context}"
            
        prompt += """
        
        The report should include the following sections:
        1. Executive Summary: Brief overview of key findings
        2. Market Overview: Current state of the market
        3. Competitive Analysis: Analysis of key competitors
        4. Consumer Insights: Key findings about consumer behavior
        5. Trends: Current and emerging trends
        6. Opportunities: Potential opportunities in the market
        7. Challenges: Key challenges to be aware of
        8. Recommendations: Strategic recommendations
        9. Conclusion: Summary and final thoughts
        """
        
        # Use higher temperature and more tokens for detailed reports by default
        report_kwargs = {
            'temperature': 0.5,
            'max_tokens': 4000,
            **kwargs  # Allow overriding defaults
        }
        
        return self.generate_response(
            prompt,
            response_format=response_format,
            **report_kwargs
        )

# Example usage
if __name__ == "__main__":
    # Initialize the agent
    research_agent = MarketResearchAgent()
    
    # Example 1: Quick market trend analysis
    trend_analysis = research_agent.analyze_market_trends(
        "current trends in sustainable packaging for e-commerce"
    )
    print("Market Trend Analysis:")
    print(trend_analysis)
    
    # Example 2: Comprehensive research report
    research_report = research_agent.generate_research_report(
        topic="I have a app that connects college students with relevant research opportunities",
        context="adoption rates, key players, and future projections"
    )
    print("\nMarket Research Report:")
    print(research_report)
