AMZ-Affiliate Video Factory - Project Documentation
=====================================================
Automated AI Content Pipeline for Amazon Affiliate Marketing

1. PROJECT ARCHITECTURE (THE 5-STEP PIPELINE)
---------------------------------------------
1. Data Acquisition: Apify (junglee/amazon-reviews-scraper) extracts raw product reviews.
2. AI Orchestration: Ollama (Llama 3) uses an AIDA Framework to synthesize reviews into a structured JSON script.
3. Voice Synthesis: edge-tts (Microsoft Neural) generates professional-grade narration.
4. Asset Sourcing: Pexels API fetches relevant B-roll, combined with product image inserts.
5. Video Rendering: MoviePy v2.0 handles the final stitch, resizing, and MP4 encoding.

2. PREREQUISITES & INSTALLATION
-------------------------------
A. Local AI Environment (Ollama)
   - Download: ollama.com
   - Pull Model: Run 'ollama pull llama3' in your terminal.
   - Operation: The Ollama tray icon must be active before running the script.

B. Python Setup
   - Command: python -m venv ai_shorts_env
   - Command: .\ai_shorts_env\Scripts\activate
   - Dependencies: pip install langchain langchain-community apify-client python-dotenv edge-tts pexel-downloader moviepy requests

C. Environment Config (.env)
   Create a .env file in the root directory:
   - APIFY_API_TOKEN=your_apify_token_here
   - PEXELS_API_KEY=your_pexels_api_key_here

3. EXECUTION & CACHING LOGIC
----------------------------
Run the main pipeline: python main.py

The Caching Layer (Developer Efficiency):
- Raw Data: Saved as cache/{asin}.json
- AI Scripts: Saved as scripts_cache/{asin}_script.json

Senior Dev Tip: If you are fine-tuning the video assembly, the script will skip the scraper and LLM phases entirely and go straight to rendering.

4. IMPLEMENTATION DETAILS
-------------------------
Step 1: Data Extraction
Uses Apify to get review text. The extract_asin utility creates a unique ID from the URL for caching.

Step 2: AIDA Scriptwriting
Prompts Llama 3 to output a JSON object containing Attention (hook), Interest/Desire (features), Action (CTA), and Visual Instructions (Pexels queries).

Step 3: Neural TTS (Voiceover)
Uses edge-tts to generate a high-quality .mp3. The audio duration dictates the final video length.

Step 4: Asset Acquisition
- B-Roll: Downloads vertical (portrait) clips from Pexels based on AI instructions.
- Product Image: Fetches the mainImage from Amazon metadata for a 2-second insert.

Step 5: MoviePy v2.0 Assembly
- Normalizes all clips to 1080x1920.
- Syncs video segments to audio timestamps.
- Injects the product image during the "Desire" segment.
- Encodes the final MP4 using libx264.

5. HARDWARE OPTIMIZATION (GTX 1650 Ti / Ryzen 7)
------------------------------------------------
- VRAM Management: Ollama consumes ~3.4GB VRAM. If MoviePy crashes during encoding, close the Ollama app after the "Script Generation" phase to free up the GPU.
- Multithreading: Assembly is configured with threads=8 to utilize the Ryzen 7's 4000-series architecture.

6. ROADMAP
----------
[x] Scraper & Cache System
[x] Local LLM JSON Mode Integration
[x] MoviePy v2.0 Refactor
[ ] Auto-burn Subtitles (TextClip)
[ ] Audio Ducking for Background Music

-----------------------------------------------------