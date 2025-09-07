#!/usr/bin/env python3
"""
Test script with rate limiting to avoid quota issues.
"""

import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def test_with_delay():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ API key not found")
        return
    
    try:
        # Use gemini-1.5-flash which has better free tier limits
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.3
        )
        
        print("🧪 Testing Gemini 1.5 Flash with rate limiting...")
        
        # Test with a simple prompt first
        response = llm.invoke("Hello! Say 'Gemini 1.5 Flash is working!' in a short sentence.")
        print(f"✅ Initial test: {response.content}")
        
        # Wait a bit before next test
        time.sleep(3)
        
        # Test with a research-style prompt
        research_prompt = "What are the main benefits of solar energy? Keep response brief."
        response2 = llm.invoke(research_prompt)
        print(f"✅ Research test: {response2.content[:100]}...")
        
        print("🎉 All tests passed! The model is working correctly.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 You may need to wait for your quota to reset (usually 24 hours)")
        print("💡 Or consider setting up billing for higher limits")

if __name__ == "__main__":
    test_with_delay()
