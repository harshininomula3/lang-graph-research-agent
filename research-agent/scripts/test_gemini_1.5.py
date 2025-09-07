#!/usr/bin/env python3
"""
Test script for Gemini 1.5 Pro model.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def test_gemini_1_5():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ API key not found")
        return
    
    try:
        # Test with the available model
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.5-pro",
            google_api_key=api_key,
            temperature=0.3
        )
        
        response = llm.invoke("Hello! Say 'Gemini 1.5 Pro is working!'")
        print("✅ SUCCESS! Gemini 1.5 Pro is working!")
        print(f"🤖 Response: {response.content}")
        
    except Exception as e:
        print(f"❌ Error with Gemini 1.5 Pro: {e}")
        
        # Try alternative available models
        alternative_models = [
            "models/gemini-1.5-flash",
            "models/gemini-2.0-flash",
            "models/gemini-2.5-flash"
        ]
        
        for model in alternative_models:
            try:
                print(f"🔧 Trying alternative model: {model}")
                llm = ChatGoogleGenerativeAI(
                    model=model,
                    google_api_key=api_key,
                    temperature=0.3
                )
                response = llm.invoke(f"Testing {model}")
                print(f"✅ SUCCESS with {model}: {response.content[:50]}...")
                break
            except Exception as alt_e:
                print(f"❌ Failed with {model}: {alt_e}")
                continue

if __name__ == "__main__":
    test_gemini_1_5()
