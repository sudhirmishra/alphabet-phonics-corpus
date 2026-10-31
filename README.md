# Alphabet Phonics & Sentences Corpus (Grade-Wise Phonics)

An extensible, structured corpus of A to Z alphabet words, phonetics, and sentences graduated from **Pre-K foundational phonics** up to **Grade 5 advanced vocabulary**, paired with neural speech audio capabilities via [Kokoro TTS](https://github.com/hexgrad/kokoro).

---

## 📚 Grade-Wise Curriculum Progression

Every letter from **A to Z** has words and contextual sentences classified across 7 educational reading stages (total **182 words** and **182 sentences**):

| Grade Level | Target Ages | Phonics & Vocabulary Focus | Example Words |
| :--- | :---: | :--- | :--- |
| **Pre-K** | Ages 3–4 | 3-letter CVC words, short vowels, foundational phonemes | *Ant, Bat, Cat, Dog, Egg, Fox, Sun* |
| **Kindergarten** | Ages 5–6 | Early sight words, basic vowel families, everyday objects | *Apple, Ball, Cup, Duck, Fish, Sock* |
| **Grade 1** | Ages 6–7 | Consonant blends, digraphs, high-frequency sight words | *Acorn, Bird, Cloud, Drum, Frog, Star* |
| **Grade 2** | Ages 7–8 | Multi-syllable basics, compound words, descriptive story words | *Anchor, Castle, Dragon, Feather, Rocket* |
| **Grade 3** | Ages 8–9 | Descriptive adjectives, nature, inquiry, and community | *Astronaut, Compass, Dolphin, Glacier, Rainbow* |
| **Grade 4** | Ages 9–10 | Academic, scientific, and sensory literature vocabulary | *Altitude, Curiosity, Ecosystem, Nebula, Quasar* |
| **Grade 5** | Ages 10–11 | Abstract thinking, nuance, and advanced expressive concepts | *Abundance, Benevolent, Diligent, Eloquent, Resilient* |

---

## 📁 Repository Structure

```
.
├── index.html                   # Interactive player with Grade and Letter filtering
├── data/
│   ├── corpus.json              # 182 words & 182 sentences with grade metadata
│   └── alphabet_corpus.db       # SQLite database with normalized `grades`, `letters`, `words`, `sentences`
├── audio/
│   ├── words/                   # Synthesized audio files
│   └── sentences/               # Synthesized sentence audio files
├── scripts/
│   ├── build_grade_corpus.py    # Generates the grade-wise JSON corpus
│   ├── init_db.py               # SQLite schema & JSON-to-SQLite sync tool
│   ├── generate_all_audio.py    # Kokoro TTS batch synthesis pipeline
│   └── generate_bark_narration.py # Suno Bark expressive story generation
├── devbox.json                  # Devbox environment configuration
├── requirements.txt             # Python dependencies
└── README.md
```

Includes:
- **Relational database & schema**: SQLite database (`data/alphabet_corpus.db`) supporting 1-to-many relationships (multiple words per letter, multiple sentences per word, media mappings for audio and images).
- **Portable JSON Dataset**: Structured format in [`data/corpus.json`](data/corpus.json) ideal for web apps and APIs.
- **Interactive Web Player**: Static GitHub Pages site in [`index.html`](index.html) for listening to words and sentences letter by letter.
- **Batch Generation Scripts**: Automated generation using Python and Kokoro TTS.
- **Suno Bark Expressive Narration**: Dedicated 200-word expressive story prompt (`data/bark_prompt_a_to_d.txt`) and pipeline script (`scripts/generate_bark_narration.py`) covering letters A to D.
- **Dual Environment Management**: Reproducible Nix/Devbox environment (`devbox.json`) or standalone `scripts/setup.sh` + `requirements.txt`.

---

## 🛠 Setup & Environment Management

You can set up and run this project using **Devbox** (recommended) or a standard **Python virtual environment**.

### Option A: Using Devbox (Recommended)
This repo provides a [`devbox.json`](devbox.json) with Python 3.12, `libsndfile`, `ffmpeg`, and automated hooks:
```bash
# Enter isolated shell (automatically activates .venv)
devbox shell

# Run project setup
devbox run setup

# Run generation
devbox run generate-kokoro
devbox run generate-bark
```

### Option B: Standalone Python Setup
A self-contained [`scripts/setup.sh`](scripts/setup.sh) script handles virtual environment creation, dependency installation from [`requirements.txt`](requirements.txt), and SQLite sync:
```bash
bash scripts/setup.sh
source .venv/bin/activate
```

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
