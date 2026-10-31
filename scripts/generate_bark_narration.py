"""
Generate speech from long text prompts using Suno Bark.

Bark produces expressive audio (including laughter, sighs, pauses) in ~13-14 second clips.
For longer prompts (such as our 200-word A-D narrative), this script splits the text
into natural semantic paragraphs/sentences, generates audio for each chunk, and
concatenates them into a single seamless audio file.

Supports small models and CPU optimization via environment variables:
- SUNO_USE_SMALL_MODELS=True
- SUNO_ENABLE_CPU_OFFLOAD=True
"""

import os
import argparse
from pathlib import Path
import numpy as np
from scipy.io.wavfile import write as write_wav

# Set lightweight model defaults before importing bark
os.environ.setdefault("SUNO_USE_SMALL_MODELS", "True")
os.environ.setdefault("SUNO_ENABLE_CPU_OFFLOAD", "True")

from bark import SAMPLE_RATE, generate_audio, preload_models

def split_into_chunks(text: str):
    """Split text into sentence/paragraph chunks suitable for Bark context window."""
    paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    chunks = []
    for p in paragraphs:
        # If paragraph is within reasonable length (~30-40 words), keep as chunk
        if len(p.split()) <= 45:
            chunks.append(p)
        else:
            # Split by period if paragraph is longer
            sents = [s.strip() + "." for s in p.split(". ") if s.strip()]
            chunks.extend(sents)
    return chunks

def generate_bark_story(prompt_path: Path, output_path: Path, voice_preset: str = "v2/en_speaker_6"):
    print(f"Loading prompt from: {prompt_path}")
    with open(prompt_path, "r", encoding="utf-8") as f:
        text = f.read()

    word_count = len(text.split())
    print(f"Prompt word count: {word_count} words")

    chunks = split_into_chunks(text)
    print(f"Divided prompt into {len(chunks)} audio chunks for synthesis.\n")

    print("Preloading Bark models (text-to-semantic, semantic-to-coarse, coarse-to-fine)...")
    preload_models()

    audio_segments = []
    # 0.25 second pause between chunks
    silence = np.zeros(int(0.25 * SAMPLE_RATE))

    for idx, chunk in enumerate(chunks, 1):
        print(f"[{idx}/{len(chunks)}] Synthesizing chunk: \"{chunk[:60]}...\"")
        audio_array = generate_audio(chunk, history_prompt=voice_preset)
        audio_segments.append(audio_array)
        audio_segments.append(silence)

    print("\nConcatenating audio pieces...")
    final_audio = np.concatenate(audio_segments)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_wav(str(output_path), SAMPLE_RATE, final_audio)
    print(f"Successfully generated Bark audio: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Bark narration for phonics prompt.")
    parser.add_argument("--prompt", type=str, default="data/bark_prompt_a_to_d.txt", help="Path to text prompt")
    parser.add_argument("--output", type=str, default="audio/stories/bark_a_to_d_story.wav", help="Output WAV path")
    parser.add_argument("--voice", type=str, default="v2/en_speaker_6", help="Bark speaker preset")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    p_path = repo_root / args.prompt
    o_path = repo_root / args.output

    generate_bark_story(p_path, o_path, voice_preset=args.voice)
