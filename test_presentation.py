#!/usr/bin/env python3
"""
Test script for the presentation agent
"""

import sys
import os
sys.path.append('agents')

def test_presentation_agent():
    """Test the presentation agent functionality"""
    try:
        from agents.presentation_agent import PresentationAgent
        
        print("🎯 Testing Presentation Agent")
        print("=" * 40)
        
        # Initialize the agent
        agent = PresentationAgent(use_rag=False)  # Disable RAG for testing
        print("✅ Agent initialized successfully")
        
        # Test create_presentation method
        print("\n📊 Testing presentation creation...")
        presentation = agent.create_presentation(
            topic="Marketing Strategy for Tech Startup",
            audience="investors and stakeholders",
            slides_count=8
        )
        
        print("✅ Presentation created successfully")
        print(f"📄 Preview (first 300 chars): {presentation[:300]}...")
        
        # Test extract_key_insights method
        print("\n🔍 Testing key insights extraction...")
        insights = agent.extract_key_insights(presentation[:1000])  # Use part of the presentation
        
        print("✅ Key insights extracted successfully")
        print(f"📋 Insights preview (first 200 chars): {insights[:200]}...")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_presentation_agent()
    sys.exit(0 if success else 1)