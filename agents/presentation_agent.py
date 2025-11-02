from .base_agent import BaseAgent

class PresentationAgent:
    def __init__(self, use_rag=True):
        self.agent = BaseAgent(model_name="gemini-2.5-flash", use_rag=use_rag)
        self.system_prompt = """You are an expert Presentation Analyst specializing in converting visual presentation slides into comprehensive text explanations. Your role is to:

1. SLIDE INTERPRETATION: Analyze presentation slides and transform visual elements, charts, diagrams, and bullet points into clear, detailed text explanations.

2. NARRATIVE CONSTRUCTION: Create coherent, flowing narratives that explain the logical progression and connections between slides, maintaining the presentation's intended story arc.

3. VISUAL ELEMENT DESCRIPTION: Accurately describe charts, graphs, images, diagrams, and other visual elements in text format, explaining their significance and key insights.

4. CONTENT ENHANCEMENT: Expand on abbreviated slide content, providing context, explanations, and deeper insights that speakers would typically provide verbally.

5. STRUCTURE PRESERVATION: Maintain the original presentation structure while making it accessible in text-only format, including slide transitions and logical flow.

6. AUDIENCE ADAPTATION: Tailor explanations to match the intended audience level, ensuring technical concepts are appropriately explained without losing accuracy.

Generate comprehensive text explanations that capture both the explicit content and implicit meaning of presentation slides. Focus on creating standalone text that fully conveys the presentation's message without requiring visual reference."""

    def explain_presentation(self, slide_content, presentation_context=None, target_audience=None):
        """Convert presentation slides into comprehensive text explanation"""
        
        # Get relevant context if RAG is enabled
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"presentation explanation {presentation_context if presentation_context else 'slides'}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=5)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context from Knowledge Base:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Slide Content: {slide_content}

{f"Presentation Context: {presentation_context}" if presentation_context else ""}

{f"Target Audience: {target_audience}" if target_audience else ""}

Please provide a comprehensive text explanation of this presentation including:

1. PRESENTATION OVERVIEW
   - Main theme and objectives
   - Key messages and takeaways
   - Overall structure and flow

2. SLIDE-BY-SLIDE EXPLANATION
   - Detailed explanation of each slide's content
   - Description of visual elements (charts, graphs, images)
   - Context and significance of each point
   - Connections between slides

3. VISUAL ELEMENTS DESCRIPTION
   - Charts and graphs: data interpretation and trends
   - Diagrams: process flows and relationships
   - Images: relevance and symbolic meaning

4. KEY INSIGHTS AND ANALYSIS
   - Critical findings and conclusions
   - Supporting evidence and data points
   - Implications and recommendations

5. NARRATIVE FLOW
   - How slides build upon each other
   - Logical progression of arguments
   - Transition explanations between sections

Format as clear, readable text that stands alone without needing visual reference.

