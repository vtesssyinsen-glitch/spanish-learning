# Add Scene Skill

When the user invokes `/add-scene`, help them add a new Spanish learning scene to the website AND generate audio files for it.

## What to ask the user

If the user hasn't described the scene, ask:
- 场景主题是什么？（例如：在银行、去医院、买东西等）
- 对话难度？（初级/中级）

## Workflow

### Step 1: Generate the scene content

Create a new scene following the existing data structure in `index.html`. Each scene needs:
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

### Step 2: Add the scene to index.html

Find the `const u = [...]` array in index.html (the scenes data array) and append the new scene object to it. Make sure the JSON syntax is valid.

### Step 3: Generate audio files

Run this Python script to generate audio for the new phrases only (it skips existing ones):

```bash
python3 generate_audio.py
```

If the cloud environment cannot reach Google TTS (403 error), generate the audio map entry and tell the user to run `py generate_audio.py` on their Windows computer, then `git add audio/ && git commit -m "Add audio for new scene" && git push origin main`.

### Step 4: Update the _audioMap in index.html

The `_audioMap` JavaScript object in index.html needs to include the new phrases. Re-generate it by running:

```python
import hashlib, re
with open('index.html', 'r') as f:
    content = f.read()
phrases = list(dict.fromkeys(re.findall(r'spanish:"([^"]+)"', content)))
mapping = {p: hashlib.md5(p.encode()).hexdigest() for p in phrases}
print(len(phrases), "phrases in map")
```

Then replace the old `var _audioMap={...}` in index.html with the updated map that includes all phrases including the new ones.

### Step 5: Commit and push

```bash
git add index.html audio/
git commit -m "Add [scene name] scene with audio"
git push
```

### Step 6: Tell the user

- If audio was generated here: "已完成！请去 GitHub 合并 PR。"
- If audio needs to be generated on their Windows computer: Give them the exact commands to run, then merge PR.

## Important notes

- Always maintain valid JavaScript syntax in index.html
- The `_audioMap` must include ALL phrases (not just new ones)
- Audio filenames are MD5 hashes of the Spanish phrase text
- The generate_audio.py script skips already-existing audio files
