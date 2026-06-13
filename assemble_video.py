from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip, vfx
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

    for i, segment in enumerate(script_data['script']):
        pool_files = sorted(assets_dir.glob(f"segment_{i}_*.mp4"))

        # Check if this is the "Desire/Alternative" segment where you want the image
        if "alternative" in segment['vocal_text'].lower() and product_image_path:
            print(f"  > Injecting product image into Segment {i}")

            # Create a 2-second clip from the product image
            img_clip = (ImageClip(str(product_image_path))
                        .with_duration(2.0)
                        .resized(width=1080))

            stock_duration = segment_duration - 2.0
            if pool_files and stock_duration > 0:
                stock_clip = VideoFileClip(str(pool_files[0])).resized(height=1920)
                if stock_clip.w > 1080:
                    stock_clip = stock_clip.cropped(x_center=stock_clip.w/2, width=1080)

                if stock_clip.duration < stock_duration:
                    stock_clip = stock_clip.with_effects([vfx.Loop(duration=stock_duration)])
                else:
                    stock_clip = stock_clip.with_duration(stock_duration)

                clips.append(concatenate_videoclips([stock_clip, img_clip], method="chain"))
            else:
                clips.append(img_clip.with_duration(segment_duration))

        elif pool_files:
            # Cut this segment into ~4s sub-clips, cycling through the pool
            sub_duration = 4.0
            num_subclips = max(1, round(segment_duration / sub_duration))
            actual_sub = segment_duration / num_subclips

            segment_clips = []
            for k in range(num_subclips):
                src = pool_files[k % len(pool_files)]
                sc = VideoFileClip(str(src)).resized(height=1920)
                if sc.w > 1080:
                    sc = sc.cropped(x_center=sc.w/2, width=1080)

                if sc.duration < actual_sub:
                    sc = sc.with_effects([vfx.Loop(duration=actual_sub)])
                else:
                    sc = sc.with_duration(actual_sub)

                segment_clips.append(sc)

            clips.append(concatenate_videoclips(segment_clips, method="chain"))

        else:
            print(f"Warning: no clips for segment {i}. Skipping.")

    if clips:
        final_video = concatenate_videoclips(clips, method="chain")
        final_video = final_video.with_audio(audio)

        output_name = "final_amazon_short.mp4"
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