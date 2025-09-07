#!/usr/bin/env python3
"""
Alternative approach to test Gemini API.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_alternative_approach():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ API key not found")
        return
    
    try:
        genai.configure(api_key=api_key)
        
        # Try different model names
        model_names = [
            "gemini-pro",
            "models/gemini-pro",
            "gemini-1.0-pro",
            "models/gemini-1.0-pro"
        ]
        
        for model_name in model_names:
            try:
                print(f"🔧 Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello, are you working?")
                print(f"✅ SUCCESS with {model_name}: {response.text[:50]}...")
                return True
            except Exception as e:
                print(f"❌ Failed with {model_name}: {e}")
                continue
                
        print("🤔 No model worked. Let's check what's available...")
        
        # List all available models
        models = genai.list_models()
        print("📋 All available models:")
        for model in models:
            print(f"   - {model.name}")
            
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    test_alternative_approach()
