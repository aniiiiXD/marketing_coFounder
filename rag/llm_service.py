"""
LLM Service - Google Gemini Implementation

Provides interface to Google Gemini API for text generation and chat.
"""

import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMService:
    """Google Gemini LLM service"""
    
    def __init__(self):
        """Initialize Gemini API"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("LLM Service initialized with Gemini Pro")
    
    def generate_text(self, prompt: str, context: Optional[List[str]] = None) -> str:
        """Generate text response with optional context"""
        try:
            # Build full prompt with context
            full_prompt = self._build_prompt_with_context(prompt, context)
            
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                logger.info("Generated text response successfully")
                return response.text
            else:
                logger.warning("Empty response from LLM")
                return "I apologize, but I couldn't generate a response. Please try rephrasing your request."
                
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return f"Error generating response: {str(e)}"
    
    def generate_marketing_content(
        self, 
        content_type: str, 
        topic: str, 
        target_audience: str,
        context: Optional[List[str]] = None,
        additional_params: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate specific marketing content"""
        
        # Build marketing-specific prompt
        prompt = self._build_marketing_prompt(
            content_type, topic, target_audience, additional_params
        )
        
        return self.generate_text(prompt, context)
    
    def analyze_with_context(self, query: str, context: List[str]) -> str:
        """Analyze query using provided context"""
        analysis_prompt = f"""
        Based on the following company and marketing context, please analyze and respond to this query:
        
        Query: {query}
        
        Context Information:
        {chr(10).join(f"- {ctx}" for ctx in context)}
        
        Please provide a detailed, actionable response that takes into account the specific context provided.
        """
        
        return self.generate_text(analysis_prompt)
    
    def _build_prompt_with_context(self, prompt: str, context: Optional[List[str]] = None) -> str:
        """Build prompt with context information"""
        if not context:
            return prompt
        
        context_text = "\n".join(f"Context: {ctx}" for ctx in context)
        
        return f"""
        {context_text}
        
        Based on the above context, please respond to:
        {prompt}
        """
    
    def _build_marketing_prompt(
        self, 
        content_type: str, 
        topic: str, 
        target_audience: str,
        additional_params: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build marketing-specific prompts"""
        
        base_prompt = f"""
        Create {content_type} content about: {topic}
        Target Audience: {target_audience}
        """
        
        if additional_params:
            for key, value in additional_params.items():
                base_prompt += f"\n{key.replace('_', ' ').title()}: {value}"
        
        # Add content-type specific instructions
        if content_type.lower() == "newsletter":
            base_prompt += "\n\nPlease include: engaging subject line, clear sections, call-to-action, and professional tone."
        elif content_type.lower() == "blog post":
            base_prompt += "\n\nPlease include: compelling headline, introduction, main points with subheadings, and conclusion."
        elif content_type.lower() == "social media":
            base_prompt += "\n\nPlease make it engaging, concise, and include relevant hashtags."
        elif content_type.lower() == "campaign strategy":
            base_prompt += "\n\nPlease include: objectives, key messages, channels, timeline, and success metrics."
        
        return base_prompt
