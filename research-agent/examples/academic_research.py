#!/usr/bin/env python3
"""
Academic research example focusing on scholarly papers and in-depth analysis.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents.research_agent import ResearchAgent

def academic_research_example():
    """Example of academic-focused research."""
    print("🎓 Starting Academic Research Example")
    
    agent = ResearchAgent()
    
    topic = "Large Language Models in Education"
    questions = [
        "What are the most cited papers about LLMs in educational applications?",
        "How are transformer architectures being used in adaptive learning systems?",
        "What ethical concerns have been raised about AI in education?",
        "What empirical studies show the effectiveness of LLMs in improving learning outcomes?"
    ]
    
    print(f"📚 Academic Topic: {topic}")
    print("🔍 Research Questions:")
    for i, q in enumerate(questions, 1):
        print(f"   {i}. {q}")
    print("-" * 60)
    
    # Conduct research with emphasis on academic sources
    results = agent.conduct_research(topic, questions)
    
    # Generate academic-style report
    report = agent.generate_report(results, topic)
    
    output_file = f"academic_llm_education_research.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Academic Research Report: {topic}\n")
        f.write("=" * 80 + "\n\n")
        f.write(report)
    
    print(f"✅ Academic research completed!")
    print(f"📄 Report saved to: {output_file}")

if __name__ == "__main__":
    academic_research_example()
