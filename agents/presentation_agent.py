"""
Presentation Agent

Handles the creation and formatting of presentation materials, including:
- Automated PowerPoint/Google Slides generation
- Data visualization and chart creation
- Brand-consistent slide design
- Executive summary generation
- Multi-format export options (PPTX, PDF, etc.)
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from .base_agent import BaseAgent

class SlideContent(BaseModel):
    slide_number: int
    title: str
    content_type: str  # "text", "bullet_points", "chart", "image", "table"
    content: Any
    speaker_notes: Optional[str] = None

class ChartData(BaseModel):
    chart_type: str  # "bar", "line", "pie", "scatter", "area"
    title: str
    data: Dict[str, Any]
    x_axis_label: Optional[str] = None
    y_axis_label: Optional[str] = None

class PresentationStructure(BaseModel):
    title: str
    subtitle: Optional[str] = None
    author: Optional[str] = None
    total_slides: int
    sections: List[str]
    slides: List[SlideContent]
    design_theme: str
    color_scheme: List[str]

class PresentationAgent(BaseAgent[PresentationStructure]):
    """
    Presentation Agent - Creates structured presentation content
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash", 
                 temperature: float = 0.5, 
                 max_tokens: int = 4000):
        super().__init__(model_name, temperature, max_tokens)
    
    def get_system_instruction(self) -> str:
        return """
        You are an expert presentation designer and storyteller. Create compelling,
        well-structured presentation content that communicates ideas clearly.
        Always respond with valid JSON matching the PresentationStructure schema.
        Focus on visual hierarchy, narrative flow, and data-driven storytelling.
        """
        
    def get_response_model(self) -> type[PresentationStructure]:
        return PresentationStructure
    
    def create_presentation(self, 
                          topic: str,
                          target_audience: str = "General audience",
                          slide_count: int = 10,
                          data: Optional[Dict[str, Any]] = None,
                          **kwargs) -> PresentationStructure:
        """
        Create a complete presentation structure.
        
        Args:
            topic: Presentation topic
            target_audience: Target audience description
            slide_count: Number of slides to generate
            data: Optional data to visualize
            
        Returns:
            PresentationStructure: Complete presentation outline with slides
        """
        response_format = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "subtitle": {"type": "string"},
                "author": {"type": "string"},
                "total_slides": {"type": "integer"},
                "sections": {"type": "array", "items": {"type": "string"}},
                "slides": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "slide_number": {"type": "integer"},
                            "title": {"type": "string"},
                            "content_type": {"type": "string"},
                            "content": {},
                            "speaker_notes": {"type": "string"}
                        },
                        "required": ["slide_number", "title", "content_type", "content"]
                    }
                },
                "design_theme": {"type": "string"},
                "color_scheme": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["title", "total_slides", "sections", "slides", "design_theme", "color_scheme"]
        }
        
        prompt = f"""
        Create a {slide_count}-slide presentation about: {topic}
        Target audience: {target_audience}
        """
        
        if data:
            prompt += f"\nData to incorporate: {data}"
            
        prompt += """
        
        Include:
        1. Compelling title and subtitle
        2. Logical sections/chapters
        3. Slide-by-slide breakdown with:
           - Slide number
           - Title
           - Content type (text, bullet_points, chart, image, table)
           - Actual content
           - Speaker notes
        4. Suggested design theme
        5. Brand color scheme (hex codes)
        
        Slide structure should include:
        - Opening slide (title)
        - Agenda/outline
        - Content slides (with mix of text, data, visuals)
        - Conclusion/call-to-action
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def create_executive_summary(self, 
                                data: Dict[str, Any],
                                max_slides: int = 5,
                                **kwargs) -> PresentationStructure:
        """
        Create an executive summary presentation.
        
        Args:
            data: Key data and insights to summarize
            max_slides: Maximum number of slides
            
        Returns:
            PresentationStructure: Executive summary presentation
        """
        response_format = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "subtitle": {"type": "string"},
                "author": {"type": "string"},
                "total_slides": {"type": "integer"},
                "sections": {"type": "array", "items": {"type": "string"}},
                "slides": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "slide_number": {"type": "integer"},
                            "title": {"type": "string"},
                            "content_type": {"type": "string"},
                            "content": {},
                            "speaker_notes": {"type": "string"}
                        },
                        "required": ["slide_number", "title", "content_type", "content"]
                    }
                },
                "design_theme": {"type": "string"},
                "color_scheme": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["title", "total_slides", "sections", "slides", "design_theme", "color_scheme"]
        }
        
        prompt = f"""
        Create an executive summary presentation (max {max_slides} slides) based on:
        {data}
        
        Focus on:
        1. Key findings and insights
        2. Critical metrics and KPIs
        3. Strategic recommendations
        4. Next steps and action items
        
        Keep it concise, high-level, and decision-focused.
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def generate_charts(self, 
                       data: Dict[str, Any],
                       chart_count: int = 3,
                       **kwargs) -> List[ChartData]:
        """
        Generate chart specifications for data visualization.
        
        Args:
            data: Data to visualize
            chart_count: Number of charts to create
            
        Returns:
            List[ChartData]: Chart specifications
        """
        response_format = {
            "type": "object",
            "properties": {
                "charts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "chart_type": {"type": "string"},
                            "title": {"type": "string"},
                            "data": {"type": "object"},
                            "x_axis_label": {"type": "string"},
                            "y_axis_label": {"type": "string"}
                        },
                        "required": ["chart_type", "title", "data"]
                    }
                }
            },
            "required": ["charts"]
        }
        
        prompt = f"""
        Create {chart_count} data visualizations for:
        {data}
        
        For each chart, specify:
        1. Chart type (bar, line, pie, scatter, area)
        2. Title
        3. Data structure with labels and values
        4. Axis labels
        
        Choose chart types that best represent the data.
        """
        
        result = self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
        
        return [ChartData(**chart) for chart in result.charts]
    
    def design_slide_layout(self, 
                          slide_content: str,
                          content_type: str = "mixed",
                          **kwargs) -> Dict[str, Any]:
        """
        Design layout for a specific slide.
        
        Args:
            slide_content: Content for the slide
            content_type: Type of content (text, data, visual)
            
        Returns:
            Dict with layout specifications
        """
        response_format = {
            "type": "object",
            "properties": {
                "layout_type": {"type": "string"},
                "title": {"type": "string"},
                "title_position": {"type": "string"},
                "content_blocks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "position": {"type": "string"},
                            "size": {"type": "string"},
                            "content": {}
                        }
                    }
                },
                "visual_elements": {"type": "array", "items": {"type": "string"}},
                "typography": {"type": "object"},
                "color_usage": {"type": "object"}
            },
            "required": ["layout_type", "title", "content_blocks"]
        }
        
        prompt = f"""
        Design a slide layout for this content:
        {slide_content}
        
        Content type: {content_type}
        
        Provide:
        1. Layout type (title-only, title-content, two-column, full-image, etc.)
        2. Title and positioning
        3. Content blocks with positions and sizes
        4. Visual elements (icons, shapes, images)
        5. Typography specifications
        6. Color usage guidelines
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def create_pitch_deck(self, 
                         company_info: Dict[str, Any],
                         **kwargs) -> PresentationStructure:
        """
        Create a pitch deck presentation.
        
        Args:
            company_info: Company details, product, market, traction, etc.
            
        Returns:
            PresentationStructure: Pitch deck structure
        """
        response_format = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "subtitle": {"type": "string"},
                "author": {"type": "string"},
                "total_slides": {"type": "integer"},
                "sections": {"type": "array", "items": {"type": "string"}},
                "slides": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "slide_number": {"type": "integer"},
                            "title": {"type": "string"},
                            "content_type": {"type": "string"},
                            "content": {},
                            "speaker_notes": {"type": "string"}
                        },
                        "required": ["slide_number", "title", "content_type", "content"]
                    }
                },
                "design_theme": {"type": "string"},
                "color_scheme": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["title", "total_slides", "sections", "slides", "design_theme", "color_scheme"]
        }
        
        prompt = f"""
        Create a pitch deck presentation for:
        {company_info}
        
        Include standard pitch deck sections:
        1. Cover slide
        2. Problem statement
        3. Solution
        4. Market opportunity
        5. Product/Demo
        6. Business model
        7. Traction/Metrics
        8. Competition
        9. Team
        10. Financials/Ask
        11. Thank you/Contact
        
        Make it investor-ready and compelling.
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )

