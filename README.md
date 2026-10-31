# Alphabet Phonics & Sentences Corpus (Kokoro TTS)

An extensible, structured corpus of A to Z alphabet words, phonetics, and sentences paired with high-quality neural speech audio generated using [Kokoro TTS](https://github.com/hexgrad/kokoro) (`af_heart` voice).

Includes:
- **Relational database & schema**: SQLite database (`data/alphabet_corpus.db`) supporting 1-to-many relationships (multiple words per letter, multiple sentences per word, media mappings for audio and images).
- **Portable JSON Dataset**: Structured format in [`data/corpus.json`](data/corpus.json) ideal for web apps and APIs.
- **Interactive Web Player**: Static GitHub Pages site in [`index.html`](index.html) for listening to words and sentences letter by letter.
- **Batch Generation Scripts**: Automated generation using Python and Kokoro TTS.
- **Suno Bark Expressive Narration**: Dedicated 200-word expressive story prompt (`data/bark_prompt_a_to_d.txt`) and pipeline script (`scripts/generate_bark_narration.py`) covering letters A to D.

---

## 🎭 Bark Story Narration (Letters A to D)

In addition to individual letter/word/sentence phonics audio, the repository includes a custom, emotionally expressive 200-word narrative prompt designed specifically for [Suno Bark](https://github.com/suno-ai/bark):

- **Prompt File**: [`data/bark_prompt_a_to_d.txt`](data/bark_prompt_a_to_d.txt) (exactly 200 words, embedding vocal cues like `[sigh]`, `[laughs]`, and `[gasp]`).
- **Generation Script**: [`scripts/generate_bark_narration.py`](scripts/generate_bark_narration.py) splits long text into semantic chunks, synthesizes expressive audio with speaker presets (e.g. `v2/en_speaker_6`), and concatenates them with natural conversational pauses.

To run Bark synthesis:
```bash
python scripts/generate_bark_narration.py --voice v2/en_speaker_6
```

---

## 📁 Repository Structure

```
.
├── index.html                   # Static web player for GitHub Pages
├── data/
│   ├── corpus.json              # Primary portable JSON dataset
│   └── alphabet_corpus.db       # Relational SQLite database
├── audio/
│   ├── words/                   # Synthesized audio for words (24kHz WAV)
│   └── sentences/               # Synthesized audio for example sentences
├── scripts/
│   ├── init_db.py               # SQLite schema & JSON-to-SQLite sync tool
│   └── generate_all_audio.py    # Kokoro TTS batch synthesis pipeline
└── README.md
```

---

## 🗄 Database Design

The dataset is organized to support adding multiple words per letter, multiple example sentences per word, and linking both audio and image media files:

```
┌──────────────┐       ┌────────────────────┐       ┌──────────────────────┐
│   letters    │       │       words        │       │      sentences       │
├──────────────┤       ├────────────────────┤       ├──────────────────────┤
│ letter (PK)  │──1:N──│ id (PK)            │──1:N──│ id (PK)              │
│ phonetic_hint│       │ letter (FK)        │       │ word_id (FK)         │
│ description  │       │ word               │       │ sentence             │
└──────────────┘       │ part_of_speech     │       │ audio_path           │
                       │ difficulty         │       └──────────────────────┘
                       │ audio_path         │
                       │ image_path         │
                       └────────────────────┘
```

### Extending the Corpus
1. To add a new word or sentence, simply add an entry into `data/corpus.json`.
2. Sync the SQLite database:
   ```bash
   python scripts/init_db.py
   ```
3. Run audio synthesis:
   ```bash
   python scripts/generate_all_audio.py
   ```

---

## 🌐 GitHub Pages Live Demo

You can interact with and listen to the alphabet words and sentences directly through GitHub Pages at:
`https://<username>.github.io/<repo-name>/`

---

## 🎙 Technology Stack
- **TTS Engine**: [Kokoro-82M](https://github.com/hexgrad/kokoro) (`kokoro` Python library)
- **Audio Output**: 24kHz Mono WAV via `soundfile`
- **Frontend**: Vanilla HTML5, Modern CSS, Web Audio API (Zero dependencies)
