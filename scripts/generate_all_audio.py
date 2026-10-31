import os
import json
from pathlib import Path
import soundfile as sf
from kokoro import KPipeline

def main():
    repo_root = Path(__file__).parent.parent
    data_file = repo_root / "data" / "corpus.json"
    audio_dir = repo_root / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    with open(data_file, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    print("Initializing Kokoro pipeline (American English, af_heart voice)...")
    pipeline = KPipeline(lang_code="a")
    voice = "af_heart"

    total_words = 0
    total_sentences = 0

    for letter_entry in corpus:
        letter = letter_entry["letter"]
        print(f"\n--- Generating for Letter {letter} ---")
        for word_entry in letter_entry.get("words", []):
            word_text = word_entry["word"]
            rel_word_audio = word_entry["audio_path"]
            word_target = repo_root / rel_word_audio
            word_target.parent.mkdir(parents=True, exist_ok=True)

            print(f"Synthesizing word: '{word_text}' -> {rel_word_audio}")
            for _, _, audio in pipeline(word_text, voice=voice, speed=1.0):
                sf.write(str(word_target), audio, 24000)
                total_words += 1
                break

            for s_entry in word_entry.get("sentences", []):
                s_text = s_entry["sentence"]
                rel_s_audio = s_entry["audio_path"]
                s_target = repo_root / rel_s_audio
                s_target.parent.mkdir(parents=True, exist_ok=True)

                print(f"Synthesizing sentence: '{s_text}' -> {rel_s_audio}")
                for _, _, audio in pipeline(s_text, voice=voice, speed=1.0):
                    sf.write(str(s_target), audio, 24000)
                    total_sentences += 1
                    break

    print(f"\nDone! Generated {total_words} words and {total_sentences} sentences.")

if __name__ == "__main__":
    main()
