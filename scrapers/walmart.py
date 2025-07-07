import requests
from bs4 import BeautifulSoup
import re

def search_walmart_us(query):
    """Search Walmart US for products and return results."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    url = f"https://www.walmart.com/search/?query={requests.utils.quote(query)}"
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        results = []
        
        # Look for product containers - Walmart has different selectors
        product_containers = soup.select('[data-item-id]') or soup.select('.product-grid-container [data-item-id]')
        
        for container in product_containers[:10]:  # Limit to first 10 results
            try:
                # Extract product name
                title_elem = container.select_one('a[data-item-title] span') or container.select_one('.product-title-link span')
                if not title_elem:
                    continue
                product_name = title_elem.text.strip()
                
                # Extract product link
                link_elem = container.select_one('a[data-item-title]') or container.select_one('.product-title-link')
                if not link_elem or not link_elem.get('href'):
                    continue
                product_link = link_elem['href']
                if not product_link.startswith('http'):
                    product_link = "https://www.walmart.com" + product_link
                
                # Extract price - try multiple selectors
                price_elem = (
                    container.select_one('[data-price-type="finalPrice"] .visuallyhidden') or
                    container.select_one('.price-main .visuallyhidden') or
                    container.select_one('[data-price-type="finalPrice"]') or
                    container.select_one('.price-main')
                )
                
                if price_elem:
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
                                "source": "Walmart US"
                            })
                            
            except Exception as e:
                continue
                
        return results
        
    except Exception as e:
        print(f"Error scraping Walmart US: {e}")
        return [] 