# Example usage
if __name__ == "__main__":
    agent = PresentationAgent()
    
    # Create general presentation
    presentation = agent.create_presentation(
        topic="Q4 Marketing Strategy Review",
        target_audience="Executive team",
        slide_count=12
    )
    print("Presentation:", presentation.dict())
    
    # Create executive summary
    summary_data = {
        "revenue": "$2.5M",
        "growth": "35% YoY",
        "key_campaigns": ["Email", "Social", "Content"],
        "roi": "250%"
    }
    exec_summary = agent.create_executive_summary(summary_data, max_slides=5)
    print("\nExecutive Summary:", exec_summary.dict())
    
    # Generate charts
    chart_data = {
        "monthly_revenue": [100000, 120000, 150000, 180000],
        "conversion_rates": {"Email": 0.05, "Social": 0.03, "Paid": 0.07}
    }
    charts = agent.generate_charts(chart_data, chart_count=2)
    print("\nCharts:", [chart.dict() for chart in charts])
    
    # Create pitch deck
    company_data = {
        "name": "TechStartup Inc",
        "product": "AI-powered analytics platform",
        "market_size": "$10B",
        "traction": "10K users, $500K ARR"
    }
    pitch_deck = agent.create_pitch_deck(company_data)
    print("\nPitch Deck:", pitch_deck.dict())