{rag_context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def analyze_slide_structure(self, slide_data, analysis_focus="comprehensive"):
        """Analyze and explain the structure and organization of slides"""
        
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"slide structure analysis presentation organization"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Slide Data: {slide_data}

Analysis Focus: {analysis_focus}

Provide a structural analysis including:

1. PRESENTATION ARCHITECTURE
   - Overall organization and hierarchy
   - Section divisions and themes
   - Information flow and sequencing

2. CONTENT CATEGORIZATION
   - Types of content per slide (data, concepts, conclusions)
   - Supporting vs. primary information
   - Visual vs. textual content balance

3. LOGICAL PROGRESSION
   - How arguments build throughout the presentation
   - Evidence presentation and conclusion drawing
   - Transition logic between major sections

4. DESIGN PATTERNS
   - Consistent formatting and layout choices
   - Visual hierarchy and emphasis techniques
   - Information density and readability

5. EFFECTIVENESS ASSESSMENT
   - Clarity of message delivery
   - Audience engagement potential
   - Areas for improvement

{rag_context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def create_presentation(self, topic, audience="general", context=None, slides_count=10):
        """Create a new presentation on a given topic"""
        
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"presentation creation {topic} {audience}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=5)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context from Knowledge Base:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Topic: {topic}
Target Audience: {audience}
Requested Slides: {slides_count}
{f"Additional Context: {context}" if context else ""}

Create a comprehensive presentation including:

1. PRESENTATION OUTLINE
   - Title slide
   - Agenda/Overview
   - Main content slides (with specific titles)
   - Conclusion/Next steps
   - Q&A slide

2. DETAILED SLIDE CONTENT
   For each slide provide:
   - Slide title
   - Key bullet points (3-5 per slide)
   - Supporting details and explanations
   - Suggested visuals or charts
   - Speaker notes

3. VISUAL RECOMMENDATIONS
   - Chart types for data presentation
   - Image suggestions for concepts
   - Layout recommendations
   - Color scheme and design notes

4. PRESENTATION FLOW
   - Logical progression between slides
   - Transition suggestions
   - Timing recommendations
   - Audience engagement points

5. SUPPORTING MATERIALS
   - Key statistics and data points
   - References and sources
   - Appendix slides for detailed information

Format as a complete presentation script with clear slide divisions.

{rag_context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def enhance_presentation(self, existing_content, enhancement_type="comprehensive"):
        """Enhance an existing presentation with additional content and improvements"""
        
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"presentation enhancement improvement {enhancement_type}"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=4)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Existing Presentation Content: {existing_content}

Enhancement Type: {enhancement_type}

Please enhance this presentation by:

1. CONTENT IMPROVEMENTS
   - Add missing key points
   - Strengthen weak arguments
   - Include relevant data and statistics
   - Improve clarity and flow

2. STRUCTURE OPTIMIZATION
   - Reorganize for better logical flow
   - Add or remove slides as needed
   - Improve transitions between sections
   - Balance content distribution

3. AUDIENCE ENGAGEMENT
   - Add interactive elements
   - Include compelling stories or examples
   - Suggest audience participation points
   - Improve opening and closing impact

4. VISUAL ENHANCEMENTS
   - Recommend charts and graphics
   - Suggest layout improvements
   - Add visual storytelling elements
   - Improve slide design consistency

5. DELIVERY IMPROVEMENTS
   - Add speaker notes and cues
   - Suggest timing and pacing
   - Include backup slides for Q&A
   - Recommend rehearsal focus areas

{rag_context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def extract_key_insights(self, presentation_content):
        """Extract and summarize key insights from presentation content"""
        
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"presentation insights analysis key points"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Presentation Content: {presentation_content}

Extract and analyze key insights including:

1. MAIN MESSAGES
   - Primary thesis or argument
   - Supporting key points
   - Core value propositions
   - Critical conclusions

2. DATA INSIGHTS
   - Key statistics and metrics
   - Trends and patterns
   - Comparative analysis
   - Performance indicators

3. STRATEGIC IMPLICATIONS
   - Business impact
   - Recommended actions
   - Risk factors
   - Opportunities identified

4. AUDIENCE TAKEAWAYS
   - What audience should remember
   - Action items for audience
   - Follow-up requirements
   - Success metrics

5. PRESENTATION EFFECTIVENESS
   - Strength of arguments
   - Quality of supporting evidence
   - Clarity of communication
   - Persuasiveness assessment

{rag_context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def convert_to_executive_summary(self, presentation_content):
        """Convert presentation content into a concise executive summary"""
        
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"executive summary presentation conversion"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Presentation Content: {presentation_content}

Create a comprehensive executive summary including:

1. EXECUTIVE OVERVIEW (2-3 paragraphs)
   - Main purpose and objectives
   - Key findings and conclusions
   - Primary recommendations

2. KEY HIGHLIGHTS
   - Most important data points
   - Critical insights
   - Major opportunities or risks
   - Success metrics

3. STRATEGIC RECOMMENDATIONS
   - Priority actions
   - Resource requirements
   - Timeline considerations
   - Expected outcomes

4. SUPPORTING EVIDENCE
   - Key statistics
   - Market data
   - Performance metrics
   - Comparative analysis

5. NEXT STEPS
   - Immediate actions required
   - Long-term strategic moves
   - Success measurement
   - Follow-up timeline

Format as a professional executive summary suitable for senior leadership review.

{rag_context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )

    def generate_speaker_notes(self, slide_content, presentation_duration=30):
        """Generate detailed speaker notes for presentation delivery"""
        
        rag_context = ""
        if self.agent.use_rag:
            search_query = f"speaker notes presentation delivery"
            relevant_docs = self.agent.get_relevant_context(search_query, n_results=3)
            if relevant_docs:
                rag_context = f"\n\nRelevant Context:\n{chr(10).join(relevant_docs)}"

        user_prompt = f"""Slide Content: {slide_content}
Presentation Duration: {presentation_duration} minutes

Generate comprehensive speaker notes including:

1. SLIDE-BY-SLIDE NOTES
   - Key talking points for each slide
   - Transition phrases between slides
   - Emphasis points and delivery cues
   - Timing recommendations per slide

2. DELIVERY GUIDANCE
   - Voice modulation suggestions
   - Gesture and movement cues
   - Audience interaction points
   - Pause and emphasis timing

3. TECHNICAL DETAILS
   - Equipment setup requirements
   - Backup plan considerations
   - Slide advancement cues
   - Technical troubleshooting tips

4. AUDIENCE ENGAGEMENT
   - Question prompts for audience
   - Interactive elements timing
   - Audience participation cues
   - Energy management techniques

5. CONTINGENCY PLANNING
   - Time adjustment strategies
   - Slide skipping options
   - Q&A preparation
   - Difficult question handling

{rag_context}"""

        return self.agent.generate_response(
            prompt=user_prompt,
            system_instruction=self.system_prompt
        )