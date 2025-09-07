import argparse
import json
from datetime import datetime
from src.agents.research_agent import ResearchAgent

def main():
    parser = argparse.ArgumentParser(description="Research Agent")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--questions", nargs="+", required=True, help="Research questions")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    # Initialize research agent
    agent = ResearchAgent()
    
    print(f"Starting research on: {args.topic}")
    print(f"Research questions: {args.questions}")
    print("-" * 50)
    
    # Conduct research
    results = agent.conduct_research(args.topic, args.questions)
    
    # Generate report
    report = agent.generate_report(results, args.topic)
    
    # Save results
    output_file = args.output or f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Research Report: {args.topic}\n")
        f.write(f"Generated on: {datetime.now()}\n")
        f.write("=" * 80 + "\n\n")
        f.write(report)
    
    print(f"\nResearch completed! Report saved to: {output_file}")
    print("\nSummary:")
    print("-" * 50)
    print(report[:500] + "..." if len(report) > 500 else report)

if __name__ == "__main__":
    main()
