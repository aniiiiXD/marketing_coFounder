"""
Orchestrator Agent

This is the main coordinator for all marketing agents. It manages the workflow between different agents,
handles task delegation, and ensures smooth communication between components. The orchestrator is responsible for:
- Initializing and managing agent instances
- Routing tasks between specialized agents
- Handling error recovery and retries
- Managing the overall execution flow
- Maintaining state between agent interactions
"""

from typing import Dict, Any, Optional, List, Type, TypeVar, Generic
from pydantic import BaseModel
import logging
from datetime import datetime

# Import agent classes
from .analytics_agent import AnalyticsAgent
from .content_planning_agent import ContentPlanningAgent
from .newsletter_agent import NewsletterAgent
from .presentation_agent import PresentationAgent

# Import models
from .models import (
    AnalyticsResponse,
    ContentPlanResponse,
    NewsletterContent,
    PresentationStructure,
    ErrorResponse
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class Orchestrator:
    """
    Main orchestrator for managing marketing agents and workflows.
    """
    
    def __init__(self):
        """Initialize the orchestrator and all agents."""
        self.analytics_agent = AnalyticsAgent()
        self.content_planning_agent = ContentPlanningAgent()
        self.newsletter_agent = NewsletterAgent()
        self.presentation_agent = PresentationAgent()
        self.state: Dict[str, Any] = {}
        logger.info("Orchestrator initialized with all agents")
    
    async def execute_workflow(self, workflow_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a predefined workflow by name.
        
        Args:
            workflow_name: Name of the workflow to execute
            **kwargs: Additional parameters for the workflow
            
        Returns:
            Dict containing the workflow results
        """
        workflow_method = getattr(self, f"workflow_{workflow_name}", None)
        if not workflow_method:
            error_msg = f"Workflow '{workflow_name}' not found"
            logger.error(error_msg)
            return self._create_error_response(error_msg)
        
        try:
            logger.info(f"Starting workflow: {workflow_name}")
            result = await workflow_method(**kwargs)
            logger.info(f"Completed workflow: {workflow_name}")
            return {"status": "success", "data": result, "timestamp": datetime.utcnow().isoformat()}
        except Exception as e:
            error_msg = f"Error in workflow '{workflow_name}': {str(e)}"
            logger.exception(error_msg)
            return self._create_error_response(error_msg)
    
    async def workflow_content_campaign(
        self,
        campaign_topic: str,
        target_audience: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        End-to-end content campaign workflow.
        
        Args:
            campaign_topic: Main topic for the campaign
            target_audience: Target audience description
            
        Returns:
            Dict containing campaign results
        """
        # 1. Content Planning
        content_plan = await self.content_planning_agent.generate_content_plan(
            topic=campaign_topic,
            target_audience=target_audience,
            timeframe=kwargs.get("timeframe", "30 days")
        )
        
        # 2. Content Creation
        created_content = []
        for idea in content_plan.content_ideas[:3]:  # Limit to top 3 ideas
            content = await self._create_content(idea, target_audience)
            created_content.append(content)
        
        # 3. Create Newsletter
        newsletter = await self.newsletter_agent.create_newsletter(
            topic=campaign_topic,
            target_audience=target_audience,
            tone=kwargs.get("tone", "professional"),
            primary_cta=kwargs.get("cta", "Learn More")
        )
        
        # 4. Create Presentation
        presentation = await self.presentation_agent.create_presentation(
            topic=f"{campaign_topic} - Campaign Overview",
            target_audience="Marketing Team",
            slide_count=8,
            data={
                "campaign_topic": campaign_topic,
                "target_audience": target_audience,
                "content_ideas": [idea.dict() for idea in content_plan.content_ideas],
                "newsletter": newsletter.dict()
            }
        )
        
        return {
            "content_plan": content_plan.dict(),
            "created_content": [c.dict() for c in created_content],
            "newsletter": newsletter.dict(),
            "presentation": presentation.dict()
        }
    
    async def workflow_analyze_campaign_performance(
        self,
        campaign_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Analyze campaign performance and generate reports.
        
        Args:
            campaign_data: Campaign performance data
            
        Returns:
            Dict containing analysis results
        """
        # 1. Analyze campaign performance
        analysis = await self.analytics_agent.analyze_campaign_performance(campaign_data)
        
        # 2. Generate presentation
        presentation = await self.presentation_agent.create_executive_summary(
            data=analysis.dict(),
            max_slides=6
        )
        
        return {
            "analysis": analysis.dict(),
            "presentation": presentation.dict()
        }
    
    async def _create_content(self, idea, target_audience: str) -> Dict[str, Any]:
        """Helper method to create content from an idea."""
        # This is a placeholder for actual content generation logic
        # In a real implementation, this would call a content generation API or service
        return {
            "title": idea.title,
            "content_type": idea.content_type,
            "target_audience": target_audience,
            "content": f"Detailed content for: {idea.title}",
            "status": "draft",
            "created_at": datetime.utcnow().isoformat()
        }
    
    def _create_error_response(self, message: str, code: int = 500) -> Dict[str, Any]:
        """Create a standardized error response."""
        return {
            "status": "error",
            "error": {
                "message": message,
                "code": code,
                "timestamp": datetime.utcnow().isoformat()
            }
        }

# Example usage
async def main():
    """Example usage of the Orchestrator."""
    orchestrator = Orchestrator()
    
    # Example 1: Run a content campaign
    campaign_result = await orchestrator.execute_workflow(
        "content_campaign",
        campaign_topic="Remote Work Productivity",
        target_audience="Freelancers and digital nomads, 25-40, global",
        timeframe="14 days"
    )
    print("Campaign Result:", campaign_result)
    
    # Example 2: Analyze campaign performance
    analysis_result = await orchestrator.execute_workflow(
        "analyze_campaign_performance",
        campaign_data={
            "campaign_name": "FocusFlow App Launch",
            "metrics": {
                "impressions": 100000,
                "clicks": 5000,
                "conversions": 250,
                "revenue": 50000
            }
        }
    )
    print("Analysis Result:", analysis_result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
