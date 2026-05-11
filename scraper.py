"""
Amazon Reviews Scraper Module
Handles scraping Amazon product reviews with local caching.
"""

import os
import json
import re
from pathlib import Path
from apify_client import ApifyClient
from langchain.tools import tool
import requests
from utils.json_utils import beautify_json_files

# Create a cache directory if it doesn't exist
CACHE_DIR = Path("scraper_cache")
CACHE_DIR.mkdir(exist_ok=True)


def extract_asin(url: str) -> str:
    """Extracts the Amazon ASIN from a URL to use as a filename."""
    match = re.search(r"/[dg]p/([^/?]+)", url)
    return match.group(1) if match else "unknown_product"

def download_product_image(scraped_data, asin):
    # Placeholder: Product image download not implemented yet
    # Assuming Apify reviews don't include mainImage
    # TODO: Implement product image scraping from Amazon product page
    print(f"Product image download for {asin} not implemented.")
    return None

@tool
def scrape_amazon_reviews(product_url: str) -> str:
    """Scrapes Amazon reviews with local caching."""
    asin = extract_asin(product_url)
    cache_path = CACHE_DIR / f"{asin}.json"

    # 1. Check if we already have this data locally
    if cache_path.exists():
        print(f"\n[Cache Hit] Loading reviews for {asin} from local storage...")
        return cache_path.read_text(encoding='utf-8')

    # 2. If not in cache, proceed to scrape
    print(f"\n[Cache Miss] Scraper triggered for: {product_url}")
    
    apify_token = os.getenv("APIFY_API_TOKEN")
    client = ApifyClient(apify_token)

    run_input = {
        "productUrls": [{"url": product_url}],
        "filterByRatings": ["allStars"],
        "maxReviews": 15,
        "sort": "helpful"
    }

    try:
        print("Requesting data from Apify...")
        run = client.actor("junglee/amazon-reviews-scraper").call(run_input=run_input)
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
        
        # 3. Save to cache for next time
        json_data = json.dumps(dataset_items, indent=4)
        cache_path.write_text(json_data, encoding='utf-8')
        print(f"Data saved to {cache_path}")
        
        # Ensure the JSON is beautified (redundant but ensures consistency)
        beautify_json_files(str(CACHE_DIR))
        
        return json_data
    except Exception as e:
        return f"Error during scraping: {str(e)}"
