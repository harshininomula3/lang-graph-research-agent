from flask import Flask, render_template, request, jsonify
import sys
import os
import json
from datetime import datetime
import threading
import time

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents.research_agent import ResearchAgent

app = Flask(__name__)

# In-memory storage for research results (in production, use a database)
research_results = {}
research_queue = []

class ResearchThread(threading.Thread):
    def __init__(self, research_id, topic, questions):
        threading.Thread.__init__(self)
        self.research_id = research_id
        self.topic = topic
        self.questions = questions
    
    def run(self):
        try:
            agent = ResearchAgent()
            results = agent.conduct_research(self.topic, self.questions)
            report = agent.generate_report(results, self.topic)
            
            # Save results
            research_results[self.research_id] = {
                'status': 'completed',
                'topic': self.topic,
                'questions': self.questions,
                'results': results,
                'report': report,
                'completed_at': datetime.now().isoformat()
            }
        except Exception as e:
            research_results[self.research_id] = {
                'status': 'error',
                'error': str(e),
                'completed_at': datetime.now().isoformat()
            }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/research', methods=['POST'])
def start_research():
    data = request.json
    topic = data.get('topic', '').strip()
    questions = [q.strip() for q in data.get('questions', []) if q.strip()]
    
    if not topic or not questions:
        return jsonify({'error': 'Topic and questions are required'}), 400
    
    # Generate unique research ID
    research_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Start research in background thread
    research_thread = ResearchThread(research_id, topic, questions)
    research_thread.start()
    
    # Store initial status
    research_results[research_id] = {
        'status': 'processing',
        'topic': topic,
        'questions': questions,
        'started_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'research_id': research_id,
        'status': 'started',
        'message': 'Research started successfully'
    })

@app.route('/api/research/<research_id>', methods=['GET'])
def get_research_status(research_id):
    if research_id not in research_results:
        return jsonify({'error': 'Research not found'}), 404
    
    result = research_results[research_id]
    return jsonify(result)

@app.route('/api/research/<research_id>/report', methods=['GET'])
def download_report(research_id):
    if research_id not in research_results:
        return jsonify({'error': 'Research not found'}), 404
    
    result = research_results[research_id]
    if result['status'] != 'completed':
        return jsonify({'error': 'Research not completed yet'}), 400
    
    return jsonify({
        'report': result['report'],
        'topic': result['topic']
    })

@app.route('/api/history', methods=['GET'])
def get_research_history():
    # Return recent research projects (last 10)
    history = []
    for research_id, research in list(research_results.items())[-10:]:
        history.append({
            'id': research_id,
            'topic': research.get('topic', ''),
            'status': research.get('status', ''),
            'started_at': research.get('started_at', ''),
            'completed_at': research.get('completed_at', '')
        })
    
    return jsonify({'history': history})

import sys

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=True, port=port)
