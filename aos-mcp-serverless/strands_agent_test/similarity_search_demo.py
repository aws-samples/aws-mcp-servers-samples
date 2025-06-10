#!/usr/bin/env python3
"""
Demonstration script for the similarity_search tool.

This script shows how to use the new similarity_search tool that retrieves data
from external knowledge bases via MCP API endpoints.
"""

from strands import Agent
import logging
import os

# Configure logging to see detailed information
logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

def main():
    """Demonstrate the similarity_search tool functionality."""
    
    # Create agent with the similarity_search tool
    agent = Agent(tools=['similarity_search.py'])

    # cn
    API_ENDPOINT = os.getenv("API_ENDPOINT", "")
    AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
    
    print("🔍 Similarity Search Tool Demo")
    print("=" * 50)
    
    # Test Case 1: Basic search
    print("\n📋 Test Case 1: Basic similarity search")
    print("-" * 30)
    
    try:
        results = agent.tool.similarity_search(
            text="machine learning algorithms",
            api_endpoint=API_ENDPOINT,
            auth_token=AUTH_TOKEN
        )
        print("✅ Basic search completed:")
        print(results)
    except Exception as e:
        print(f"❌ Basic search failed: {e}")
    
    # Test Case 2: Search with score threshold
    print("\n📋 Test Case 2: Search with score threshold")
    print("-" * 30)
    
    try:
        results = agent.tool.similarity_search(
            text="厄尔尼诺监测系统",
            k=5,
            score=0.5,
            api_endpoint=API_ENDPOINT,
            auth_token=AUTH_TOKEN
        )
        print("✅ Filtered search completed:")
        print(results)
    except Exception as e:
        print(f"❌ Filtered search failed: {e}")
    
    # Test Case 3: Limited results
    print("\n📋 Test Case 3: Limited results search")
    print("-" * 30)
    
    try:
        results = agent.tool.similarity_search(
            text="artificial intelligence best practices",
            k=3,
            score=0.0,
            api_endpoint=API_ENDPOINT,
            auth_token=AUTH_TOKEN
        )
        print("✅ Limited search completed:")
        print(results)
    except Exception as e:
        print(f"❌ Limited search failed: {e}")
    
    # Test Case 4: High score threshold (might return no results)
    print("\n📋 Test Case 4: High score threshold")
    print("-" * 30)
    
    try:
        results = agent.tool.similarity_search(
            text="hello world",
            k=5,
            score=1.9,
            api_endpoint=API_ENDPOINT,
            auth_token=AUTH_TOKEN
        )
        print("✅ High threshold search completed:")
        print(results)
    except Exception as e:
        print(f"❌ High threshold search failed: {e}")
    
    print("\n🎉 Similarity Search Tool Demo completed!")

if __name__ == "__main__":
    main()
