#!/usr/bin/env python3
"""
Custom research example that demonstrates how to extend the basic functionality.
"""

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents.research_agent import ResearchAgent

def custom_research_with_savepoints():
    """Example with intermediate save points and custom processing."""
    print("🛠️ Starting Custom Research Example")
    
    agent = ResearchAgent()
    
    topic = "Quantum Computing Applications"
    questions = [
        "What are the current practical applications of quantum computing?",
        "Which companies are leading in quantum computing development?",
        "What are the main technical challenges in quantum computing?",
        "How might quantum computing impact cryptography and cybersecurity?"
    ]
    
    print(f"🔬 Research Topic: {topic}")
    
    # Research step by step with save points
    all_results = {}
    
    for i, question in enumerate(questions, 1):
        print(f"\n🔍 Researching question {i}/{len(questions)}: {question}")
        
        results = agent.conduct_research(topic, [question])
        all_results[question] = results[question]
        
        # Save intermediate results
        with open(f"intermediate_results_q{i}.json", "w", encoding="utf-8") as f:
            json.dump({question: results[question]}, f, indent=2)
        
        print(f"   ✅ Question {i} completed and saved")
    
    # Generate final report
    print("\n📊 Generating comprehensive report...")
    report = agent.generate_report(all_results, topic)
    
    # Save final report
    output_file = "quantum_computing_comprehensive_report.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Comprehensive Research Report: {topic}\n")
        f.write("=" * 80 + "\n\n")
        f.write(report)
    
    print(f"✅ All research completed!")
    print(f"📄 Final report saved to: {output_file}")
    print(f"📁 Intermediate results saved for each question")

if __name__ == "__main__":
    custom_research_with_savepoints()
