#!/usr/bin/env python3
"""
Basic example of using the Research Agent for general topic research.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents.research_agent import ResearchAgent

def basic_research_example():
    """Example of basic research on a general topic."""
    print("🚀 Starting Basic Research Example")
    
    try:
        # Initialize the research agent
        agent = ResearchAgent()
        
        # Define research parameters
        topic = "Renewable Energy Trends 2024"
        questions = [
            "What are the latest developments in solar energy technology?",
            "How is wind energy adoption progressing globally?",
            "What are the economic impacts of renewable energy transition?",
            "What challenges remain in renewable energy storage?"
        ]
        
        print(f"📚 Research Topic: {topic}")
        print("🔍 Research Questions:")
        for i, q in enumerate(questions, 1):
            print(f"   {i}. {q}")
        print("-" * 60)
        
        # Conduct research
        results = agent.conduct_research(topic, questions)
        
        # Generate comprehensive report
        report = agent.generate_report(results, topic)
        
        # Save results
        output_file = f"renewable_energy_research_{len(questions)}_questions.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Research Report: {topic}\n")
            f.write("=" * 80 + "\n\n")
            f.write(report)
        
        print(f"✅ Research completed!")
        print(f"📄 Report saved to: {output_file}")
        print(f"📊 Report length: {len(report)} characters")
        
        # Show a preview
        print("\n📋 Report Preview:")
        print("-" * 40)
        print(report[:300] + "..." if len(report) > 300 else report)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure your Gemini API key is valid and has access to the models")

if __name__ == "__main__":
    basic_research_example()
