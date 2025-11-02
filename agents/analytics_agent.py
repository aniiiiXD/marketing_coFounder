from base_agent import BaseAgent

class AnalyticsAgent:
    def __init__(self, use_rag=True):
        self.agent = BaseAgent(model_name="gemini-2.5-flash", use_rag=use_rag)
        self.system_prompt = """You are a Senior Data Analytics Specialist with expertise in business intelligence, performance metrics, and data-driven decision making. Your role is to:

1. PERFORMANCE ANALYSIS: Analyze key performance indicators (KPIs), conversion rates, user engagement metrics, and business performance data to identify trends and insights.

2. DATA INTERPRETATION: Transform raw data into actionable insights, identify patterns, correlations, and anomalies that impact business outcomes.

3. PREDICTIVE ANALYTICS: Use historical data to forecast trends, predict user behavior, and anticipate market changes that could affect business strategy.

4. REPORTING & VISUALIZATION: Create clear, compelling data narratives that communicate complex analytics in an accessible format for stakeholders.

5. OPTIMIZATION RECOMMENDATIONS: Provide specific, data-backed recommendations for improving performance, reducing costs, and maximizing ROI.

6. A/B TESTING & EXPERIMENTATION: Design and analyze experiments to validate hypotheses and optimize business processes.

Deliver precise, quantitative insights with clear methodology, statistical significance, and actionable recommendations. Focus on metrics that directly impact business growth and user experience."""

    def analyze_performance(self, data_context, analysis_type="comprehensive"):
        """Conduct comprehensive analytics analysis"""
        
        # Get relevant context if RAG is enabled
        context = ""
        if self.agent.use_rag:
            search_query = f"analytics performance data analysis {data_context} {analysis_type}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=5)
            if relevant_docs:
                context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Data Context: {data_context}

Analysis Type: {analysis_type}

Please provide a comprehensive analytics analysis covering:
1. Key performance indicators and metrics analysis
2. Trend identification and pattern recognition
3. User behavior and engagement insights
4. Conversion funnel analysis and optimization opportunities
5. Predictive insights and forecasting
6. Data-driven recommendations for improvement
7. Risk assessment and mitigation strategies

{context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def create_dashboard_insights(self, metrics_data):
        """Generate insights for dashboard visualization"""
        
        context = ""
        if self.agent.use_rag:
            search_query = f"dashboard analytics visualization metrics {metrics_data}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Metrics Data: {metrics_data}

Create dashboard-ready insights including:
1. Key metric summaries with trend indicators
2. Alert conditions and threshold recommendations
3. Visualization suggestions for different data types
4. Executive summary with top 3 insights
5. Action items based on current performance

{context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

def main():
    print("Analytics Agent initialized")
    
    agent = AnalyticsAgent(use_rag=False)
    
    data_context = "Eterna unified trading terminal - user engagement, transaction volumes, and platform performance metrics"
    
    response = agent.analyze_performance(data_context)
    print(response)

if __name__ == "__main__":
    main()