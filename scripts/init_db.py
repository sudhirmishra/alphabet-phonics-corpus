import json
import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS letters (
    letter TEXT PRIMARY KEY,
    phonetic_hint TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS grades (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age_range TEXT,
    description TEXT,
    rank INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS words (
    id TEXT PRIMARY KEY,
    letter TEXT NOT NULL,
    word TEXT NOT NULL,
    grade TEXT NOT NULL,
    part_of_speech TEXT,
    audio_path TEXT,
    image_path TEXT,
    FOREIGN KEY (letter) REFERENCES letters(letter),
    FOREIGN KEY (grade) REFERENCES grades(id)
);

CREATE TABLE IF NOT EXISTS sentences (
    id TEXT PRIMARY KEY,
    word_id TEXT NOT NULL,
    sentence TEXT NOT NULL,
    audio_path TEXT,
    FOREIGN KEY (word_id) REFERENCES words(id)
);

CREATE INDEX IF NOT EXISTS idx_words_letter ON words(letter);
CREATE INDEX IF NOT EXISTS idx_words_grade ON words(grade);
CREATE INDEX IF NOT EXISTS idx_sentences_word_id ON sentences(word_id);
"""

GRADES_DATA = [
    ("Pre-K", "Pre-Kindergarten", "3-4", "Simple 3-letter CVC words, foundational phonics", 0),
    ("Kindergarten", "Kindergarten", "5-6", "Early sight words, short vowels, foundational reading", 1),
    ("Grade 1", "First Grade", "6-7", "Consonant blends, long vowels, high-frequency sight words", 2),
    ("Grade 2", "Second Grade", "7-8", "Multi-syllable basics, compound words, descriptive words", 3),
    ("Grade 3", "Third Grade", "8-9", "Descriptive adjectives, nature, school, and community concepts", 4),
    ("Grade 4", "Fourth Grade", "9-10", "Academic, scientific, and literary vocabulary", 5),
    ("Grade 5", "Fifth Grade", "10-11", "Abstract thinking, expressive words, advanced concepts", 6)
]

def init_db(db_path: Path):
    if db_path.exists():
        db_path.unlink()  # Clean reset for new schema
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)
    cur = conn.cursor()
    for gid, name, age, desc, rank in GRADES_DATA:
        cur.execute(
            "INSERT OR REPLACE INTO grades (id, name, age_range, description, rank) VALUES (?, ?, ?, ?, ?)",
            (gid, name, age, desc, rank)
        )
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
                   (id, letter, word, grade, part_of_speech, audio_path, image_path) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    w["id"],
                    item["letter"],
                    w["word"],
                    w.get("grade", "Pre-K"),
                    w.get("part_of_speech", ""),
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
        print(f"Database successfully rebuilt & populated at: {db_file}")
    else:
        print(f"Database initialized at: {db_file}")
