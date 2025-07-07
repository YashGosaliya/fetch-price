#!/usr/bin/env python3
"""
Test script for the Best Price Fetcher Tool

This script demonstrates how to use the tool with various example queries.
"""

import json
import subprocess
import sys

def test_query(country, query):
    """Test a specific query and display results."""
    print(f"\n{'='*60}")
    print(f"Testing: Country={country}, Query='{query}'")
    print(f"{'='*60}")
    
    # Prepare input JSON
    input_data = {
        "country": country,
        "query": query
    }
    
    try:
        # Run the tool
        result = subprocess.run(
            [sys.executable, "fetch_best_price.py"],
            input=json.dumps(input_data),
            text=True,
            capture_output=True,
            timeout=60  # 60 second timeout
        )
        
        if result.returncode == 0:
            try:
                results = json.loads(result.stdout)
                if isinstance(results, list) and results:
                    print(f"✓ Found {len(results)} results:")
                    for i, item in enumerate(results[:5], 1):  # Show first 5 results
                        print(f"  {i}. {item['productName'][:50]}...")
                        print(f"     Price: {item['currency']} {item['price']}")
                        print(f"     Source: {item['source']}")
                        print(f"     Link: {item['link'][:80]}...")
                        print()
                else:
                    print("✗ No results found or error occurred")
                    if result.stderr:
                        print(f"Error output: {result.stderr}")
            except json.JSONDecodeError:
                print("✗ Invalid JSON output")
                print(f"Output: {result.stdout}")
        else:
            print(f"✗ Tool failed with return code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
                
    except subprocess.TimeoutExpired:
        print("✗ Tool timed out (60 seconds)")
    except Exception as e:
        print(f"✗ Error running tool: {e}")

def main():
    """Run test queries."""
    print("Best Price Fetcher Tool - Test Suite")
    print("This will test various queries across different countries.")
    
    # Test cases
    test_cases = [
        ("US", "iPhone 15 Pro 128GB"),
        ("US", "Samsung Galaxy S24"),
        ("IN", "MacBook Air M2"),
        ("IN", "OnePlus 12"),
        ("US", "PlayStation 5"),
    ]
    
    for country, query in test_cases:
        test_query(country, query)
        print("\n" + "-"*60)
    
    print("\nTest completed!")

if __name__ == "__main__":
    main() 