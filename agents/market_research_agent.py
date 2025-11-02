
from .base_agent import BaseAgent

class MarketResearchAgent:
    def __init__(self, use_rag=True):
        self.agent = BaseAgent(model_name="gemini-2.5-flash", use_rag=use_rag)
        self.system_prompt = """You are an expert Market Research Analyst with deep expertise in competitive intelligence, market dynamics, and strategic positioning. Your role is to:

1. COMPETITIVE ANALYSIS: Identify direct and indirect competitors, analyze their strengths/weaknesses, pricing strategies, market positioning, and unique value propositions.

2. MARKET DYNAMICS: Assess market size, growth trends, customer segments, emerging opportunities, and potential threats or disruptions.

3. STRATEGIC INSIGHTS: Provide actionable recommendations for market entry, positioning, differentiation strategies, and tactical moves based on current market conditions.

4. TREND ANALYSIS: Identify emerging trends, technologies, consumer behaviors, and market shifts that could impact business strategy.

5. CUSTOMER INTELLIGENCE: Analyze target audience preferences, pain points, buying behaviors, and unmet needs in the market.

Deliver comprehensive, data-driven insights with specific recommendations and strategic implications. Focus on actionable intelligence that drives business decisions."""

    def analyze_market(self, company_info, specific_focus=None):
        """Conduct comprehensive market research analysis"""
        
        # Get relevant context if RAG is enabled
        context = ""
        if self.agent.use_rag:
            search_query = f"market research competitive analysis {company_info}"
            if specific_focus:
                search_query += f" {specific_focus}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=5)
            if relevant_docs:
                context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Company Information: {company_info}

{f"Specific Focus Areas: {specific_focus}" if specific_focus else ""}

Please provide a comprehensive market research analysis covering:
1. Competitive landscape and key players
2. Market size, trends, and growth opportunities  
3. Target audience analysis and customer segments
4. Strategic positioning recommendations
5. Tactical moves and market entry strategies
6. Emerging trends and future market outlook

{context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

def main():
    print("Market Research Agent initialized")
    
    agent = MarketResearchAgent(use_rag=False)
    
    company_info = "We are Eterna, we provide a service on unified trading terminal for different DEXs at one place"
    
    response = agent.analyze_market(company_info)
    print(response)

if __name__ == "__main__":
    main()