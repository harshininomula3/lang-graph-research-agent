#!/bin/bash
# Navigation helper script for research agent project

echo "🧭 Research Agent Project Navigation"
echo "==================================="

# Check if we're in the right directory
CURRENT_DIR=$(pwd)
if [[ $CURRENT_DIR == *"/research-agent" ]]; then
    echo "✅ You're in the correct directory: research-agent/"
else
    echo "❌ You're in: $CURRENT_DIR"
    echo "💡 You need to be in: ~/Desktop/lang_graph_research_asistant/research-agent/"
    echo ""
    read -p "Would you like to navigate there now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd ~/Desktop/lang_graph_research_asistant/research-agent/
        echo "✅ Navigated to: $(pwd)"
    else
        echo "⚠️  Staying in current directory"
    fi
fi

echo ""
echo "📁 Current directory contents:"
ls -la

echo ""
echo "🚀 Available commands:"
echo "  python examples/lightweight_research.py    # Run basic research"
echo "  python examples/comprehensive_research.py  # Run advanced research"
echo "  python scripts/batch_research.py           # Run batch research"
echo "  python scripts/view_report.py              # View research reports"
echo "  python scripts/celebrate_success.py        # Celebrate success! 🎉"
