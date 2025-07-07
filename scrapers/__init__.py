from .amazon import search_amazon_us
from .ebay import search_ebay_us
from .walmart import search_walmart_us
from .flipkart import search_flipkart_in
from .amazon_in import search_amazon_in

def get_scrapers_for_country(country):
    """Return list of scraper functions for a given country."""
    country = country.upper()
    scrapers_map = {
        "US": [search_amazon_us, search_ebay_us, search_walmart_us],
        "IN": [search_flipkart_in, search_amazon_in],
        # Add more countries as needed
    }
    return scrapers_map.get(country, []) 