#!/usr/bin/env python3
"""
Main entry point for the Marketing Agent system.
"""

# Load environment variables first
from dotenv import load_dotenv
import os
import sys

# Load .env file from the project root
load_dotenv()

# Verify required environment variables
if not os.getenv('GOOGLE_API_KEY'):
    print("Error: GOOGLE_API_KEY environment variable is not set.")
    print("Please check your .env file in the project root contains:")
    print("GOOGLE_API_KEY=your_api_key_here")
    exit(1)

def main():
    """Main entry point with integrated setup"""
    print("🚀 Marketing Agent System - Integrated Setup")
    print("="*60)
    
    try:
        # Import orchestrator
        from agents.orchestrator import MarketingOrchestrator
        
        # Initialize orchestrator with auto-setup
        print("📋 Initializing Marketing Orchestrator...")
        orchestrator = MarketingOrchestrator(auto_setup=True)
        
        # Check if we have command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == 'demo':
                company_name = sys.argv[2] if len(sys.argv) > 2 else "Demo Company"
                print(f"\n🎯 Running demo for: {company_name}")
                orchestrator.quick_demo(company_name)
            elif sys.argv[1] == 'analyze':
                company_name = sys.argv[2] if len(sys.argv) > 2 else "Demo Company"
                company_info = {
                    'name': company_name,
                    'industry': 'Technology',
                    'target_audience': 'Small to medium businesses'
                }
                print(f"\n📊 Running comprehensive analysis for: {company_name}")
                orchestrator.comprehensive_analysis_with_output(company_info)
            else:
                print(f"Unknown command: {sys.argv[1]}")
                print("Usage: python main.py [demo|analyze] [company_name]")
        else:
            # Run interactive mode
            orchestrator.interactive_mode()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
        