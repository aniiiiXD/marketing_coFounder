"""
Newsletter Agent

Handles the creation and optimization of email newsletters, including:
- Newsletter content generation
- Subject line optimization
- Personalization and segmentation
- Email template design
- A/B testing recommendations
- Engagement optimization

This agent creates compelling newsletter content that drives opens, clicks, and conversions.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from .base_agent import BaseAgent

class SubjectLine(BaseModel):
    text: str
    predicted_open_rate: float
    tone: str  # "urgent", "casual", "professional", "playful"
    emoji_included: bool

class NewsletterSection(BaseModel):
    section_type: str  # "header", "hero", "article", "cta", "footer"
    title: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    cta_text: Optional[str] = None
    cta_link: Optional[str] = None

class NewsletterContent(BaseModel):
    subject_lines: List[SubjectLine]
    preheader_text: str
    sections: List[NewsletterSection]
    personalization_tags: List[str]
    target_segment: str
    estimated_read_time: str
    tone: str
    call_to_action: str

class NewsletterAgent(BaseAgent[NewsletterContent]):
    """
    Newsletter Agent - Creates optimized email newsletter content
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash", 
                 temperature: float = 0.6, 
                 max_tokens: int = 3000):
        super().__init__(model_name, temperature, max_tokens)
    
    def get_system_instruction(self) -> str:
        return """
        You are an expert email marketing copywriter specializing in newsletters.
        Create engaging, conversion-focused newsletter content with compelling subject lines.
        Always respond with valid JSON matching the NewsletterContent schema.
        Focus on readability, engagement, and driving action.
        """
        
    def get_response_model(self) -> type[NewsletterContent]:
        return NewsletterContent
    
    def create_newsletter(self, 
                         topic: str,
                         target_audience: str = "General subscribers",
                         tone: str = "professional",
                         primary_cta: str = "Learn More",
                         **kwargs) -> NewsletterContent:
        """
        Create a complete newsletter with subject lines and sections.
        
        Args:
            topic: Newsletter topic or theme
            target_audience: Target subscriber segment
            tone: Writing tone (professional, casual, playful, urgent)
            primary_cta: Primary call-to-action
            
        Returns:
            NewsletterContent: Complete newsletter structure
        """
        response_format = {
            "type": "object",
            "properties": {
                "subject_lines": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "predicted_open_rate": {"type": "number"},
                            "tone": {"type": "string"},
                            "emoji_included": {"type": "boolean"}
                        },
                        "required": ["text", "predicted_open_rate", "tone", "emoji_included"]
                    }
                },
                "preheader_text": {"type": "string"},
                "sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "section_type": {"type": "string"},
                            "title": {"type": "string"},
                            "content": {"type": "string"},
                            "image_url": {"type": "string"},
                            "cta_text": {"type": "string"},
                            "cta_link": {"type": "string"}
                        },
                        "required": ["section_type", "content"]
                    }
                },
                "personalization_tags": {"type": "array", "items": {"type": "string"}},
                "target_segment": {"type": "string"},
                "estimated_read_time": {"type": "string"},
                "tone": {"type": "string"},
                "call_to_action": {"type": "string"}
            },
            "required": ["subject_lines", "preheader_text", "sections", "personalization_tags", "target_segment", "estimated_read_time", "tone", "call_to_action"]
        }
        
        prompt = f"""
        Create an email newsletter about: {topic}
        Target audience: {target_audience}
        Tone: {tone}
        Primary CTA: {primary_cta}
        
        Include:
        1. 5 subject line variations with predicted open rates and tones
        2. Compelling preheader text (50-100 characters)
        3. Newsletter sections:
           - Header with greeting
           - Hero section with main message
           - 2-3 article/content sections
           - Call-to-action section
           - Footer with social links
        4. Personalization tags to use ({{first_name}}, {{company}}, etc.)
        5. Target segment description
        6. Estimated read time
        7. Overall tone
        8. Primary call-to-action
        
        Make it engaging, scannable, and conversion-focused.
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def generate_subject_lines(self, 
                              newsletter_topic: str,
                              count: int = 10,
                              **kwargs) -> List[SubjectLine]:
        """
        Generate multiple subject line variations.
        
        Args:
            newsletter_topic: Topic of the newsletter
            count: Number of subject lines to generate
            
        Returns:
            List[SubjectLine]: Subject line variations
        """
        response_format = {
            "type": "object",
            "properties": {
                "subject_lines": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "predicted_open_rate": {"type": "number"},
                            "tone": {"type": "string"},
                            "emoji_included": {"type": "boolean"}
                        },
                        "required": ["text", "predicted_open_rate", "tone", "emoji_included"]
                    }
                }
            },
            "required": ["subject_lines"]
        }
        
        prompt = f"""
        Generate {count} subject line variations for a newsletter about: {newsletter_topic}
        
        For each subject line:
        1. Keep under 50 characters
        2. Estimate open rate (0-1)
        3. Specify tone (urgent, casual, professional, playful)
        4. Note if emoji is included
        
        Vary the approach: questions, benefits, urgency, curiosity, personalization.
        """
        
        result = self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
        
        return [SubjectLine(**line) for line in result.subject_lines]
    
    def optimize_content(self, 
                        existing_content: str,
                        goal: str = "increase engagement",
                        **kwargs) -> Dict[str, Any]:
        """
        Optimize existing newsletter content.
        
        Args:
            existing_content: Current newsletter content
            goal: Optimization goal
            
        Returns:
            Dict with optimized content and recommendations
        """
        response_format = {
            "type": "object",
            "properties": {
                "optimized_content": {"type": "string"},
                "changes_made": {"type": "array", "items": {"type": "string"}},
                "readability_score": {"type": "number"},
                "engagement_predictions": {"type": "object"},
                "recommendations": {"type": "array", "items": {"type": "string"}},
                "ab_test_suggestions": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["optimized_content", "changes_made", "readability_score", "recommendations"]
        }
        
        prompt = f"""
        Optimize this newsletter content to {goal}:
        
        {existing_content}
        
        Provide:
        1. Optimized version of the content
        2. List of changes made
        3. Readability score (0-100)
        4. Predicted engagement metrics
        5. Additional recommendations
        6. A/B test suggestions
        
        Focus on clarity, scannability, and driving action.
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def create_drip_campaign(self, 
                           campaign_goal: str,
                           email_count: int = 5,
                           **kwargs) -> Dict[str, Any]:
        """
        Create a multi-email drip campaign sequence.
        
        Args:
            campaign_goal: Goal of the drip campaign
            email_count: Number of emails in sequence
            
        Returns:
            Dict with complete drip campaign structure
        """
        response_format = {
            "type": "object",
            "properties": {
                "campaign_name": {"type": "string"},
                "goal": {"type": "string"},
                "total_emails": {"type": "integer"},
                "emails": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "email_number": {"type": "integer"},
                            "send_delay": {"type": "string"},
                            "subject_line": {"type": "string"},
                            "preview_text": {"type": "string"},
                            "key_message": {"type": "string"},
                            "content_outline": {"type": "array", "items": {"type": "string"}},
                            "cta": {"type": "string"}
                        },
                        "required": ["email_number", "send_delay", "subject_line", "key_message", "cta"]
                    }
                },
                "segmentation_criteria": {"type": "array", "items": {"type": "string"}},
                "success_metrics": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["campaign_name", "goal", "total_emails", "emails", "success_metrics"]
        }
        
        prompt = f"""
        Create a {email_count}-email drip campaign for: {campaign_goal}
        
        For each email in the sequence:
        1. Email number
        2. Send delay (e.g., "Day 1", "3 days after signup")
        3. Subject line
        4. Preview text
        5. Key message/theme
        6. Content outline
        7. Call-to-action
        
        Also include:
        - Campaign name
        - Segmentation criteria
        - Success metrics to track
        
        Build a logical progression that nurtures leads toward the goal.
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def personalize_content(self, 
                          base_content: str,
                          subscriber_data: Dict[str, Any],
                          **kwargs) -> Dict[str, Any]:
        """
        Generate personalized newsletter variations.
        
        Args:
            base_content: Base newsletter content
            subscriber_data: Subscriber segment data
            
        Returns:
            Dict with personalized content versions
        """
        response_format = {
            "type": "object",
            "properties": {
                "personalized_versions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "segment": {"type": "string"},
                            "subject_line": {"type": "string"},
                            "content": {"type": "string"},
                            "personalization_elements": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "dynamic_content_blocks": {"type": "array", "items": {"type": "object"}},
                "personalization_strategy": {"type": "string"}
            },
            "required": ["personalized_versions", "personalization_strategy"]
        }
        
        prompt = f"""
        Create personalized versions of this newsletter:
        
        Base content:
        {base_content}
        
        Subscriber segments:
        {subscriber_data}
        
        For each segment, provide:
        1. Segment name
        2. Personalized subject line
        3. Adapted content
        4. Personalization elements used
        
        Also include:
        - Dynamic content blocks
        - Overall personalization strategy
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )

# Example usage
if __name__ == "__main__":
    agent = NewsletterAgent()
    
    # Create newsletter
    newsletter = agent.create_newsletter(
        topic="New product launch announcement",
        target_audience="Active customers",
        tone="professional",
        primary_cta="Shop Now"
    )
    print("Newsletter:", newsletter.dict())
    
    # Generate subject lines
    subject_lines = agent.generate_subject_lines(
        newsletter_topic="Weekly industry insights",
        count=5
    )
    print("\nSubject Lines:", [line.dict() for line in subject_lines])
    
    # Optimize content
    existing = "Check out our new features. Click here to learn more."
    optimized = agent.optimize_content(
        existing_content=existing,
        goal="increase click-through rate"
    )
    print("\nOptimized:", optimized)
    
    # Create drip campaign
    drip = agent.create_drip_campaign(
        campaign_goal="Onboard new users",
        email_count=5
    )
    print("\nDrip Campaign:", drip)