#!/usr/bin/env python3
"""
Lightweight research example that uses fewer API calls to avoid quota limits.
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents.research_agent import ResearchAgent

def lightweight_research_example():
    """Lightweight research example to avoid quota issues."""
    print("🚀 Starting Lightweight Research Example")
    print("💡 Using gemini-1.5-flash with rate limiting")
    
    try:
        # Initialize the research agent
        agent = ResearchAgent()
        
        # Use fewer, more focused questions to reduce API calls
        topic = "Solar Energy Benefits"
        questions = [
            "What are the main environmental benefits of solar energy?",
            "What are the economic advantages of solar power?"
        ]
        
        print(f"📚 Research Topic: {topic}")
        print("🔍 Research Questions:")
        for i, q in enumerate(questions, 1):
            print(f"   {i}. {q}")
        print("-" * 60)
        
        # Conduct research
        results = agent.conduct_research(topic, questions)
        
        # Generate concise report
        report = agent.generate_report(results, topic)
        
        # Save results
        output_file = f"lightweight_solar_research.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Lightweight Research Report: {topic}\n")
            f.write("=" * 80 + "\n\n")
            f.write(report)
        
        print(f"✅ Research completed!")
        print(f"📄 Report saved to: {output_file}")
        
        # Show a preview
        print("\n📋 Report Preview:")
        print("-" * 40)
        print(report[:200] + "..." if len(report) > 200 else report)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 You may have exceeded your free tier quota.")
        print("💡 Try again in 24 hours or set up billing for higher limits.")

if __name__ == "__main__":
    lightweight_research_example()
