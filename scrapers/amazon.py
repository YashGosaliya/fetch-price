import requests
from bs4 import BeautifulSoup
import re
import time

def search_amazon_us(query):
    """Search Amazon US for products and return results."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    url = f"https://www.amazon.com/s?k={requests.utils.quote(query)}"
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        results = []
        
        # Look for product containers
        product_containers = soup.select('[data-component-type="s-search-result"]')
        
        for container in product_containers[:10]:  # Limit to first 10 results
            try:
                # Extract product name
                title_elem = container.select_one('h2 a span')
                if not title_elem:
                    continue
                product_name = title_elem.text.strip()
                
                # Extract product link
                link_elem = container.select_one('h2 a')
                if not link_elem or not link_elem.get('href'):
                    continue
                product_link = "https://www.amazon.com" + link_elem['href']
                
                # Extract price
                price_elem = container.select_one('.a-price-whole')
                fraction_elem = container.select_one('.a-price-fraction')
                
                if price_elem:
                    price_whole = price_elem.text.replace(',', '')
                    price_fraction = fraction_elem.text if fraction_elem else '00'
                    price = f"{price_whole}.{price_fraction}"
                    
                    # Clean price (remove any non-numeric characters except decimal)
                    price = re.sub(r'[^\d.]', '', price)
                    
                    if price and float(price) > 0:
                        results.append({
                            "link": product_link,
                            "price": price,
                            "currency": "USD",
                            "productName": product_name,
                            "source": "Amazon US"
                        })
                        
            except Exception as e:
                continue
                
        return results
        
    except Exception as e:
        print(f"Error scraping Amazon US: {e}")
        return [] 