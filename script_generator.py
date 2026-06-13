"""
Video Script Generator Module
Generates video scripts from scraped Amazon reviews using LLM and AIDA framework.
"""

import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from pathlib import Path
from utils.json_utils import beautify_json_files

def generate_video_script(scraped_json: str, asin: str) -> dict:

    """
    Generates a structured video script from Amazon reviews using AIDA framework.
    
    Args:
        scraped_json: JSON string containing scraped Amazon reviews
        
    Returns:
        dict: Structured script with metadata and AIDA segments
    """
    # 1. Setup Cache Directory
    scripts_dir = Path("scripts_cache")
    scripts_dir.mkdir(exist_ok=True)
    cache_path = scripts_dir / f"{asin}_script.json"

    # 2. Check if the script is already cached
    if cache_path.exists():
        print(f"\n[Cache Hit] Loading generated script for {asin} from local storage...")
        return json.loads(cache_path.read_text(encoding='utf-8'))

    # 3. If no cache, run the LLM (only if necessary)
    print(f"\n[Cache Miss] Synthesizing script into structured JSON for {asin}...")
    
    llm = OllamaLLM(model="llama3", format="json")  # Force Ollama to output JSON
    
    prompt = PromptTemplate.from_template("""
        Analyze these Amazon reviews: {data}

        Return ONLY a JSON object for a 45-second video script using the AIDA framework.

        STRICT GUIDELINES:
        1. ATTENTION: Start with a controversial or surprising fact about the product category.
        2. INTEREST: Highlight the 'Hero Feature' mentioned most in the reviews.
        3. DESIRE: Address a common 'Main Concern' found in the reviews and debunk it or explain why it's worth it.
        4. ACTION: Create an urgency-based CTA.

        OUTPUT STRUCTURE:
        {{
            "metadata": {{
                "asin": "string",
                "hero_feature": "string",
                "sentiment_score": "0-100"
            }},
            "script": [
                {{
                    "segment": "Attention",
                    "vocal_text": "string",
                    "visual_instruction": "A unique, specific scene description. Avoid generic terms."
                }},
                {{
                    "segment": "Interest",
                    "vocal_text": "string",
                    "visual_instruction": "A unique, specific scene description. Avoid generic terms."
                }},
                {{
                    "segment": "Desire",
                    "vocal_text": "string",
                    "visual_instruction": "A unique, specific scene description. Avoid generic terms."
                }},
                {{
                    "segment": "Action",
                    "vocal_text": "string",
                    "visual_instruction": "A unique, specific scene description. Avoid generic terms."
                }}
            ]
        }}
    """)
    
    response = llm.invoke(prompt.format(data=scraped_json))
    
    # Robust Cleaning: Remove any markdown backticks if the LLM added them
    clean_response = response.strip()
    if clean_response.startswith("```json"):
        clean_response = clean_response.replace("```json", "").replace("```", "").strip()
    elif clean_response.startswith("```"):
        clean_response = clean_response.replace("```", "").strip()

    try:
        script_data = json.loads(clean_response)
        
        # 4. Save to cache for next time
        cache_path.write_text(json.dumps(script_data, indent=4), encoding='utf-8')
        print(f"✓ Script saved to {cache_path}")
        
        # Ensure the JSON is beautified (redundant but ensures consistency)
        beautify_json_files("scripts_cache")
        
        return script_data
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}")
        return {"error": "Invalid JSON", "raw": response}
