"""
Response models for agent outputs.

This module contains Pydantic models for structured responses from all agents.
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

# Common models used across multiple agents
class Trend(BaseModel):
    """A market trend observation."""
    name: str = Field(..., description="Name or title of the trend")
    description: str = Field(..., description="Detailed description of the trend")
    impact: str = Field(..., description="Potential impact of this trend")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")

class Insight(BaseModel):
    """A data-driven insight with business implications."""
    title: str = Field(..., description="Title of the insight")
    description: str = Field(..., description="Detailed explanation")
    significance: str = Field(..., description="Why this insight matters")
    data_points: List[str] = Field(default_factory=list, description="Supporting data points")
    impact: str = Field(description="Impact level (high/medium/low)", default="medium")

class Recommendation(BaseModel):
    """An actionable recommendation with priority and expected impact."""
    action: str = Field(..., description="Recommended action")
    rationale: str = Field(..., description="Reasoning behind the recommendation")
    priority: str = Field(..., description="Priority level (low/medium/high)")
    expected_impact: str = Field(..., description="Expected outcome of taking this action")
    effort: str = Field(description="Implementation effort (low/medium/high)", default="medium")

# Analytics Agent Models
class Metric(BaseModel):
    """A performance metric with values over time."""
    name: str = Field(..., description="Name of the metric")
    values: List[float] = Field(..., description="List of metric values")
    timestamps: List[datetime] = Field(..., description="Timestamps for each value")
    unit: str = Field("", description="Unit of measurement")
    trend: str = Field(..., description="Trend direction (increasing/decreasing/stable)")
    change_percentage: float = Field(..., description="Percentage change")

class CampaignMetrics(BaseModel):
    """Performance metrics for a marketing campaign."""
    campaign_name: str
    impressions: int
    clicks: int
    conversions: int
    ctr: float  # Click-through rate
    conversion_rate: float
    cost: float
    revenue: float
    roi: float

class CustomerJourneyStage(BaseModel):
    """A stage in the customer journey with metrics."""
    stage: str
    touchpoints: List[str]
    conversion_rate: float
    avg_time_in_stage: str
    drop_off_rate: float

class ABTestResult(BaseModel):
    """Results of an A/B test comparison."""
    test_name: str
    variant_a: Dict[str, Any]
    variant_b: Dict[str, Any]
    winner: str
    confidence_level: float
    recommendation: str

class AnalyticsResponse(BaseModel):
    """Comprehensive analytics response with insights and recommendations."""
    summary: str
    campaign_metrics: List[CampaignMetrics]
    customer_journey: List[CustomerJourneyStage]
    key_insights: List[str]
    recommendations: List[Recommendation]
    predictions: Dict[str, Any]

# Content Planning Agent Models
class ContentIdea(BaseModel):
    """A content idea with SEO and targeting information."""
    title: str
    description: str
    target_keywords: List[str]
    estimated_word_count: int
    priority: str  # "low", "medium", "high"
    content_type: str  # "blog", "social", "video", "infographic"
    seo_potential: Optional[float] = None
    engagement_potential: Optional[float] = None

class ContentCalendarEntry(BaseModel):
    """An entry in the content calendar."""
    content_title: str
    publish_date: str
    content_type: str
    target_audience: str
    keywords: List[str]
    status: str  # "planned", "in_progress", "ready", "published"
    assigned_to: Optional[str] = None
    channels: List[str] = []

class ContentPlanResponse(BaseModel):
    """Comprehensive content plan with strategy and calendar."""
    strategy_overview: str
    content_ideas: List[ContentIdea]
    calendar_entries: List[ContentCalendarEntry]
    seo_recommendations: Dict[str, Any]
    content_gap_analysis: Dict[str, Any]
    insights: List[Insight]
    recommendations: List[Recommendation]

# Presentation Agent Models
class ChartData(BaseModel):
    """Data structure for charts in presentations."""
    chart_type: str  # "bar", "line", "pie", "scatter", "area"
    title: str
    data: Dict[str, Any]
    x_axis_label: Optional[str] = None
    y_axis_label: Optional[str] = None

class SlideContent(BaseModel):
    """Content for a single presentation slide."""
    slide_number: int
    title: str
    content_type: str  # "text", "bullet_points", "chart", "image", "table"
    content: Any
    speaker_notes: Optional[str] = None

class PresentationStructure(BaseModel):
    """Complete presentation structure with design elements."""
    title: str
    subtitle: Optional[str] = None
    author: Optional[str] = None
    total_slides: int
    sections: List[str]
    slides: List[SlideContent]
    design_theme: str
    color_scheme: List[str]

# Newsletter Agent Models
class SubjectLine(BaseModel):
    """Email subject line with performance predictions."""
    text: str
    predicted_open_rate: float
    tone: str  # "urgent", "casual", "professional", "playful"
    emoji_included: bool

class NewsletterSection(BaseModel):
    """A section in the newsletter email."""
    section_type: str  # "header", "hero", "article", "cta", "footer"
    title: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    cta_text: Optional[str] = None
    cta_link: Optional[str] = None
    order: Optional[int] = None

class NewsletterContent(BaseModel):
    """Complete newsletter email content and metadata."""
    subject_lines: List[SubjectLine]
    preheader_text: str
    sections: List[NewsletterSection]
    personalization_tags: List[str]
    target_segment: str
    estimated_read_time: str
    tone: str
    call_to_action: str
    footer: Optional[str] = None

# Common Response Models
class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    details: Optional[Dict[str, Any]] = None
    code: Optional[int] = None
