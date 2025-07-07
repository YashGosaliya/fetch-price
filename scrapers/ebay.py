import requests
from bs4 import BeautifulSoup
import re

def search_ebay_us(query):
    """Search eBay US for products and return results."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    url = f"https://www.ebay.com/sch/i.html?_nkw={requests.utils.quote(query)}&_sacat=0"
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        results = []
        
        # Look for product containers
        product_containers = soup.select('.s-item')
        
        for container in product_containers[:10]:  # Limit to first 10 results
            try:
                # Extract product name
                title_elem = container.select_one('.s-item__title')
                if not title_elem:
                    continue
                product_name = title_elem.text.strip()
                
                # Skip "Shop on eBay" or similar non-product items
                if "Shop on eBay" in product_name or "See similar items" in product_name:
                    continue
                
                # Extract product link
                link_elem = container.select_one('.s-item__link')
                if not link_elem or not link_elem.get('href'):
                    continue
                product_link = link_elem['href']
                
                # Extract price
                price_elem = container.select_one('.s-item__price')
                if not price_elem:
                    continue
                    
                price_text = price_elem.text.strip()
                # Extract numeric price
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                if price_match:
                    price = price_match.group()
                    # Clean price
                    price = re.sub(r'[^\d.]', '', price)
                    
                    if price and float(price) > 0:
                        results.append({
                            "link": product_link,
                            "price": price,
                            "currency": "USD",
                            "productName": product_name,
                            "source": "eBay US"
                        })
                        
            except Exception as e:
                continue
                
        return results
        
    except Exception as e:
        print(f"Error scraping eBay US: {e}")
        return [] 