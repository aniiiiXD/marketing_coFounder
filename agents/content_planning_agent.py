"""
Content Planning Agent

Manages the content strategy and calendar, including:
- Content ideation and topic generation
- SEO optimization and keyword research
- Content calendar management
- Content gap analysis
- Performance-based content optimization

This agent ensures content aligns with marketing goals, target audience,
and follows SEO best practices while maintaining a consistent publishing schedule.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from .base_agent import BaseAgent

class ContentIdea(BaseModel):
    title: str
    description: str
    target_keywords: List[str]
    estimated_word_count: int
    priority: str  # "low", "medium", "high"
    content_type: str  # "blog", "social", "video", "infographic"

class ContentCalendarEntry(BaseModel):
    content_title: str
    publish_date: str
    content_type: str
    target_audience: str
    keywords: List[str]
    status: str  # "planned", "in_progress", "ready", "published"

class ContentPlanResponse(BaseModel):
    strategy_overview: str
    content_ideas: List[ContentIdea]
    calendar_entries: List[ContentCalendarEntry]
    seo_recommendations: List[str]
    content_gaps: List[str]
    performance_metrics: Dict[str, Any]

class ContentPlanningAgent(BaseAgent[ContentPlanResponse]):
    """
    Content Planning Agent - Generates content strategies and calendars
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash", 
                 temperature: float = 0.4, 
                 max_tokens: int = 3000):
        super().__init__(model_name, temperature, max_tokens)
    
    def get_system_instruction(self) -> str:
        return """
        You are an expert content strategist and SEO specialist. Generate comprehensive 
        content plans with actionable ideas, SEO-optimized topics, and structured calendars.
        Always respond with valid JSON matching the ContentPlanResponse schema.
        """
        
    def get_response_model(self) -> type[ContentPlanResponse]:
        return ContentPlanResponse
    
    def generate_content_plan(self, 
                            topic: str, 
                            target_audience: str = None,
                            timeframe: str = "30 days",
                            **kwargs) -> ContentPlanResponse:
        """
        Generate a comprehensive content plan.
        
        Args:
            topic: Main topic or industry focus
            target_audience: Target audience description
            timeframe: Planning timeframe (e.g., "30 days", "3 months")
            
        Returns:
            ContentPlanResponse: Structured content plan with ideas and calendar
        """
        response_format = {
            "type": "object",
            "properties": {
                "strategy_overview": {"type": "string"},
                "content_ideas": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "target_keywords": {"type": "array", "items": {"type": "string"}},
                            "estimated_word_count": {"type": "integer"},
                            "priority": {"type": "string"},
                            "content_type": {"type": "string"}
                        },
                        "required": ["title", "description", "target_keywords", "estimated_word_count", "priority", "content_type"]
                    }
                },
                "calendar_entries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content_title": {"type": "string"},
                            "publish_date": {"type": "string"},
                            "content_type": {"type": "string"},
                            "target_audience": {"type": "string"},
                            "keywords": {"type": "array", "items": {"type": "string"}},
                            "status": {"type": "string"}
                        },
                        "required": ["content_title", "publish_date", "content_type", "target_audience", "keywords", "status"]
                    }
                },
                "seo_recommendations": {"type": "array", "items": {"type": "string"}},
                "content_gaps": {"type": "array", "items": {"type": "string"}},
                "performance_metrics": {"type": "object"}
            },
            "required": ["strategy_overview", "content_ideas", "calendar_entries", "seo_recommendations", "content_gaps", "performance_metrics"]
        }
        
        prompt = f"""
        Create a comprehensive content plan for: {topic}
        Timeframe: {timeframe}
        """
        
        if target_audience:
            prompt += f"\nTarget Audience: {target_audience}"
            
        prompt += """
        
        Include:
        1. Strategy overview
        2. 5-10 content ideas with SEO keywords
        3. Content calendar with publishing schedule
        4. SEO recommendations
        5. Identified content gaps
        6. Key performance metrics to track
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def generate_content_ideas(self, 
                              topic: str, 
                              count: int = 10,
                              **kwargs) -> List[ContentIdea]:
        """
        Generate content ideas for a specific topic.
        
        Args:
            topic: Topic to generate ideas for
            count: Number of ideas to generate
            
        Returns:
            List[ContentIdea]: List of content ideas
        """
        response_format = {
            "type": "object",
            "properties": {
                "ideas": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "target_keywords": {"type": "array", "items": {"type": "string"}},
                            "estimated_word_count": {"type": "integer"},
                            "priority": {"type": "string"},
                            "content_type": {"type": "string"}
                        },
                        "required": ["title", "description", "target_keywords", "estimated_word_count", "priority", "content_type"]
                    }
                }
            },
            "required": ["ideas"]
        }
        
        prompt = f"""
        Generate {count} content ideas for: {topic}
        
        Each idea should include:
        - Engaging title
        - Brief description
        - Target SEO keywords
        - Estimated word count
        - Priority level (low/medium/high)
        - Content type (blog/social/video/infographic)
        """
        
        result = self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
        
        return [ContentIdea(**idea) for idea in result.ideas]
    
    def optimize_seo(self, 
                    content_topic: str, 
                    current_keywords: List[str] = None,
                    **kwargs) -> Dict[str, Any]:
        """
        Generate SEO optimization recommendations.
        
        Args:
            content_topic: Topic of the content
            current_keywords: Current keywords being targeted
            
        Returns:
            Dict with SEO recommendations
        """
        response_format = {
            "type": "object",
            "properties": {
                "primary_keywords": {"type": "array", "items": {"type": "string"}},
                "secondary_keywords": {"type": "array", "items": {"type": "string"}},
                "long_tail_keywords": {"type": "array", "items": {"type": "string"}},
                "meta_title": {"type": "string"},
                "meta_description": {"type": "string"},
                "recommended_headings": {"type": "array", "items": {"type": "string"}},
                "internal_link_suggestions": {"type": "array", "items": {"type": "string"}},
                "content_structure": {"type": "string"}
            },
            "required": ["primary_keywords", "secondary_keywords", "long_tail_keywords", "meta_title", "meta_description"]
        }
        
        prompt = f"""
        Provide SEO optimization recommendations for content about: {content_topic}
        """
        
        if current_keywords:
            prompt += f"\nCurrent keywords: {', '.join(current_keywords)}"
            
        prompt += """
        
        Include:
        - Primary keywords (3-5)
        - Secondary keywords (5-10)
        - Long-tail keywords (5-10)
        - Optimized meta title
        - Optimized meta description
        - Recommended heading structure
        - Internal linking suggestions
        - Overall content structure recommendations
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )

# Example usage
if __name__ == "__main__":
    agent = ContentPlanningAgent()
    
    # Generate content plan
    plan = agent.generate_content_plan(
        topic="AI-powered productivity tools for remote teams",
        target_audience="Tech-savvy remote workers and team managers",
        timeframe="30 days"
    )
    print("Content Plan:", plan.dict())
    
    # Generate content ideas
    ideas = agent.generate_content_ideas(
        topic="sustainable fashion trends",
        count=5
    )
    print("\nContent Ideas:", [idea.dict() for idea in ideas])
    
    # SEO optimization
    seo = agent.optimize_seo(
        content_topic="Best project management software for startups",
        current_keywords=["project management", "startup tools"]
    )
    print("\nSEO Recommendations:", seo)