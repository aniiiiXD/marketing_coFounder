#!/usr/bin/env python3
"""
Example usage of the Presentation Agent

This script demonstrates various ways to use the presentation agent
for creating, analyzing, and enhancing presentations.
"""

import sys
import os
sys.path.append('agents')

def presentation_examples():
    """Demonstrate various presentation agent capabilities"""
    
    try:
        from agents.presentation_agent import PresentationAgent
        
        print("🎯 Presentation Agent Examples")
        print("=" * 50)
        
        # Initialize agent
        agent = PresentationAgent(use_rag=True)
        
        # Example 1: Create a marketing presentation
        print("\n📊 Example 1: Creating Marketing Presentation")
        print("-" * 40)
        
        marketing_presentation = agent.create_presentation(
            topic="Q1 Marketing Campaign Results",
            audience="marketing team and executives",
            context="Focus on ROI, customer acquisition, and brand awareness metrics",
            slides_count=12
        )
        
        print("✅ Marketing presentation created")
        print(f"Preview: {marketing_presentation[:400]}...\n")
        
        # Example 2: Analyze existing slide content
        print("📋 Example 2: Analyzing Slide Structure")
        print("-" * 40)
        
        sample_slides = """
        Slide 1: Company Overview
        - Founded in 2020
        - 50+ employees
        - $2M ARR
        
        Slide 2: Market Opportunity
        - $10B market size
        - 15% annual growth
        - Underserved SMB segment
        
        Slide 3: Our Solution
        - AI-powered platform
        - 50% cost reduction
        - 3x faster implementation
        """
        
        structure_analysis = agent.analyze_slide_structure(
            slide_data=sample_slides,
            analysis_focus="logical flow and content balance"
        )
        
        print("✅ Structure analysis completed")
        print(f"Analysis: {structure_analysis[:400]}...\n")
        
        # Example 3: Extract key insights
        print("🔍 Example 3: Extracting Key Insights")
        print("-" * 40)
        
        insights = agent.extract_key_insights(sample_slides)
        
        print("✅ Key insights extracted")
        print(f"Insights: {insights[:400]}...\n")
        
        # Example 4: Create executive summary
        print("📄 Example 4: Executive Summary")
        print("-" * 40)
        
        exec_summary = agent.convert_to_executive_summary(sample_slides)
        
        print("✅ Executive summary created")
        print(f"Summary: {exec_summary[:400]}...\n")
        
        # Example 5: Generate speaker notes
        print("🎤 Example 5: Speaker Notes")
        print("-" * 40)
        
        speaker_notes = agent.generate_speaker_notes(
            slide_content=sample_slides,
            presentation_duration=20
        )
        
        print("✅ Speaker notes generated")
        print(f"Notes: {speaker_notes[:400]}...\n")
        
        print("🎉 All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in examples: {e}")
        import traceback
        traceback.print_exc()

def interactive_presentation_demo():
    """Interactive demo for presentation agent"""
    
    try:
        from agents.presentation_agent import PresentationAgent
        
        print("🎯 Interactive Presentation Demo")
        print("=" * 40)
        
        agent = PresentationAgent(use_rag=True)
        
        while True:
            print("\nChoose an option:")
            print("1. Create new presentation")
            print("2. Analyze slide content")
            print("3. Extract key insights")
            print("4. Generate speaker notes")
            print("5. Create executive summary")
            print("6. Quit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                topic = input("Enter presentation topic: ")
                audience = input("Enter target audience: ")
                slides = input("Number of slides (default 10): ") or "10"
                
                result = agent.create_presentation(
                    topic=topic,
                    audience=audience,
                    slides_count=int(slides)
                )
                print(f"\n📊 Generated Presentation:\n{result}\n")
                
            elif choice == '2':
                content = input("Enter slide content to analyze: ")
                
                result = agent.analyze_slide_structure(content)
                print(f"\n📋 Structure Analysis:\n{result}\n")
                
            elif choice == '3':
                content = input("Enter presentation content: ")
                
                result = agent.extract_key_insights(content)
                print(f"\n🔍 Key Insights:\n{result}\n")
                
            elif choice == '4':
                content = input("Enter slide content: ")
                duration = input("Presentation duration in minutes (default 30): ") or "30"
                
                result = agent.generate_speaker_notes(content, int(duration))
                print(f"\n🎤 Speaker Notes:\n{result}\n")
                
            elif choice == '5':
                content = input("Enter presentation content: ")
                
                result = agent.convert_to_executive_summary(content)
                print(f"\n📄 Executive Summary:\n{result}\n")
                
            elif choice == '6':
                print("Goodbye! 👋")
                break
                
            else:
                print("Invalid choice. Please try again.")
                
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function to run examples or interactive demo"""
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_presentation_demo()
    else:
        presentation_examples()

if __name__ == "__main__":
    main()