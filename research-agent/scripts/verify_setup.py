#!/usr/bin/env python3
"""
Script to verify that the research agent setup is working correctly.
"""

import sys
import os
from dotenv import load_dotenv

def check_imports():
    """Check if all required imports work"""
    print("🔍 Checking imports...")
    
    imports_to_check = [
        ("langchain", "langchain"),
        ("langchain_community", "langchain_community"),
        ("langchain_google_genai", "langchain_google_genai"),
        ("google.generativeai", "google.generativeai"),
        ("arxiv", "arxiv"),
        ("bs4", "beautifulsoup4"),
    ]
    
    all_imports_ok = True
    for import_name, package_name in imports_to_check:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} (missing)")
            all_imports_ok = False
    
    return all_imports_ok

def check_env_vars():
    """Check if environment variables are set"""
    print("\n🔍 Checking environment variables...")
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        print("✅ GEMINI_API_KEY is set")
        return True
    else:
        print("❌ GEMINI_API_KEY not set or still using placeholder")
        return False

def check_project_structure():
    """Check if project files exist"""
    print("\n🔍 Checking project structure...")
    
    required_files = [
        "src/agents/research_agent.py",
        "src/tools/web_search.py",
        "src/utils/config.py",
        "src/utils/prompts.py",
        "examples/basic_research.py",
        ".env",
        "requirements.txt"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            all_files_exist = False
    
    return all_files_exist

def main():
    print("🧪 Research Agent Setup Verification")
    print("=" * 50)
    
    imports_ok = check_imports()
    env_ok = check_env_vars()
    structure_ok = check_project_structure()
    
    print("\n" + "=" * 50)
    if imports_ok and env_ok and structure_ok:
        print("🎉 Setup is complete and ready to use!")
        print("\nYou can now run: python examples/basic_research.py")
    else:
        print("❌ Setup issues detected. Please fix the above problems.")
        
        if not imports_ok:
            print("\n💡 Try: pip install -r requirements.txt")
        if not env_ok:
            print("💡 Edit .env file and add your Gemini API key")
        if not structure_ok:
            print("�� Check that all project files are in place")

if __name__ == "__main__":
    main()
