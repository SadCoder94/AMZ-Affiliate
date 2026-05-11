from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip
from pathlib import Path
import os

def assemble_video(script_data, product_image_path=None):
    print("\n[Step 5] Assembling Final Video with MoviePy...")
    
    assets_dir = Path("video_assets")
    audio_path = "narration.mp3"
    
    if not os.path.exists(audio_path):
        print("Error: Narration audio not found.")
        return

    audio = AudioFileClip(audio_path)
    clips = []
    
    # Calculate duration per segment
    num_segments = len(script_data['script'])
    segment_duration = audio.duration / num_segments

    for i,segment in enumerate(script_data['script']):
        video_path = assets_dir / f"segment_{i}.mp4"
        
        # Check if this is the "Desire/Alternative" segme   nt where you want the image
        # Logic: If 'alternative' or 'product' is in the vocal text, insert image
        if "alternative" in segment['vocal_text'].lower() and product_image_path:
            print(f"  > Injecting product image into Segment {i}")
            
            # Create a 2-second clip from the product image
            img_clip = (ImageClip(str(product_image_path))
                        .with_duration(2.0)
                        .resized(width=1080)) # Ensure it fits vertical width
            
            # Get the remaining stock footage for this segment
            stock_duration = segment_duration - 2.0
            if video_path.exists() and stock_duration > 0:
                stock_clip = VideoFileClip(str(video_path)).with_duration(stock_duration).resized(height=1920)
                # Combine: Stock -> Product Image
                clips.append(concatenate_videoclips([stock_clip, img_clip], method="chain"))
            else:
                clips.append(img_clip.with_duration(segment_duration))

        elif video_path.exists():
            # Load clip
            clip = VideoFileClip(str(video_path))
            
            # 1. Resize/Crop to Vertical (1080x1920)
            # v2.0 uses .resized() and .cropped()
            clip = clip.resized(height=1920)
            if clip.w > 1080:
                clip = clip.cropped(x_center=clip.w/2, width=1080)
            
            # 2. Adjust duration
            # v2.0 uses .with_duration()
            if clip.duration < segment_duration:
                # Loop if too short
                clip = clip.with_effects([lambda c: c.loop(duration=segment_duration)])
            else:
                clip = clip.with_duration(segment_duration)
                
            clip = VideoFileClip(str(video_path)).resized(height=1920)
            if clip.w > 1080:
                clip = clip.cropped(x_center=clip.w/2, width=1080)
            clips.append(clip.with_duration(segment_duration))
        else:
            print(f"Warning: segment_{i}.mp4 missing. Skipping.")

    if clips:
        # 3. Concatenate and attach audio
        # 'method="chain"' is the new default for simple sequences
        final_video = concatenate_videoclips(clips, method="chain")
        final_video = final_video.with_audio(audio)
        
        # 4. Write the file
        output_name = "final_amazon_short.mp4"
        # MoviePy v2.0 handles codecs very cleanly on Windows
        final_video.write_videofile(
            output_name, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac",
            temp_audiofile='temp-audio.m4a', 
            remove_temp=True,
            threads=8
        )
        print(f"\n✓ SUCCESS! Video rendered as {output_name}")
    else:
        print("Error: No video clips were successfully processed.")