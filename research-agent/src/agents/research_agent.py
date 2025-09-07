from langchain.agents import AgentType, initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool, StructuredTool
from langchain.memory import ConversationBufferMemory
from langchain.agents import tool
from typing import List, Dict
import json
import time

from src.tools.web_search import WebSearchTool
from src.utils.config import Config
from src.utils.prompts import RESEARCH_AGENT_PROMPT, SUMMARY_PROMPT

class ResearchAgent:
    def __init__(self):
        Config.validate_config()
        
        # Use gemini-1.5-flash which has higher free tier limits
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.5-flash",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.3
        )
        
        self.web_search_tool = WebSearchTool()
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
        self.tools = self._setup_tools()
        self.agent = self._initialize_agent()
    
    def _setup_tools(self) -> List[Tool]:
        """Setup tools for the research agent"""
        
        @tool
        def web_search(query: str) -> str:
            """Search the web for information. Input should be a search query."""
            results = self.web_search_tool.search_web(query)
            return json.dumps(results, indent=2)
        
        @tool
        def academic_search(query: str) -> str:
            """Search academic sources for research papers. Input should be a research topic."""
            results = self.web_search_tool.search_academic(query)
            return json.dumps(results, indent=2)
        
        # Use StructuredTool for the summarize_research function
        def summarize_research(topic: str, findings: str) -> str:
            """Summarize research findings. Input should be topic and findings."""
            prompt = SUMMARY_PROMPT.format(topic=topic, findings=findings)
            return self.llm.invoke(prompt).content
        
        # Create a StructuredTool that accepts multiple arguments
        summarize_tool = StructuredTool.from_function(
            func=summarize_research,
            name="ResearchSummarizer",
            description="Summarize research findings into comprehensive reports.",
        )
        
        return [
            Tool.from_function(
                func=web_search,
                name="WebSearch",
                description="Search the web for current information"
            ),
            Tool.from_function(
                func=academic_search,
                name="AcademicSearch",
                description="Search academic sources for research papers"
            ),
            summarize_tool
        ]
    
    def _initialize_agent(self):
        """Initialize the research agent"""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def conduct_research(self, topic: str, research_questions: List[str]) -> Dict:
        """Conduct comprehensive research on a topic with rate limiting"""
        results = {}
        
        for i, question in enumerate(research_questions):
            prompt = RESEARCH_AGENT_PROMPT.format(topic=topic, query=question)
            
            try:
                print(f"🔍 Researching question {i+1}/{len(research_questions)}: {question}")
                response = self.agent.invoke({"input": prompt})
                results[question] = response["output"]
                
                # Add delay between requests to avoid rate limiting
                if i < len(research_questions) - 1:
                    print("⏳ Waiting 5 seconds to avoid rate limits...")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"❌ Error researching {question}: {e}")
                results[question] = f"Research failed: {str(e)}"
                
                # If it's a rate limit error, wait longer
                if "429" in str(e) or "quota" in str(e).lower():
                    print("🚫 Rate limit hit. Waiting 30 seconds...")
                    time.sleep(30)
        
        return results
    
    def generate_report(self, research_results: Dict, topic: str) -> str:
        """Generate a comprehensive research report"""
        findings_str = json.dumps(research_results, indent=2)
        
        report_prompt = f"""
        Generate a comprehensive research report on the topic: {topic}
        
        Research Findings:
        {findings_str}
        
        Please structure the report with:
        1. Executive Summary
        2. Key Findings
        3. Methodology
        4. Analysis
        5. Conclusions
        6. Recommendations
        7. References
        
        Make the report professional and well-structured.
        Be concise but comprehensive.
        """
        
        return self.llm.invoke(report_prompt).content
