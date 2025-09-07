#!/usr/bin/env python3
"""
List available Gemini models to see what's working.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def list_available_models():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ Please add your Gemini API key to .env file")
        return
    
    try:
        genai.configure(api_key=api_key)
        
        print("🔍 Listing available models...")
        models = genai.list_models()
        
        print("✅ Available models:")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"📦 {model.name} - {model.description}")
                
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        print("\n💡 Make sure:")
        print("1. Gemini API is enabled: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
        print("2. Your API key has proper permissions")
        print("3. You're using the correct project")

if __name__ == "__main__":
    list_available_models()
