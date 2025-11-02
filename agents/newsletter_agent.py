from base_agent import BaseAgent

class NewsletterAgent:
    def __init__(self, use_rag=True):
        self.agent = BaseAgent(model_name="gemini-2.5-flash", use_rag=use_rag)
        self.system_prompt = """You are an expert Newsletter Content Generator specializing in creating engaging, informative newsletters based on current news and contextual information. Your role is to:

1. NEWS SYNTHESIS: Transform raw news articles, industry updates, and trending topics into digestible, engaging newsletter content that provides value to readers.

2. CONTEXTUAL STORYTELLING: Weave together multiple news sources and context to create coherent narratives that help readers understand the bigger picture and implications.

3. AUDIENCE-FOCUSED WRITING: Adapt complex information into accessible, engaging content that matches the audience's knowledge level and interests.

4. NEWSLETTER FORMATTING: Structure content with compelling headlines, clear sections, bullet points, and smooth transitions that enhance readability and engagement.

5. ACTIONABLE INSIGHTS: Extract key takeaways, trends, and actionable insights from news and context to provide real value beyond just information sharing.

6. BRAND VOICE INTEGRATION: Seamlessly incorporate brand messaging and positioning while maintaining editorial credibility and reader trust.

Generate complete newsletter content including subject lines, main body sections, key highlights, and calls-to-action. Focus on creating newsletters that inform, engage, and drive reader action."""

    def create_newsletter_strategy(self, brand_info, subscriber_profile, newsletter_goals):
        """Develop comprehensive newsletter strategy"""
        
        # Get relevant context if RAG is enabled
        context = ""
        if self.agent.use_rag:
            search_query = f"newsletter strategy email marketing {brand_info}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=5)
            if relevant_docs:
                context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Brand Information: {brand_info}

Subscriber Profile: {subscriber_profile}

Newsletter Goals: {newsletter_goals}

Please develop a comprehensive newsletter strategy including:
1. Newsletter positioning and unique value proposition
2. Content pillars and recurring newsletter sections
3. Publishing frequency and optimal send times
4. Subscriber segmentation and personalization strategy
5. Welcome sequence and onboarding flow
6. Engagement tactics and interactive elements
7. Monetization opportunities and conversion strategies
8. Growth tactics for subscriber acquisition
9. Performance metrics and success indicators

{context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def generate_newsletter_content(self, newsletter_theme, target_segment, key_updates):
        """Generate specific newsletter content"""
        
        context = ""
        if self.agent.use_rag:
            search_query = f"newsletter content {newsletter_theme} {target_segment}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Newsletter Theme: {newsletter_theme}

Target Segment: {target_segment}

Key Updates/News: {key_updates}

Create engaging newsletter content including:
1. Compelling subject line options (3-5 variations)
2. Engaging opening hook and preview text
3. Main content sections with clear value propositions
4. Industry insights and trending topics
5. Company updates and product highlights
6. Educational content and actionable tips
7. Strong call-to-action and next steps
8. Social proof and community highlights
9. Closing with personality and brand voice

{context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def optimize_newsletter_performance(self, current_metrics, improvement_goals):
        """Provide newsletter optimization recommendations"""
        
        context = ""
        if self.agent.use_rag:
            search_query = f"newsletter optimization email marketing metrics"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Current Newsletter Metrics: {current_metrics}

Improvement Goals: {improvement_goals}

Provide optimization recommendations including:
1. Subject line and preview text improvements
2. Content structure and formatting enhancements
3. Call-to-action optimization strategies
4. Segmentation and personalization opportunities
5. Send time and frequency optimization
6. A/B testing recommendations
7. Re-engagement campaign strategies
8. List hygiene and deliverability improvements

{context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

def main():
    print("Newsletter Agent initialized")
    
    agent = NewsletterAgent(use_rag=False)
    
    brand_info = "Eterna - unified trading terminal for different DEXs"
    subscriber_profile = "Crypto traders and DeFi enthusiasts interested in trading efficiency"
    newsletter_goals = "Educate subscribers about DeFi trading, showcase platform features, drive user adoption"
    
    response = agent.create_newsletter_strategy(brand_info, subscriber_profile, newsletter_goals)
    print(response)

if __name__ == "__main__":
    main()