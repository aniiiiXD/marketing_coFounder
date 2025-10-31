#!/usr/bin/env python3
"""
Main entry point for the Marketing Agent system.
"""

# Load environment variables first
from dotenv import load_dotenv
import os
import asyncio

# Load .env file from the project root
load_dotenv()

# Verify required environment variables
if not os.getenv('GOOGLE_API_KEY'):
    print("Error: GOOGLE_API_KEY environment variable is not set.")
    print("Please check your .env file in the project root contains:")
    print("GOOGLE_API_KEY=your_api_key_here")
    exit(1)

# Now import the orchestrator
from agents.orchestrator import main as run_orchestrator

if __name__ == "__main__":
    asyncio.run(run_orchestrator())
 