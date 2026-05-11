"""
Amazon Affiliate Video Pipeline
Main orchestration module that coordinates scraping, script generation, voiceover, and visuals.
"""

import asyncio
from dotenv import load_dotenv
from scraper import scrape_amazon_reviews, download_product_image
from script_generator import generate_video_script
from voiceover import generate_voiceover
from visuals import fetch_visuals
from assemble_video import assemble_video
import re
import json

# Load API keys from .env file
load_dotenv()

def extract_asin(url: str) -> str:
    """Extracts the Amazon ASIN from a URL to use as a filename."""
    # Standard Amazon ASIN pattern: /dp/ or /gp/ followed by 10 alphanumeric chars
    match = re.search(r"/[dg]p/([^/?]+)", url)
    return match.group(1) if match else "unknown_product"

async def main_pipeline():
    """
    Main pipeline orchestration.
    Executes all steps: scraping → script generation → voiceover → visuals.
    """
    print("--- Amazon Affiliate Video Pipeline ---")
    url = input("Paste Amazon Product URL: ")
    
    # Extract ASIN at the start of your pipeline
    asin = extract_asin(url)

    # Step 1: Run the scraper
    raw_data = scrape_amazon_reviews.invoke({"product_url": url})

    if "Error" not in raw_data:
        parsed_data = json.loads(raw_data)
        # Step 1.5: Download product image
        product_img_path = download_product_image(parsed_data, asin)

        # Step 2: Generate the video script
        script_data = generate_video_script(raw_data, asin)
        
        # Step 3: Generate Voiceover
        await generate_voiceover(script_data)
        
        # Step 4: Fetch Visuals
        fetch_visuals(script_data)

        # 5. Assemble
        assemble_video(script_data, product_img_path)
    else:
        print(f"Pipeline failed: {raw_data}")


if __name__ == "__main__":
    asyncio.run(main_pipeline())

