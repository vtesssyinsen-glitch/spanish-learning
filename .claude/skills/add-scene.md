# Add Scene Skill

When the user invokes `/add-scene`, help them add a new Spanish learning scene to the website AND generate audio files for it.

## What to ask the user

If the user hasn't described the scene, ask:
- 场景主题是什么？（例如：在银行、去医院、买东西等）
- 对话难度？（初级/中级）

## Project Architecture

### Audio playback system
- All Spanish audio is pre-generated as MP3 files in `audio/` directory
- Filenames are MD5 hashes of the Spanish phrase text
- `var _audioMap={...}` in index.html maps phrase → MD5 hash
- `window._curAudio` is a single persistent `<audio>` DOM element used for all playback
- `window._lastKey` tracks the last played audio key for toggle play/stop behavior
- `window._spd` controls playback speed (1 or 0.8)
- Clicking same button while playing → stops; clicking again → replays
- Clicking different button → stops current, plays new
- speechSynthesis is used as fallback only on devices with Spanish voices

### UI features
- 🔊 per-sentence play/stop toggle buttons
- `▶ 朗读全文` floating button (bottom-left): plays all dialogue sentences in sequence, shows `⏹ 停止朗读` while playing
- `1x/0.8x` floating speed toggle button (bottom-right)
- Both floating buttons only visible in dialogue view

### Data structure
Each scene in the `const u = [...]` array needs:
- `id`: unique string
- `title`: scene title in Chinese
- `emoji`: relevant emoji
- `subtitle`: Spanish subtitle (e.g. "En el banco")
- `dialogue`: array of conversation lines, each with:
  - `speaker`: "A" or "B"
  - `speakerName`: Chinese name (e.g. "你", "银行员工")
  - `spanish`: the Spanish sentence
  - `pronunciation`: phonetic pronunciation in caps (e.g. "bweh-nos DEE-as")
  - `chinese`: Chinese translation
- `vocabulary`: array of key words, each with:
  - `spanish`: the Spanish word/phrase
  - `pronunciation`: phonetic pronunciation
  - `chinese`: Chinese translation

## Workflow

### Step 1: Generate the scene content

Create a new scene following the data structure above.

### Step 2: Add the scene to index.html

Find the `const u = [...]` array in index.html and append the new scene object. Make sure the JavaScript syntax is valid.

### Step 3: Update the _audioMap in index.html

Re-generate the full `_audioMap` to include new phrases:

```python
import hashlib, re
with open('index.html', 'r') as f:
    content = f.read()
phrases = list(dict.fromkeys(re.findall(r'spanish:"([^"]+)"', content)))
mapping = {p: hashlib.md5(p.encode()).hexdigest() for p in phrases}
# Replace var _audioMap={...} in index.html with updated mapping
```

### Step 4: Generate audio files

The cloud environment cannot reach Google TTS. Tell the user to run on their Windows computer:

```
cd %USERPROFILE%\Desktop\spanish-learning
git pull
py generate_audio.py
git add audio/
git commit -m "Add audio for new scene"
git push origin main
```

The script skips already-existing audio files and only generates new ones.

### Step 5: Commit and push index.html

```bash
git add index.html
git commit -m "Add [scene name] scene"
git push
```

### Step 6: Tell the user

Give the user the Windows commands from Step 4, then tell them the website will be ready after they push the audio files (no PR merge needed since we push directly to main).

## Important notes

- Always maintain valid JavaScript syntax in index.html
- The `_audioMap` must include ALL phrases (not just new ones) — regenerate the full map every time
- Audio filenames are MD5 hashes of the Spanish phrase text: `hashlib.md5(phrase.encode()).hexdigest()`
- The generate_audio.py script skips already-existing audio files
- Push index.html changes directly to main (no PR needed)
- Audio files are pushed directly to main from the user's Windows computer
