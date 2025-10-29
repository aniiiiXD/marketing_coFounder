"""
Base Agent for Gemini API Integration

This module provides a base class for creating AI agents that use Google's Gemini API.
It handles common functionality like API initialization, request formatting, and response handling.
"""

"""
Base Agent for AI Agent Infrastructure

This module provides a base class for all AI agents with:
- Standardized structured JSON output
- Error handling and validation
- Common configuration and utilities
- Response formatting and parsing
"""

from typing import Dict, Any, Optional, Type, TypeVar, Generic
from pydantic import BaseModel, ValidationError
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

T = TypeVar('T', bound=BaseModel)

class BaseAgent(Generic[T]):
    """
    Base class for all AI agents with structured output support.
    
    This class provides common functionality for all agents, including:
    - Structured JSON response handling
    - Error handling and validation
    - Request/response logging
    - Configuration management
    
    Child classes should implement specific agent functionality and response models.
    """
    
    def __init__(self, 
                 model_name: str = "gemini-2.5-flash", 
                 temperature: float = 0.3, 
                 max_tokens: int = 2000):
        """
        Initialize the base agent with common configuration.
        
        Args:
            model_name: The AI model to use (default: "gemini-2.5-flash")
            temperature: Controls response randomness (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_instruction = self.get_system_instruction()
        self.response_model = self.get_response_model()
        
        # Initialize the AI client
        self.client = genai.Client()
        
        logger.info(f"Initialized {self.__class__.__name__} with model {model_name}")
    
    def get_system_instruction(self) -> str:
        """
        Define the system instruction for the agent.
        
        This method should be overridden by child classes to provide
        specific instructions for each agent type.
        
        Returns:
            str: The system instruction for the agent
        """
        return """
        You are a helpful AI assistant. Your responses should be clear, 
        concise, and focused on providing helpful information.
        
        IMPORTANT: Your response MUST be a valid JSON object. 
        The JSON should be well-formatted and include all necessary data 
        to answer the query completely.
        """
    
    def get_response_model(self) -> Type[BaseModel]:
        """
        Define the Pydantic model for validating responses.
        
        This method should be overridden by child classes to provide
        a specific response model for validation.
        
        Returns:
            Type[BaseModel]: A Pydantic model class for response validation
        """
        class DefaultResponse(BaseModel):
            response: str
            
        return DefaultResponse
    
    def _validate_response(self, data: Dict[str, Any]) -> T:
        """
        Validate the response against the defined model.
        
        Args:
            data: The response data to validate
            
        Returns:
            T: Validated response model instance
            
        Raises:
            ValueError: If validation fails
        """
        try:
            return self.response_model(**data)
        except ValidationError as e:
            logger.error(f"Response validation failed: {e}")
            raise ValueError(f"Response validation failed: {e}")
    
    def _generate_structured_response(
        self, 
        prompt: str, 
        response_format: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> T:
        """
        Generate a structured response from the AI model.
        
        Args:
            prompt: The user's input prompt
            response_format: Optional JSON schema for the response
            **kwargs: Additional configuration overrides
            
        Returns:
            T: Validated response model instance
            
        Raises:
            ValueError: If the response cannot be generated or validated
        """
        # Prepare the full prompt with JSON formatting instructions
        full_prompt = prompt
        if response_format:
            format_instruction = f"""
            Respond with a JSON object that follows this exact structure:
            {json.dumps(response_format, indent=2)}
            
            Ensure the response is valid JSON and includes all required fields.
            """
            full_prompt = f"{prompt}\n\n{format_instruction}"
        else:
            full_prompt = f"{prompt}\n\nRespond with a valid JSON object containing your response."
        
        try:
            # Configure the API request
            config = {
                "model": self.model_name,
                "config": types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=kwargs.get('temperature', self.temperature),
                    max_output_tokens=kwargs.get('max_tokens', self.max_tokens),
                ),
                "contents": [{"role": "user", "parts": [{"text": full_prompt}]}]
            }
            
            # Make the API call
            logger.info(f"Sending request to {self.model_name}")
            response = self.client.models.generate_content(**config)
            
            # Parse the response
            response_text = response.text.strip()
            try:
                response_data = json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse response as JSON: {e}")
                logger.debug(f"Raw response: {response_text}")
                raise ValueError("The response could not be parsed as valid JSON")
            
            # Validate against the response model
            return self._validate_response(response_data)
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    def generate_response(self, *args, **kwargs) -> T:
        """
        Generate a response using the agent's specific implementation.
        
        This method should be implemented by child classes to provide
        domain-specific functionality.
        
        Returns:
            T: The generated response, validated against the response model
            
        Raises:
            NotImplementedError: If not implemented by child class
        """
        raise NotImplementedError("Subclasses must implement generate_response")
