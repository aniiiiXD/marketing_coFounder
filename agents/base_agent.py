"""
Base Agent for Gemini API Integration with RAG System

Completely flexible - does not control response structure or format.
"""

from typing import Dict, Any, Optional, List
from google import genai
from google.genai import types
from dotenv import load_dotenv
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class BaseAgent:
    """
    Base class for all AI agents with RAG integration.
    Completely flexible - agents control their own response format.
    """
    
    def __init__(self, 
                 model_name: str = "gemini-2.5-flash", 
                 use_rag: bool = True):
        """
        Initialize the base agent.
        
        Args:
            model_name: The AI model to use (default: "gemini-2.5-flash")
            use_rag: Whether to integrate with RAG system for knowledge retrieval
        """
        self.model_name = model_name
        self.use_rag = use_rag
        
        # Initialize the AI client
        self.client = genai.Client()
        
        # Initialize RAG system if enabled
        self.rag_system = None
        if self.use_rag:
            try:
                from rag.rag_system import MarketingRAGSystem
                self.rag_system = MarketingRAGSystem()
                logger.info(f"RAG system integrated for {self.__class__.__name__}")
            except Exception as e:
                logger.warning(f"Could not initialize RAG system: {e}")
                self.use_rag = False
        
        logger.info(f"Initialized {self.__class__.__name__} with model {model_name}")
    
    def get_relevant_context(self, query: str, filters: Optional[Dict[str, Any]] = None, n_results: int = 5) -> List[str]:
        """
        Retrieve relevant context from the RAG system.
        Public method for agents to use as needed.
        """
        if not self.use_rag or not self.rag_system:
            return []
        
        try:
            results = self.rag_system.vector_store.search(query, n_results=n_results, filters=filters)
            return [result["document"] for result in results]
        except Exception as e:
            logger.warning(f"Error retrieving context: {e}")
            return []
    
    def generate_response(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        **config_kwargs
    ) -> str:
        """
        Generate a response using the Gemini API.
        Completely flexible - no structure imposed.
        
        Args:
            prompt: The input prompt or message
            system_instruction: Optional system instruction (agent can provide their own)
            **config_kwargs: Additional configuration for GenerateContentConfig
            
        Returns:
            str: The raw generated response
        """
        try:
            # Build config
            config_params = {}
            if system_instruction:
                config_params["system_instruction"] = system_instruction
            
            # Add any additional config parameters
            config_params.update(config_kwargs)
            
            # Generate the response using the Gemini API
            response = self.client.models.generate_content(
                model=self.model_name,
                config=types.GenerateContentConfig(**config_params),
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"