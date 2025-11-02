from .base_agent import BaseAgent

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

    def generate_newsletter(self, context_info, news_sources, brand_info=None, target_audience=None):
        """Generate complete newsletter based on context and news"""
        
        # Get relevant context if RAG is enabled
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"newsletter content {context_info} news"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=5)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context from Knowledge Base:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Context Information: {context_info}

News Sources and Updates: {news_sources}

{f"Brand Information: {brand_info}" if brand_info else ""}

{f"Target Audience: {target_audience}" if target_audience else ""}

Generate a complete newsletter including:

1. SUBJECT LINE OPTIONS (3-5 compelling variations)
2. NEWSLETTER HEADER with engaging opening
3. TOP NEWS HIGHLIGHTS (3-4 key stories with brief summaries)
4. MAIN FEATURE STORY (detailed analysis of the most important news)
5. INDUSTRY INSIGHTS section (trends and implications)
6. QUICK BITES (5-7 shorter news items with one-line summaries)
7. WHAT TO WATCH (upcoming events, dates, or developments)
8. CLOSING THOUGHTS with call-to-action

Format the newsletter with clear sections, engaging headlines, and smooth transitions. Make it informative yet easy to scan and read.

{rag_context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def create_news_summary(self, news_articles, focus_area=None):
        """Create a focused news summary from multiple articles"""
        
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"news summary {focus_area if focus_area else 'general'}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""News Articles: {news_articles}

{f"Focus Area: {focus_area}" if focus_area else ""}

Create a comprehensive news summary including:
1. EXECUTIVE SUMMARY (2-3 sentences capturing the main themes)
2. KEY DEVELOPMENTS (5-7 most important news items with brief explanations)
3. TREND ANALYSIS (what patterns or trends emerge from these stories)
4. IMPACT ASSESSMENT (how these developments might affect readers)
5. LOOKING AHEAD (what to watch for next)

Keep the summary engaging, informative, and actionable for newsletter readers.

{rag_context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def generate_themed_newsletter(self, theme, context_data, news_data):
        """Generate a newsletter focused on a specific theme"""
        
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"themed newsletter {theme} content"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Newsletter Theme: {theme}

Context Data: {context_data}

News Data: {news_data}

Generate a themed newsletter including:
1. THEME-FOCUSED SUBJECT LINES (3 options)
2. THEMATIC INTRODUCTION explaining the focus
3. CURATED NEWS SELECTION (stories that fit the theme)
4. DEEP DIVE ANALYSIS on the theme's implications
5. EXPERT PERSPECTIVES or quotes related to the theme
6. ACTIONABLE TAKEAWAYS for readers
7. RELATED RESOURCES or further reading
8. THEME-APPROPRIATE CALL-TO-ACTION

Ensure all content ties back to the central theme while remaining informative and engaging.

{rag_context}"""

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