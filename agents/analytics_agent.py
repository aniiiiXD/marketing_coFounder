"""
Analytics Agent

Responsible for tracking and analyzing marketing performance metrics, including:
- Campaign performance analysis
- ROI and conversion tracking
- Customer journey mapping
- A/B test analysis
- Predictive analytics and forecasting
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from .base_agent import BaseAgent

class CampaignMetrics(BaseModel):
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
    stage: str
    touchpoints: List[str]
    conversion_rate: float
    avg_time_in_stage: str
    drop_off_rate: float

class ABTestResult(BaseModel):
    test_name: str
    variant_a: Dict[str, Any]
    variant_b: Dict[str, Any]
    winner: str
    confidence_level: float
    recommendation: str

class AnalyticsResponse(BaseModel):
    summary: str
    campaign_metrics: List[CampaignMetrics]
    customer_journey: List[CustomerJourneyStage]
    key_insights: List[str]
    recommendations: List[str]
    predictions: Dict[str, Any]

class AnalyticsAgent(BaseAgent[AnalyticsResponse]):
    """
    Analytics Agent - Analyzes marketing performance and provides insights
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash", 
                 temperature: float = 0.2, 
                 max_tokens: int = 3000):
        super().__init__(model_name, temperature, max_tokens)
    
    def get_system_instruction(self) -> str:
        return """
        You are an expert marketing analytics specialist. Analyze performance data,
        identify trends, calculate metrics, and provide actionable insights.
        Always respond with valid JSON matching the AnalyticsResponse schema.
        Be precise with numbers and data-driven in your recommendations.
        """
        
    def get_response_model(self) -> type[AnalyticsResponse]:
        return AnalyticsResponse
    
    def analyze_campaign_performance(self, 
                                    campaign_data: Dict[str, Any],
                                    **kwargs) -> AnalyticsResponse:
        """
        Analyze marketing campaign performance.
        
        Args:
            campaign_data: Dictionary containing campaign metrics and data
            
        Returns:
            AnalyticsResponse: Comprehensive performance analysis
        """
        response_format = {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "campaign_metrics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "campaign_name": {"type": "string"},
                            "impressions": {"type": "integer"},
                            "clicks": {"type": "integer"},
                            "conversions": {"type": "integer"},
                            "ctr": {"type": "number"},
                            "conversion_rate": {"type": "number"},
                            "cost": {"type": "number"},
                            "revenue": {"type": "number"},
                            "roi": {"type": "number"}
                        },
                        "required": ["campaign_name", "impressions", "clicks", "conversions", "ctr", "conversion_rate", "cost", "revenue", "roi"]
                    }
                },
                "customer_journey": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "stage": {"type": "string"},
                            "touchpoints": {"type": "array", "items": {"type": "string"}},
                            "conversion_rate": {"type": "number"},
                            "avg_time_in_stage": {"type": "string"},
                            "drop_off_rate": {"type": "number"}
                        },
                        "required": ["stage", "touchpoints", "conversion_rate", "avg_time_in_stage", "drop_off_rate"]
                    }
                },
                "key_insights": {"type": "array", "items": {"type": "string"}},
                "recommendations": {"type": "array", "items": {"type": "string"}},
                "predictions": {"type": "object"}
            },
            "required": ["summary", "campaign_metrics", "customer_journey", "key_insights", "recommendations", "predictions"]
        }
        
        prompt = f"""
        Analyze the following campaign performance data:
        {campaign_data}
        
        Provide:
        1. Executive summary of performance
        2. Detailed campaign metrics (impressions, clicks, conversions, CTR, conversion rate, cost, revenue, ROI)
        3. Customer journey analysis with stages and touchpoints
        4. Key insights from the data
        5. Actionable recommendations for improvement
        6. Predictions for next period based on trends
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def analyze_ab_test(self, 
                       test_data: Dict[str, Any],
                       **kwargs) -> ABTestResult:
        """
        Analyze A/B test results and determine winner.
        
        Args:
            test_data: Dictionary containing A/B test data
            
        Returns:
            ABTestResult: Analysis with winner and recommendations
        """
        response_format = {
            "type": "object",
            "properties": {
                "test_name": {"type": "string"},
                "variant_a": {"type": "object"},
                "variant_b": {"type": "object"},
                "winner": {"type": "string"},
                "confidence_level": {"type": "number"},
                "recommendation": {"type": "string"}
            },
            "required": ["test_name", "variant_a", "variant_b", "winner", "confidence_level", "recommendation"]
        }
        
        prompt = f"""
        Analyze the following A/B test data:
        {test_data}
        
        Provide:
        1. Test name/description
        2. Variant A performance metrics
        3. Variant B performance metrics
        4. Winner determination
        5. Statistical confidence level (0-1)
        6. Recommendation for next steps
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def calculate_roi(self, 
                     campaigns: List[Dict[str, Any]],
                     **kwargs) -> Dict[str, Any]:
        """
        Calculate ROI and financial metrics for campaigns.
        
        Args:
            campaigns: List of campaign data with costs and revenues
            
        Returns:
            Dict with ROI analysis and financial insights
        """
        response_format = {
            "type": "object",
            "properties": {
                "total_investment": {"type": "number"},
                "total_revenue": {"type": "number"},
                "overall_roi": {"type": "number"},
                "roi_by_campaign": {"type": "array", "items": {
                    "type": "object",
                    "properties": {
                        "campaign_name": {"type": "string"},
                        "roi": {"type": "number"},
                        "performance_rating": {"type": "string"}
                    }
                }},
                "best_performing_campaign": {"type": "string"},
                "worst_performing_campaign": {"type": "string"},
                "insights": {"type": "array", "items": {"type": "string"}},
                "optimization_suggestions": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["total_investment", "total_revenue", "overall_roi", "roi_by_campaign", "insights"]
        }
        
        prompt = f"""
        Calculate ROI and analyze financial performance for these campaigns:
        {campaigns}
        
        Provide:
        1. Total investment across all campaigns
        2. Total revenue generated
        3. Overall ROI percentage
        4. ROI breakdown by campaign
        5. Best and worst performing campaigns
        6. Financial insights
        7. Optimization suggestions
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def predict_performance(self, 
                          historical_data: Dict[str, Any],
                          forecast_period: str = "30 days",
                          **kwargs) -> Dict[str, Any]:
        """
        Generate performance predictions based on historical data.
        
        Args:
            historical_data: Past performance metrics
            forecast_period: Period to forecast (e.g., "30 days", "3 months")
            
        Returns:
            Dict with predictions and confidence intervals
        """
        response_format = {
            "type": "object",
            "properties": {
                "forecast_period": {"type": "string"},
                "predicted_metrics": {"type": "object"},
                "confidence_interval": {"type": "object"},
                "trend_analysis": {"type": "string"},
                "risk_factors": {"type": "array", "items": {"type": "string"}},
                "opportunities": {"type": "array", "items": {"type": "string"}},
                "recommended_actions": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["forecast_period", "predicted_metrics", "confidence_interval", "trend_analysis"]
        }
        
        prompt = f"""
        Based on this historical performance data:
        {historical_data}
        
        Predict performance for the next {forecast_period}.
        
        Include:
        1. Predicted metrics (impressions, clicks, conversions, revenue)
        2. Confidence intervals for predictions
        3. Trend analysis
        4. Identified risk factors
        5. Growth opportunities
        6. Recommended actions to achieve predictions
        """
        
        return self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
    
    def map_customer_journey(self, 
                           touchpoint_data: Dict[str, Any],
                           **kwargs) -> List[CustomerJourneyStage]:
        """
        Map and analyze customer journey stages.
        
        Args:
            touchpoint_data: Data about customer touchpoints and interactions
            
        Returns:
            List[CustomerJourneyStage]: Journey stages with metrics
        """
        response_format = {
            "type": "object",
            "properties": {
                "journey_stages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "stage": {"type": "string"},
                            "touchpoints": {"type": "array", "items": {"type": "string"}},
                            "conversion_rate": {"type": "number"},
                            "avg_time_in_stage": {"type": "string"},
                            "drop_off_rate": {"type": "number"}
                        },
                        "required": ["stage", "touchpoints", "conversion_rate", "avg_time_in_stage", "drop_off_rate"]
                    }
                }
            },
            "required": ["journey_stages"]
        }
        
        prompt = f"""
        Map the customer journey based on this touchpoint data:
        {touchpoint_data}
        
        For each stage (Awareness, Consideration, Decision, Retention), provide:
        1. Stage name
        2. Key touchpoints
        3. Conversion rate to next stage
        4. Average time spent in stage
        5. Drop-off rate
        """
        
        result = self._generate_structured_response(
            prompt=prompt,
            response_format=response_format,
            **kwargs
        )
        
        return [CustomerJourneyStage(**stage) for stage in result.journey_stages]

# Example usage
if __name__ == "__main__":
    agent = AnalyticsAgent()
    
    # Analyze campaign performance
    campaign_data = {
        "campaigns": [
            {"name": "Q4 Email Campaign", "impressions": 50000, "clicks": 2500, "conversions": 125, "cost": 5000, "revenue": 15000},
            {"name": "Social Media Ads", "impressions": 100000, "clicks": 3000, "conversions": 150, "cost": 8000, "revenue": 20000}
        ]
    }
    
    analysis = agent.analyze_campaign_performance(campaign_data)
    print("Campaign Analysis:", analysis.dict())
    
    # A/B test analysis
    ab_test_data = {
        "test_name": "Email Subject Line Test",
        "variant_a": {"subject": "Save 20% Today", "opens": 450, "clicks": 90, "conversions": 15},
        "variant_b": {"subject": "Exclusive Deal Inside", "opens": 520, "clicks": 110, "conversions": 22}
    }
    
    ab_result = agent.analyze_ab_test(ab_test_data)
    print("\nA/B Test Result:", ab_result.dict())
    
    # ROI calculation
    roi_analysis = agent.calculate_roi(campaign_data["campaigns"])
    print("\nROI Analysis:", roi_analysis)