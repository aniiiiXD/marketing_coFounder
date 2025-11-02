from .base_agent import BaseAgent

class ContentPlanningAgent:
    def __init__(self, use_rag=True):
        self.agent = BaseAgent(model_name="gemini-2.5-flash", use_rag=use_rag)
        self.system_prompt = """You are an expert Content Strategy Director with deep expertise in content marketing, editorial planning, and audience engagement. Your role is to:

1. CONTENT STRATEGY: Develop comprehensive content strategies aligned with business objectives, target audience needs, and brand positioning.

2. EDITORIAL PLANNING: Create detailed content calendars, publication schedules, and content distribution strategies across multiple channels.

3. AUDIENCE-CENTRIC CONTENT: Design content that resonates with specific audience segments, addresses their pain points, and guides them through the customer journey.

4. CONTENT OPTIMIZATION: Ensure content is optimized for SEO, social media engagement, and conversion goals while maintaining brand voice consistency.

5. MULTI-FORMAT PLANNING: Plan diverse content formats including blog posts, social media content, videos, infographics, whitepapers, and interactive content.

6. PERFORMANCE-DRIVEN APPROACH: Integrate content performance metrics and analytics to continuously improve content effectiveness and ROI.

Deliver strategic, actionable content plans with clear timelines, resource requirements, and success metrics. Focus on creating content that drives engagement, builds authority, and converts prospects into customers."""

    def create_content_strategy(self, brand_info, target_audience, goals):
        """Develop comprehensive content strategy"""
        
        # Get relevant context if RAG is enabled
        context = ""
        if self.agent.use_rag:
            search_query = f"content strategy planning {brand_info} {target_audience}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=5)
            if relevant_docs:
                context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Brand Information: {brand_info}

Target Audience: {target_audience}

Content Goals: {goals}

Please develop a comprehensive content strategy including:
1. Content pillars and key themes aligned with brand positioning
2. Audience persona-specific content recommendations
3. Content calendar framework with optimal posting frequency
4. Multi-channel content distribution strategy
5. Content formats and types for maximum engagement
6. SEO and keyword integration strategy
7. Content performance metrics and KPIs
8. Resource requirements and workflow recommendations

{context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def generate_content_calendar(self, timeframe, content_themes, channels):
        """Generate detailed content calendar"""
        
        context = ""
        if self.agent.use_rag:
            search_query = f"content calendar planning {content_themes} {channels}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Timeframe: {timeframe}

Content Themes: {content_themes}

Distribution Channels: {channels}

Create a detailed content calendar including:
1. Weekly/monthly content schedule with specific topics
2. Content format recommendations for each piece
3. Channel-specific adaptations and optimizations
4. Seasonal and trending topic integration
5. Content series and campaign planning
6. Resource allocation and production timelines
7. Cross-promotion and repurposing opportunities

{context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

def main():
    print("Content Planning Agent initialized")
    
    agent = ContentPlanningAgent(use_rag=False)
    
    brand_info = "Eterna - unified trading terminal for different DEXs"
    target_audience = "Crypto traders, DeFi enthusiasts, and institutional investors"
    goals = "Increase brand awareness, educate users about unified trading benefits, drive platform adoption"
    
    response = agent.create_content_strategy(brand_info, target_audience, goals)
    print(response)

if __name__ == "__main__":
    main()