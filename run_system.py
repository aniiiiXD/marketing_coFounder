#!/usr/bin/env python3
"""
Simple Run Script for Marketing Agent System

This script provides easy commands to run the complete system.
"""

import sys
import os
from pathlib import Path

def print_usage():
    """Print usage instructions"""
    print("🚀 Marketing Agent System - Run Commands")
    print("="*50)
    print("Usage: python run_system.py [command] [options]")
    print("\nCommands:")
    print("  setup          - Initialize fresh vector store and load data")
    print("  demo [name]    - Run quick demo (default: Demo Company)")
    print("  analyze [name] - Run comprehensive analysis")
    print("  interactive    - Start interactive mode")
    print("  test           - Run integration tests")
    print("  status         - Show system status")
    print("\nExamples:")
    print("  python run_system.py setup")
    print("  python run_system.py demo 'TechCorp'")
    print("  python run_system.py analyze 'MyCompany'")
    print("  python run_system.py interactive")

def run_setup():
    """Run vector store setup"""
    print("🔧 Setting up vector store...")
    
    try:
        from vector_manager import VectorStoreManager
        
        manager = VectorStoreManager()
        
        # Initialize and load data
        if manager.initialize_fresh_vector_store():
            load_result = manager.load_knowledge_base_data()
            verification = manager.verify_data_loading()
            manager.print_status()
            
            if verification["verification_status"] == "success":
                print("\n✅ Setup completed successfully!")
                return True
            else:
                print("\n❌ Setup verification failed")
                return False
        else:
            print("\n❌ Setup failed")
            return False
            
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def run_demo(company_name="Demo Company"):
    """Run demo mode"""
    print(f"🎯 Running demo for: {company_name}")
    
    try:
        from agents.orchestrator import MarketingOrchestrator
        
        orchestrator = MarketingOrchestrator(auto_setup=True)
        orchestrator.quick_demo(company_name)
        
        print("\n✅ Demo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

def run_analysis(company_name="Demo Company"):
    """Run comprehensive analysis"""
    print(f"📊 Running comprehensive analysis for: {company_name}")
    
    try:
        from agents.orchestrator import MarketingOrchestrator
        
        orchestrator = MarketingOrchestrator(auto_setup=True)
        
        company_info = {
            'name': company_name,
            'industry': 'Technology',
            'target_audience': 'Small to medium businesses',
            'value_proposition': 'Innovative solutions for modern challenges'
        }
        
        results = orchestrator.comprehensive_analysis_with_output(company_info)
        
        print(f"\n✅ Analysis completed with {len(results.get('analysis', {}))} components!")
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")

def run_interactive():
    """Run interactive mode"""
    print("🎮 Starting interactive mode...")
    
    try:
        from agents.orchestrator import MarketingOrchestrator
        
        orchestrator = MarketingOrchestrator(auto_setup=True)
        orchestrator.interactive_mode()
        
    except Exception as e:
        print(f"❌ Interactive mode error: {e}")

def run_test():
    """Run integration tests"""
    print("🧪 Running integration tests...")
    
    try:
        from test_integration import test_step_by_step_integration
        
        success = test_step_by_step_integration()
        
        if success:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed!")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

def show_status():
    """Show system status"""
    print("📊 Checking system status...")
    
    try:
        from vector_manager import VectorStoreManager
        
        manager = VectorStoreManager()
        
        # Try to initialize (won't clear if exists)
        if manager.initialize_fresh_vector_store():
            manager.print_status()
        else:
            print("❌ Could not access vector store")
            
    except Exception as e:
        print(f"❌ Status error: {e}")

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        run_setup()
    elif command == "demo":
        company_name = sys.argv[2] if len(sys.argv) > 2 else "Demo Company"
        run_demo(company_name)
    elif command == "analyze":
        company_name = sys.argv[2] if len(sys.argv) > 2 else "Demo Company"
        run_analysis(company_name)
    elif command == "interactive":
        run_interactive()
    elif command == "test":
        run_test()
    elif command == "status":
        show_status()
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()

if __name__ == "__main__":
    main()