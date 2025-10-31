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

import json
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
        
        # Get and validate API key
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set. Please check your .env file.")
            
        print(f"Using API Key: {self.api_key[:10]}...{self.api_key[-4:]}")
        
        # Initialize the AI client with API key
        self.client = genai.Client(api_key=self.api_key)
        
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
        Generate a structured response using the AI model.
        
        Args:
            prompt: The input prompt or message
            response_format: Optional schema for the expected response format
            **kwargs: Additional parameters for the generation
            
        Returns:
            An instance of the response model with the generated content
            
        Raises:
            ValueError: If the response cannot be generated or validated
        """
        try:
            # Generate the response using the specified template
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disables thinking
                ),
                **kwargs
            )
            
            # Parse and validate the response
            response_json = response.json()
            # Extract the text content from the Gemini response
            if 'candidates' in response_json and len(response_json['candidates']) > 0:
                candidate = response_json['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                    content = candidate['content']['parts'][0]['text']
                    try:
                        # Try to parse the content as JSON if it's a JSON string
                        content_json = json.loads(content)
                        return self._validate_response(content_json)
                    except json.JSONDecodeError:
                        # If it's not a JSON string, try to use it as is
                        return self._validate_response({"response": content})
            
            # If we can't extract structured content, try to validate the full response
            return self._validate_response(response_json)
            
        except Exception as e:
            logger.error(f"Error in generate: {str(e)}")
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



# Test the API connection when this module is run directly
# if __name__ == "__main__":
#     import asyncio
    
#     async def test_api_connection():
#         print("\n=== Testing API Connection ===")
        
#         # Create a test agent
#         test_agent = BaseAgent()
        
#         try:
#             # Test the API with a simple prompt
#             print("\nSending test request to Gemini API...")
#             response = test_agent.client.models.generate_content(
#                 model="gemini-2.5-flash",
#                 contents="Hello, Gemini! This is a test. Please respond with a short greeting.",
#                 config=types.GenerateContentConfig(
#                     thinking_config=types.ThinkingConfig(thinking_budget=0)
#                 )
#             )
            
#             print("\n=== Test Successful! ===")
#             print("API Response:")
#             print(response.text)
            
#         except Exception as e:
#             print("\n=== Test Failed! ===")
#             print(f"Error: {str(e)}")
#             if "API key" in str(e):
#                 print("\nTroubleshooting:")
#                 print("1. Make sure you have a .env file in your project root")
#                 print("2. Verify it contains: GOOGLE_API_KEY=your_actual_api_key")
#                 print("3. The .env file should be in the same directory as main.py")
    
#     # Run the test
#     asyncio.run(test_api_connection())