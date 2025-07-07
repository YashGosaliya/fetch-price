#!/usr/bin/env python3
"""
Best Price Fetcher Tool

A tool that compares product prices across multiple e-commerce websites
for a given country and query.

Usage:
    echo '{"country": "US", "query":"iPhone 16 Pro, 128GB"}' | python fetch_best_price.py
"""

import sys
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrapers import get_scrapers_for_country

def fetch_best_price(input_json):
    """
    Fetch the best prices for a product across multiple websites.
    
    Args:
        input_json (dict): Dictionary containing 'country' and 'query' keys
        
    Returns:
        list: Sorted list of product results with price, link, currency, and product name
    """
    country = input_json.get("country", "").upper()
    query = input_json.get("query", "")
    
    if not country or not query:
        return {"error": "Both 'country' and 'query' are required"}
    
    # Get scrapers for the specified country
    scrapers = get_scrapers_for_country(country)
    
    if not scrapers:
        return {"error": f"No scrapers available for country: {country}"}
    
    all_results = []
    
    # Use ThreadPoolExecutor to run scrapers concurrently
    with ThreadPoolExecutor(max_workers=len(scrapers)) as executor:
        # Submit all scraper tasks
        future_to_scraper = {
            executor.submit(scraper, query): scraper.__name__ 
            for scraper in scrapers
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_scraper):
            scraper_name = future_to_scraper[future]
            try:
                results = future.result()
                if results:
                    all_results.extend(results)
                    print(f"✓ {scraper_name}: Found {len(results)} results", file=sys.stderr)
                else:
                    print(f"✗ {scraper_name}: No results found", file=sys.stderr)
            except Exception as e:
                print(f"✗ {scraper_name}: Error - {e}", file=sys.stderr)
    
    # Filter out results without valid prices and sort by price
    valid_results = []
    for result in all_results:
        try:
            price = float(result.get("price", "0"))
            if price > 0:
                valid_results.append(result)
        except (ValueError, TypeError):
            continue
    
    # Sort by price (ascending)
    valid_results.sort(key=lambda x: float(x["price"]))
    
    return valid_results

def main():
    """Main function to handle command line input/output."""
    try:
        # Read JSON input from stdin
        input_data = sys.stdin.read().strip()
        if not input_data:
            print(json.dumps({"error": "No input provided"}, indent=2))
            return
        
        # Parse JSON input
        try:
            input_json = json.loads(input_data)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid JSON input: {e}"}, indent=2))
            return
        
        # Fetch results
        results = fetch_best_price(input_json)
        
        # Output results as JSON
        print(json.dumps(results, indent=2))
        
    except KeyboardInterrupt:
        print(json.dumps({"error": "Operation cancelled by user"}, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {e}"}, indent=2))

if __name__ == "__main__":
    main() 