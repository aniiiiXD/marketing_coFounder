#!/usr/bin/env python3
"""
Integration Test Script

Tests the complete flow: Vector Store → RAG → Agents → Orchestrator → Output
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

def test_step_by_step_integration():
    """Test complete integration step by step"""
    
    print("🧪 INTEGRATION TEST - Step by Step")
    print("="*60)
    
    # Step 1: Test Vector Store Manager
    print("\n📋 STEP 1: Testing Vector Store Manager")
    print("-" * 40)
    
    try:
        from vector_manager import VectorStoreManager
        
        manager = VectorStoreManager()
        
        # Initialize fresh vector store
        print("🔄 Initializing fresh vector store...")
        if manager.initialize_fresh_vector_store():
            print("✅ Vector store initialized")
        else:
            print("❌ Vector store initialization failed")
            return False
        
        # Load data
        print("📊 Loading knowledge base data...")
        load_result = manager.load_knowledge_base_data()
        if load_result["status"] == "success":
            print(f"✅ Loaded {load_result['document_count']} documents")
        else:
            print(f"❌ Data loading failed: {load_result['message']}")
            return False
        
        # Verify
        print("🔍 Verifying data...")
        verification = manager.verify_data_loading()
        if verification["verification_status"] == "success":
            print("✅ Data verification passed")
        else:
            print("❌ Data verification failed")
            return False
            
    except Exception as e:
        print(f"❌ Step 1 failed: {e}")
        return False
    
    # Step 2: Test Individual Agents
    print("\n📋 STEP 2: Testing Individual Agents")
    print("-" * 40)
    
    try:
        from agents.presentation_agent import PresentationAgent
        from agents.market_research_agent import MarketResearchAgent
        
        # Test presentation agent
        print("🎯 Testing Presentation Agent...")
        pres_agent = PresentationAgent(use_rag=True)
        presentation = pres_agent.create_presentation(
            topic="Test Marketing Strategy",
            audience="test audience",
            slides_count=5
        )
        if presentation and len(presentation) > 100:
            print("✅ Presentation agent working")
        else:
            print("❌ Presentation agent failed")
        
        # Test market research agent
        print("📊 Testing Market Research Agent...")
        market_agent = MarketResearchAgent(use_rag=True)
        market_analysis = market_agent.analyze_market(
            company_info="Test Company in Technology sector"
        )
        if market_analysis and len(market_analysis) > 100:
            print("✅ Market research agent working")
        else:
            print("❌ Market research agent failed")
            
    except Exception as e:
        print(f"❌ Step 2 failed: {e}")
        return False
    
    # Step 3: Test Orchestrator
    print("\n📋 STEP 3: Testing Orchestrator Integration")
    print("-" * 40)
    
    try:
        from agents.orchestrator import MarketingOrchestrator
        
        # Initialize orchestrator (should auto-setup)
        print("🚀 Initializing orchestrator...")
        orchestrator = MarketingOrchestrator(auto_setup=False)  # Skip auto-setup since we already did it
        orchestrator.rag_system = manager.get_rag_system()
        
        # Test comprehensive analysis
        print("📊 Running comprehensive analysis...")
        company_info = {
            'name': 'Test Integration Company',
            'industry': 'Technology',
            'target_audience': 'Small businesses'
        }
        
        results = orchestrator.comprehensive_analysis_with_output(company_info)
        
        if results and 'analysis' in results and len(results['analysis']) > 0:
            print(f"✅ Orchestrator generated {len(results['analysis'])} analysis components")
        else:
            print("❌ Orchestrator analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ Step 3 failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 4: Verify Outputs
    print("\n📋 STEP 4: Verifying Output Files")
    print("-" * 40)
    
    try:
        output_dir = Path("outputs")
        if output_dir.exists():
            output_files = list(output_dir.glob("*"))
            print(f"✅ Found {len(output_files)} output files:")
            for file in output_files[-5:]:  # Show last 5 files
                print(f"   📄 {file.name}")
        else:
            print("❌ No output directory found")
            return False
            
    except Exception as e:
        print(f"❌ Step 4 failed: {e}")
        return False
    
    print("\n🎉 INTEGRATION TEST COMPLETED SUCCESSFULLY!")
    print("="*60)
    return True

def test_main_py_integration():
    """Test main.py integration"""
    
    print("\n🧪 TESTING MAIN.PY INTEGRATION")
    print("="*50)
    
    try:
        # Test demo mode
        print("🎯 Testing demo mode...")
        os.system("python main.py demo 'Integration Test Company'")
        
        print("✅ Main.py integration test completed")
        
    except Exception as e:
        print(f"❌ Main.py test failed: {e}")

def main():
    """Run all integration tests"""
    
    # Run step-by-step integration test
    success = test_step_by_step_integration()
    
    if success:
        # Test main.py if step-by-step passed
        test_main_py_integration()
    else:
        print("❌ Step-by-step integration failed. Skipping main.py test.")

if __name__ == "__main__":
    main()