"""
Stock Visuals Fetching Module
Fetches stock footage from Pexels for video segments.
"""

import os
import shutil
from pathlib import Path
from pexel_downloader import PexelDownloader


def fetch_visuals(script_data: dict) -> None:
    """
    Downloads stock footage from Pexels based on visual instructions in the script.
    
    Args:
        script_data: Dictionary containing script segments with visual_instruction
        
    Returns:
        None (saves video assets to video_assets folder)
    """
    print("\n[Step 4] Fetching Stock Footage from Pexels...")
    
    api_key = os.getenv("PEXELS_API_KEY")
    downloader = PexelDownloader(api_key=api_key)
    
    # Create a clean assets folder
    assets_dir = Path("video_assets")
    if assets_dir.exists():
        try:
            shutil.rmtree(assets_dir)  # Clear old clips to avoid confusion
        except PermissionError as e:
            print(f"  ! Warning: Could not delete old assets directory ({e}). Will overwrite files instead.")
    assets_dir.mkdir(exist_ok=True)

    for i, segment in enumerate(script_data['script']):
        query = segment['visual_instruction']
        print(f"  > Downloading clips for Segment {i}: '{query}'")
        
        try:
            # Download a pool of portrait videos for the segment
            # Note: pexel-downloader saves with its own naming scheme
            downloader.download_videos(
                query=query, 
                num_videos=5, 
                save_directory=str(assets_dir), 
                size="medium"
            )
            
            # Logic to find the newly downloaded files and rename them
            # This ensures Step 5 (MoviePy) can find the pool easily
            downloaded_files = list(assets_dir.glob("*.mp4"))
            # Sort by creation time to find the latest batch
            downloaded_files.sort(key=os.path.getmtime, reverse=True)
            pool = downloaded_files[:5]

            if pool:
                for j, f in enumerate(pool):
                    os.rename(f, assets_dir / f"segment_{i}_{j}.mp4")
            else:
                print(f"  ! No files downloaded for segment {i}")

        except Exception as e:
            print(f"  ! Failed to get clip for '{query}': {e}")