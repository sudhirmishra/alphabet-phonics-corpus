import os
import json
import time
from pathlib import Path
import soundfile as sf
from kokoro import KPipeline

def load_env(env_path: Path):
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

def main():
    repo_root = Path(__file__).parent.parent
    load_env(repo_root / ".env")
    
    data_file = repo_root / "data" / "corpus.json"
    audio_dir = repo_root / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    with open(data_file, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    print("Initializing Kokoro pipeline (American English, voice='af_heart')...")
    pipeline = KPipeline(lang_code="a")
    voice = "af_heart"

    total_words_generated = 0
    total_sentences_generated = 0
    skipped_count = 0
    start_time = time.time()

    for letter_entry in corpus:
        letter = letter_entry["letter"]
        print(f"\n==========================================")
        print(f" Processing Letter [{letter}]")
        print(f"==========================================")
        
        for word_entry in letter_entry.get("words", []):
            word_text = word_entry["word"]
            grade = word_entry.get("grade", "Pre-K")
            rel_word_audio = word_entry["audio_path"]
            word_target = repo_root / rel_word_audio
            word_target.parent.mkdir(parents=True, exist_ok=True)

            # Generate Word Audio
            if not word_target.exists():
                print(f"[{letter}] ({grade}) Word: '{word_text}' -> {rel_word_audio}")
                for _, _, audio in pipeline(word_text, voice=voice, speed=1.0):
                    sf.write(str(word_target), audio, 24000)
                    total_words_generated += 1
                    break
            else:
                skipped_count += 1

            # Generate Sentence Audio
            for s_entry in word_entry.get("sentences", []):
                s_text = s_entry["sentence"]
                rel_s_audio = s_entry["audio_path"]
                s_target = repo_root / rel_s_audio
                s_target.parent.mkdir(parents=True, exist_ok=True)

                if not s_target.exists():
                    print(f"[{letter}] ({grade}) Sentence: \"{s_text}\" -> {rel_s_audio}")
                    for _, _, audio in pipeline(s_text, voice=voice, speed=1.0):
                        sf.write(str(s_target), audio, 24000)
                        total_sentences_generated += 1
                        break
                else:
                    skipped_count += 1

    elapsed = time.time() - start_time
    print(f"\n==========================================")
    print(f" Kokoro Generation Complete!")
    print(f"  - Words synthesized     : {total_words_generated}")
    print(f"  - Sentences synthesized : {total_sentences_generated}")
    print(f"  - Files already cached  : {skipped_count}")
    print(f"  - Time taken            : {elapsed:.1f}s")
    print(f"==========================================")

if __name__ == "__main__":
    main()
