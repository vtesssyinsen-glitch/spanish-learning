"""
Run this script on your computer to generate Spanish audio files.

Install dependencies first:
    pip install gtts

Then run:
    python generate_audio.py

The script will create an 'audio/' folder with all MP3 files.
Commit and push the audio/ folder to GitHub to complete the setup.
"""

import hashlib
import os
import re

def main():
    try:
        from gtts import gTTS
    except ImportError:
        print("Please install gTTS first: pip install gtts")
        return

    # All Spanish phrases from the website
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    phrases = list(dict.fromkeys(re.findall(r'spanish:"([^"]+)"', content)))
    print(f"Found {len(phrases)} phrases to generate.")

    os.makedirs("audio", exist_ok=True)

    for i, phrase in enumerate(phrases):
        key = hashlib.md5(phrase.encode()).hexdigest()
        path = f"audio/{key}.mp3"
        if os.path.exists(path):
            print(f"[{i+1}/{len(phrases)}] Skip (exists): {phrase[:40]}")
            continue
        try:
            tts = gTTS(text=phrase, lang="es")
            tts.save(path)
            print(f"[{i+1}/{len(phrases)}] OK: {phrase[:40]}")
        except Exception as e:
            print(f"[{i+1}/{len(phrases)}] ERROR: {phrase[:40]} — {e}")

    count = len([f for f in os.listdir("audio") if f.endswith(".mp3")])
    print(f"\nDone! {count} audio files in audio/")
    print("Now run: git add audio/ && git commit -m 'Add pre-generated Spanish audio' && git push")

if __name__ == "__main__":
    main()
