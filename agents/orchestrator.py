#!/usr/bin/env python3
"""
Marketing Agent Orchestrator

Coordinates multiple specialized marketing agents to provide comprehensive marketing solutions.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MarketingOrchestrator:
    """
    Orchestrates multiple marketing agents to provide comprehensive marketing solutions.
    """
    
    def __init__(self, auto_setup: bool = True):
        """Initialize the orchestrator with all available agents."""
        self.agents = {}
        self.vector_manager = None
        self.rag_system = None
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        if auto_setup:
            self._setup_vector_store()
        
        self._initialize_agents()
        logger.info("Marketing Orchestrator initialized with all agents")
    
    def _setup_vector_store(self):
        """Setup fresh vector store with data loading"""
        try:
            print("\n🚀 Setting up fresh vector store...")
            print("="*50)
            
            # Import vector manager
            from vector_manager import VectorStoreManager
            self.vector_manager = VectorStoreManager()
            
            # Initialize fresh vector store
            print("📋 Step 1: Initializing fresh vector store...")
            if self.vector_manager.initialize_fresh_vector_store():
                print("✅ Vector store initialized")
            else:
                print("❌ Failed to initialize vector store")
                return False
            
            # Load knowledge base data
            print("📋 Step 2: Loading knowledge base data...")
            load_result = self.vector_manager.load_knowledge_base_data()
            if load_result["status"] == "success":
                print(f"✅ Loaded {load_result['document_count']} documents into {load_result['chunk_count']} chunks")
            else:
                print(f"⚠️  Loading: {load_result['message']}")
            
            # Verify data loading
            print("📋 Step 3: Verifying data loading...")
            verification = self.vector_manager.verify_data_loading()
            if verification["verification_status"] == "success":
                print("✅ Data verification successful")
            else:
                print("❌ Data verification failed")
            
            # Get RAG system
            self.rag_system = self.vector_manager.get_rag_system()
            
            # Print status
            self.vector_manager.print_status()
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up vector store: {e}")
            print(f"❌ Vector store setup failed: {e}")
            return False
    
    def _initialize_agents(self):
        """Initialize all marketing agents."""
        try:
            # Import and initialize all agents
            from agents.analytics_agent import AnalyticsAgent
            from agents.content_planning_agent import ContentPlanningAgent
            from agents.market_research_agent import MarketResearchAgent
            from agents.newsletter_agent import NewsletterAgent
            from agents.presentation_agent import PresentationAgent
            
            self.agents = {
                'analytics': AnalyticsAgent(),
                'content_planning': ContentPlanningAgent(),
                'market_research': MarketResearchAgent(),
                'newsletter': NewsletterAgent(),
                'presentation': PresentationAgent()
            }
            
            logger.info(f"Initialized {len(self.agents)} agents: {list(self.agents.keys())}")
            
        except Exception as e:
            logger.error(f"Error initializing agents: {e}")
            # Initialize with empty dict if agents fail to load
            self.agents = {}
            logger.warning("Continuing with no agents loaded")
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agent names."""
        return list(self.agents.keys())
    
    def execute_single_agent(self, agent_name: str, method: str, **kwargs) -> Any:
        """Execute a specific method on a single agent."""
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found. Available: {list(self.agents.keys())}")
        
        agent = self.agents[agent_name]
        
        if not hasattr(agent, method):
            raise ValueError(f"Method '{method}' not found on agent '{agent_name}'")
        
        try:
            result = getattr(agent, method)(**kwargs)
            logger.info(f"Successfully executed {agent_name}.{method}")
            return result
        except Exception as e:
            logger.error(f"Error executing {agent_name}.{method}: {e}")
            raise   
 
    def comprehensive_marketing_analysis(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a comprehensive marketing analysis using multiple agents.
        
        Args:
            company_info: Dictionary containing company information
            
        Returns:
            Dictionary with results from all agents
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'company_info': company_info,
            'analysis': {}
        }
        
        if not self.agents:
            results['error'] = "No agents available"
            return results
        
        try:
            # 1. Market Research Analysis
            if 'market_research' in self.agents:
                logger.info("Running market research analysis...")
                market_analysis = self.agents['market_research'].analyze_market(
                    company_info=str(company_info),
                    specific_focus="competitive positioning and market opportunities"
                )
                results['analysis']['market_research'] = market_analysis
            
            # 2. Content Strategy Planning
            if 'content_planning' in self.agents:
                logger.info("Creating content strategy...")
                content_strategy = self.agents['content_planning'].create_content_strategy(
                    brand_info=company_info.get('name', 'Company'),
                    target_audience=company_info.get('target_audience', 'General audience'),
                    goals="brand awareness, lead generation, customer engagement"
                )
                results['analysis']['content_strategy'] = content_strategy
            
            # 3. Analytics Setup (if available)
            if 'analytics' in self.agents and hasattr(self.agents['analytics'], 'setup_tracking'):
                logger.info("Setting up analytics tracking...")
                analytics_setup = self.agents['analytics'].setup_tracking(
                    company_info=company_info
                )
                results['analysis']['analytics_setup'] = analytics_setup
            
            # 4. Newsletter Strategy (if available)
            if 'newsletter' in self.agents and hasattr(self.agents['newsletter'], 'create_newsletter_strategy'):
                logger.info("Creating newsletter strategy...")
                newsletter_strategy = self.agents['newsletter'].create_newsletter_strategy(
                    company_info=company_info
                )
                results['analysis']['newsletter_strategy'] = newsletter_strategy
            
            logger.info("Comprehensive marketing analysis completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            results['error'] = str(e)
            return results
    
    def create_marketing_presentation(self, company_info: Dict[str, Any], 
                                    presentation_type: str = "comprehensive") -> str:
        """
        Create a marketing presentation using the presentation agent.
        
        Args:
            company_info: Company information
            presentation_type: Type of presentation to create
            
        Returns:
            Generated presentation content
        """
        try:
            if 'presentation' not in self.agents:
                return "Presentation agent not available"
            
            logger.info(f"Creating {presentation_type} marketing presentation...")
            
            # Get comprehensive analysis first
            analysis = self.comprehensive_marketing_analysis(company_info)
            
            # Create presentation using the presentation agent
            presentation = self.agents['presentation'].create_presentation(
                topic=f"{company_info.get('name', 'Company')} Marketing Strategy",
                audience="stakeholders and marketing team",
                context=json.dumps(analysis, indent=2)
            )
            
            logger.info("Marketing presentation created successfully")
            return presentation
            
        except Exception as e:
            logger.error(f"Error creating presentation: {e}")
            return f"Error creating presentation: {str(e)}"   
 
    def run_marketing_workflow(self, workflow_type: str, **kwargs) -> Dict[str, Any]:
        """
        Run predefined marketing workflows.
        
        Args:
            workflow_type: Type of workflow to run
            **kwargs: Additional parameters for the workflow
            
        Returns:
            Workflow results
        """
        workflows = {
            'new_company_onboarding': self._new_company_workflow,
            'quarterly_review': self._quarterly_review_workflow,
            'campaign_planning': self._campaign_planning_workflow,
            'competitive_analysis': self._competitive_analysis_workflow
        }
        
        if workflow_type not in workflows:
            raise ValueError(f"Workflow '{workflow_type}' not found. Available: {list(workflows.keys())}")
        
        try:
            logger.info(f"Running {workflow_type} workflow...")
            result = workflows[workflow_type](**kwargs)
            logger.info(f"Workflow {workflow_type} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in workflow {workflow_type}: {e}")
            return {'error': str(e), 'workflow': workflow_type}
    
    def _new_company_workflow(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Workflow for new company onboarding."""
        results = {
            'workflow': 'new_company_onboarding',
            'timestamp': datetime.now().isoformat(),
            'steps': {}
        }
        
        # Step 1: Comprehensive analysis
        results['steps']['analysis'] = self.comprehensive_marketing_analysis(company_info)
        
        # Step 2: Create onboarding presentation
        results['steps']['presentation'] = self.create_marketing_presentation(
            company_info, "onboarding"
        )
        
        return results
    
    def _quarterly_review_workflow(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Workflow for quarterly marketing review."""
        results = {
            'workflow': 'quarterly_review',
            'timestamp': datetime.now().isoformat(),
            'steps': {}
        }
        
        # Market research update
        if 'market_research' in self.agents:
            results['steps']['market_update'] = self.execute_single_agent(
                'market_research', 'analyze_market',
                company_info=str(company_info),
                specific_focus="quarterly trends and competitive changes"
            )
        
        # Analytics review (if available)
        if 'analytics' in self.agents and hasattr(self.agents['analytics'], 'generate_report'):
            results['steps']['analytics_report'] = self.execute_single_agent(
                'analytics', 'generate_report',
                report_type="quarterly"
            )
        
        return results
    
    def _campaign_planning_workflow(self, campaign_info: Dict[str, Any]) -> Dict[str, Any]:
        """Workflow for campaign planning."""
        results = {
            'workflow': 'campaign_planning',
            'timestamp': datetime.now().isoformat(),
            'steps': {}
        }
        
        # Content planning for campaign
        if 'content_planning' in self.agents:
            results['steps']['content_plan'] = self.execute_single_agent(
                'content_planning', 'create_content_strategy',
                brand_info=campaign_info.get('brand', 'Campaign'),
                target_audience=campaign_info.get('audience', 'Target audience'),
                goals=campaign_info.get('goals', 'Campaign objectives')
            )
        
        return results
    
    def _competitive_analysis_workflow(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Workflow for competitive analysis."""
        results = {
            'workflow': 'competitive_analysis',
            'timestamp': datetime.now().isoformat(),
            'steps': {}
        }
        
        # Deep competitive analysis
        if 'market_research' in self.agents:
            results['steps']['competitive_research'] = self.execute_single_agent(
                'market_research', 'analyze_market',
                company_info=str(company_info),
                specific_focus="competitive landscape and positioning opportunities"
            )
        
        return results  
  
    def quick_demo(self, company_name: str = "Demo Company"):
        """Run a quick demo of the orchestrator capabilities."""
        print(f"🚀 Running Quick Demo for {company_name}")
        print("=" * 50)
        
        # Sample company info
        company_info = {
            'name': company_name,
            'industry': 'Technology',
            'target_audience': 'Small to medium businesses',
            'value_proposition': 'Innovative solutions for modern challenges'
        }
        
        print(f"Available agents: {', '.join(self.get_available_agents())}")
        
        if not self.agents:
            print("❌ No agents available. Please check agent initialization.")
            return
        
        # Run comprehensive analysis
        print("\n📊 Running comprehensive marketing analysis...")
        analysis = self.comprehensive_marketing_analysis(company_info)
        
        print(f"✅ Analysis completed with {len(analysis.get('analysis', {}))} components")
        
        # Show sample results
        for component, result in analysis.get('analysis', {}).items():
            print(f"\n📋 {component.replace('_', ' ').title()}:")
            if isinstance(result, str):
                print(result[:200] + "..." if len(result) > 200 else result)
            else:
                print(f"Generated {type(result).__name__} result")
        
        print(f"\n🎯 Demo completed successfully!")
        
        # Save demo results
        self._save_output({
            "demo_type": "quick_demo",
            "company_info": company_info,
            "analysis_results": analysis,
            "timestamp": datetime.now().isoformat()
        }, f"demo_results_{company_name.lower().replace(' ', '_')}.json")
    
    def interactive_mode(self):
        """Run the orchestrator in interactive mode."""
        print("🚀 Marketing Agent Orchestrator")
        print("=" * 50)
        print(f"Available agents: {', '.join(self.get_available_agents()) if self.agents else 'None'}")
        print("\nCommands:")
        print("1. 'demo [company_name]' - Run quick demo")
        print("2. 'analyze [company_name]' - Run comprehensive analysis")
        print("3. 'workflow [type]' - Run predefined workflow")
        print("4. 'agent [name] [method]' - Execute specific agent method")
        print("5. 'presentation [company_name]' - Create marketing presentation")
        print("6. 'help' - Show this help")
        print("7. 'quit' - Exit")
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if command.lower() == 'quit':
                    break
                elif command.lower() == 'help':
                    print("Available workflows: new_company_onboarding, quarterly_review, campaign_planning, competitive_analysis")
                    print(f"Available agents: {', '.join(self.get_available_agents())}")
                elif command.lower().startswith('demo'):
                    parts = command.split(' ', 1)
                    company_name = parts[1] if len(parts) > 1 else "Demo Company"
                    self.quick_demo(company_name)
                elif command.lower().startswith('analyze'):
                    parts = command.split(' ', 1)
                    company_name = parts[1] if len(parts) > 1 else input("Company name: ")
                    
                    company_info = {'name': company_name}
                    result = self.comprehensive_marketing_analysis(company_info)
                    print(json.dumps(result, indent=2))
                    
                elif command.lower().startswith('workflow'):
                    parts = command.split(' ', 1)
                    workflow_type = parts[1] if len(parts) > 1 else input("Workflow type: ")
                    
                    company_name = input("Company name: ")
                    company_info = {'name': company_name}
                    
                    result = self.run_marketing_workflow(workflow_type, company_info=company_info)
                    print(json.dumps(result, indent=2))
                    
                elif command.lower().startswith('presentation'):
                    parts = command.split(' ', 1)
                    company_name = parts[1] if len(parts) > 1 else input("Company name: ")
                    
                    company_info = {'name': company_name}
                    result = self.create_marketing_presentation(company_info)
                    print(result)
                    
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("\nGoodbye! 👋")
    
    def _save_output(self, data: Any, filename: str):
        """Save output data to file with terminal notification"""
        try:
            output_path = self.output_dir / filename
            
            if isinstance(data, (dict, list)):
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            
            print(f"💾 Saved output to: {output_path}")
            logger.info(f"Saved output to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving output: {e}")
            print(f"❌ Failed to save output: {e}")
    
    def comprehensive_analysis_with_output(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive analysis with detailed terminal output and file saving"""
        print(f"\n🚀 Starting Comprehensive Marketing Analysis for {company_info.get('name', 'Company')}")
        print("="*70)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'company_info': company_info,
            'analysis': {},
            'execution_log': []
        }
        
        if not self.agents:
            print("❌ No agents available")
            results['error'] = "No agents available"
            return results
        
        try:
            # 1. Market Research Analysis
            if 'market_research' in self.agents:
                print("\n📊 Running Market Research Analysis...")
                print("-" * 40)
                
                market_analysis = self.agents['market_research'].analyze_market(
                    company_info=str(company_info),
                    specific_focus="competitive positioning and market opportunities"
                )
                results['analysis']['market_research'] = market_analysis
                results['execution_log'].append("✅ Market research completed")
                
                print("✅ Market research analysis completed")
                print(f"📄 Preview: {market_analysis[:200]}...")
                
                # Save individual result
                self._save_output(market_analysis, f"market_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            
            # 2. Content Strategy Planning
            if 'content_planning' in self.agents:
                print("\n📝 Creating Content Strategy...")
                print("-" * 40)
                
                content_strategy = self.agents['content_planning'].create_content_strategy(
                    brand_info=company_info.get('name', 'Company'),
                    target_audience=company_info.get('target_audience', 'General audience'),
                    goals="brand awareness, lead generation, customer engagement"
                )
                results['analysis']['content_strategy'] = content_strategy
                results['execution_log'].append("✅ Content strategy completed")
                
                print("✅ Content strategy created")
                print(f"📄 Preview: {content_strategy[:200]}...")
                
                # Save individual result
                self._save_output(content_strategy, f"content_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            
            # 3. Presentation Creation
            if 'presentation' in self.agents:
                print("\n🎯 Creating Marketing Presentation...")
                print("-" * 40)
                
                presentation = self.agents['presentation'].create_presentation(
                    topic=f"{company_info.get('name', 'Company')} Marketing Strategy",
                    audience="stakeholders and marketing team",
                    context=json.dumps(company_info, indent=2),
                    slides_count=10
                )
                results['analysis']['presentation'] = presentation
                results['execution_log'].append("✅ Presentation created")
                
                print("✅ Marketing presentation created")
                print(f"📄 Preview: {presentation[:200]}...")
                
                # Save individual result
                self._save_output(presentation, f"presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            
            # 4. Analytics Setup (if available)
            if 'analytics' in self.agents and hasattr(self.agents['analytics'], 'setup_tracking'):
                print("\n📈 Setting up Analytics...")
                print("-" * 40)
                
                analytics_setup = self.agents['analytics'].setup_tracking(
                    company_info=company_info
                )
                results['analysis']['analytics_setup'] = analytics_setup
                results['execution_log'].append("✅ Analytics setup completed")
                
                print("✅ Analytics setup completed")
                print(f"📄 Preview: {analytics_setup[:200]}...")
            
            # 5. Newsletter Strategy (if available)
            if 'newsletter' in self.agents and hasattr(self.agents['newsletter'], 'create_newsletter_strategy'):
                print("\n📧 Creating Newsletter Strategy...")
                print("-" * 40)
                
                newsletter_strategy = self.agents['newsletter'].create_newsletter_strategy(
                    company_info=company_info
                )
                results['analysis']['newsletter_strategy'] = newsletter_strategy
                results['execution_log'].append("✅ Newsletter strategy completed")
                
                print("✅ Newsletter strategy created")
                print(f"📄 Preview: {newsletter_strategy[:200]}...")
            
            # Save comprehensive results
            print(f"\n🎉 Comprehensive Analysis Completed!")
            print(f"📊 Generated {len(results['analysis'])} analysis components")
            
            # Save complete analysis
            self._save_output(results, f"comprehensive_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            logger.info("Comprehensive marketing analysis completed successfully")
            return results
            
        except Exception as e:
            error_msg = f"Error in comprehensive analysis: {e}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            results['error'] = str(e)
            return results

def main():
    """Main entry point for the orchestrator."""
    try:
        orchestrator = MarketingOrchestrator()
        
        # Check if we have command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == 'demo':
                company_name = sys.argv[2] if len(sys.argv) > 2 else "Demo Company"
                orchestrator.quick_demo(company_name)
            else:
                print(f"Unknown command: {sys.argv[1]}")
                print("Usage: python orchestrator.py [demo] [company_name]")
        else:
            orchestrator.interactive_mode()
            
    except Exception as e:
        logger.error(f"Failed to start orchestrator: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()