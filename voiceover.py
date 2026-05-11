"""
Voiceover Generation Module
Generates AI voiceover using Microsoft Neural voice via edge-tts.
"""

import asyncio
import edge_tts


async def generate_voiceover(script_data: dict) -> None:
    """
    Generates AI voiceover from script data using Microsoft Neural voice.
    
    Args:
        script_data: Dictionary containing script segments with vocal_text
        
    Returns:
        None (saves to narration.mp3)
    """
    print("\n[Step 3] Generating AI Voiceover (Microsoft Neural)...")
    
    # Combine all vocal texts into one long string for the narrator
    full_text = " ".join([s['vocal_text'] for s in script_data['script']])
    
    # Using 'en-US-ChristopherNeural' for a professional reviewer vibe
    communicate = edge_tts.Communicate(full_text, "en-US-ChristopherNeural")
    await communicate.save("narration.mp3")
    print("✓ Voiceover saved as narration.mp3")
