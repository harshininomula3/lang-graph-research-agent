#!/usr/bin/env python3
"""
Quick test to verify Gemini API is working.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def main():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ Please add your Gemini API key to .env file")
        print("💡 Get it from: https://aistudio.google.com/app/apikey")
        return
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with a simple prompt
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello! Say 'Research Agent is working!' if you can hear me.")
        
        print("✅ SUCCESS! Gemini API is working!")
        print("�� Response:", response.text)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("This might be because:")
        print("1. API key is incorrect")
        print("2. Gemini API not enabled in your Google Cloud project")
        print("3. Billing not set up (though free tier should work)")
        print("\n💡 Check: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")

if __name__ == "__main__":
    main()
