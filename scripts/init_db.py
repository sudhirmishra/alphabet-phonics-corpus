import json
import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS letters (
    letter TEXT PRIMARY KEY,
    phonetic_hint TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS words (
    id TEXT PRIMARY KEY,
    letter TEXT NOT NULL,
    word TEXT NOT NULL,
    part_of_speech TEXT,
    difficulty TEXT DEFAULT 'beginner',
    audio_path TEXT,
    image_path TEXT,
    FOREIGN KEY (letter) REFERENCES letters(letter)
);

CREATE TABLE IF NOT EXISTS sentences (
    id TEXT PRIMARY KEY,
    word_id TEXT NOT NULL,
    sentence TEXT NOT NULL,
    audio_path TEXT,
    FOREIGN KEY (word_id) REFERENCES words(id)
);

CREATE INDEX IF NOT EXISTS idx_words_letter ON words(letter);
CREATE INDEX IF NOT EXISTS idx_sentences_word_id ON sentences(word_id);
"""

def init_db(db_path: Path):
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()

def build_db_from_json(json_path: Path, db_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for item in data:
        cur.execute(
            "INSERT OR REPLACE INTO letters (letter, phonetic_hint, description) VALUES (?, ?, ?)",
            (item["letter"], item.get("phonetic_hint", ""), item.get("description", ""))
        )
        for w in item.get("words", []):
            cur.execute(
                """INSERT OR REPLACE INTO words 
                   (id, letter, word, part_of_speech, difficulty, audio_path, image_path) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    w["id"],
                    item["letter"],
                    w["word"],
                    w.get("part_of_speech", ""),
                    w.get("difficulty", "beginner"),
                    w.get("audio_path", ""),
                    w.get("image_path", "")
                )
            )
            for s in w.get("sentences", []):
                cur.execute(
                    """INSERT OR REPLACE INTO sentences (id, word_id, sentence, audio_path) 
                       VALUES (?, ?, ?, ?)""",
                    (s["id"], w["id"], s["sentence"], s.get("audio_path", ""))
                )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    base = Path(__file__).parent.parent
    db_file = base / "data" / "alphabet_corpus.db"
    json_file = base / "data" / "corpus.json"
    init_db(db_file)
    if json_file.exists():
        build_db_from_json(json_file, db_file)
        print(f"Database populated at: {db_file}")
    else:
        print(f"Database initialized at: {db_file}")
