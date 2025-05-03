# Auto Video Generator Web Server (Python + FastAPI + MoviePy)
# Requirements: pip install fastapi uvicorn moviepy requests

from fastapi import FastAPI, Request
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import requests
import os

app = FastAPI()

@app.post("/generate")
async def generate_video(request: Request):
    data = await request.json()
    script_text = data.get("script_text")
    audio_url = data.get("audio_url")
    background_url = data.get("background_url")

    AUDIO_PATH = "voiceover.mp3"
    BACKGROUND_PATH = "background.mp4"
    OUTPUT_VIDEO = "final_video.mp4"

    # Download audio and background video
    with open(AUDIO_PATH, 'wb') as f:
        f.write(requests.get(audio_url).content)

    with open(BACKGROUND_PATH, 'wb') as f:
        f.write(requests.get(background_url).content)

    # Load audio and background video
    audio = AudioFileClip(AUDIO_PATH)
    background = VideoFileClip(BACKGROUND_PATH).subclip(0, audio.duration)
    background = background.resize((1080, 1920))  # Vertical format

    # Create text caption
    caption = TextClip(script_text, fontsize=60, color='white', bg_color='black', size=(1000, None), method='caption')
    caption = caption.set_duration(audio.duration).set_position(('center', 'bottom'))

    # Create final video
    final = CompositeVideoClip([background, caption.set_start(0)]).set_audio(audio)
    final.write_videofile(OUTPUT_VIDEO, fps=30, codec='libx264')

    return {"status": "success", "output_file": OUTPUT_VIDEO}

# To run locally: uvicorn script_name:app --reload --host 0.0.0.0 --port 8000
