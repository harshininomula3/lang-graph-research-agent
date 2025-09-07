#!/bin/bash
echo "🚀 Starting Research Agent in Production Mode..."
cd app
gunicorn -w 4 -b 0.0.0.0:5000 app:app
