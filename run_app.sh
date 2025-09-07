#!/bin/bash
echo "🚀 Starting Research Agent Web App..."
cd app
export FLASK_APP=app.py
export FLASK_ENV=development
python -m flask run --host=0.0.0.0 --port=5000
