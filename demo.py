#!/usr/bin/env python3
"""
Demo script to capture proof of working for the required query.
This script will run the tool and save the output as proof.
"""

import json
import subprocess
import sys
from datetime import datetime

def run_demo():
    """Run the demo and capture output."""
    print("🎯 Price Fetcher Tool - Demo")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # The required query
    query = {
        "country": "US",
        "query": "iPhone 16 Pro, 128GB"
    }
    
    print(f"Testing query: {json.dumps(query, indent=2)}")
    print("-" * 50)
    
    try:
        # Run the tool
        result = subprocess.run(
            [sys.executable, "fetch_best_price.py"],
            input=json.dumps(query),
            text=True,
            capture_output=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # Parse and display results
            results = json.loads(result.stdout)
            
            if isinstance(results, list) and results:
                print(f"✅ SUCCESS: Found {len(results)} results")
                print()
                print("📊 Results (sorted by price):")
                print("-" * 50)
                
                for i, item in enumerate(results[:5], 1):  # Show first 5 results
                    print(f"{i}. {item['productName'][:60]}...")
                    print(f"   💰 Price: {item['currency']} {item['price']}")
                    print(f"   🏪 Source: {item['source']}")
                    print(f"   🔗 Link: {item['link'][:80]}...")
                    print()
                
                # Save proof to file
                proof_data = {
                    "timestamp": datetime.now().isoformat(),
                    "query": query,
                    "total_results": len(results),
                    "results": results[:5],  # Save first 5 results
                    "status": "SUCCESS"
                }
                
                with open("proof_of_working.json", "w") as f:
                    json.dump(proof_data, f, indent=2)
                
                print("💾 Proof saved to: proof_of_working.json")
                
            else:
                print("❌ No results found")
                print(f"Error output: {result.stderr}")
                
        else:
            print(f"❌ Tool failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ Tool timed out (60 seconds)")
    except Exception as e:
        print(f"❌ Error running tool: {e}")
    
    print("=" * 50)
    print("Demo completed!")

if __name__ == "__main__":
    run_demo() 