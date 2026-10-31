"""
Generate test audio samples for evaluating Kokoro voices and hybrid combinations
using the classic phonological test sentence:
“With tenure, Suzie’d have all the more leisure for yachting, but her publications are no good.”

This sentence stresses:
- Palatalization & glides: "tenure", "leisure", "yachting"
- Contraction & assimilation: "Suzie'd have"
- Vowel contrasts & rhythm: "all the more leisure... but her publications are no good"

Includes:
- Individual pure voices (US female, US male, British female, British male)
- Hybrid voice blends (e.g. 70% Heart + 30% Bella, 50% Heart + 50% Adam, etc.)
- HTML visual comparison showcase to easily play and compare all variants.
"""

import os
import json
import time
from pathlib import Path
import soundfile as sf
import torch
from kokoro import KPipeline

SENTENCE = "With tenure, Suzie’d have all the more leisure for yachting, but her publications are no good."

# Voices to benchmark
VOICE_SPECS = [
    # --- US Female ---
    {"id": "af_heart", "type": "pure", "name": "Heart (US Female)", "desc": "Warm, engaging, standard Kokoro reference voice", "lang": "a"},
    {"id": "af_bella", "type": "pure", "name": "Bella (US Female)", "desc": "Bright, clear, expressive", "lang": "a"},
    {"id": "af_sarah", "type": "pure", "name": "Sarah (US Female)", "desc": "Soft, natural conversational tone", "lang": "a"},
    {"id": "af_nicole", "type": "pure", "name": "Nicole (US Female)", "desc": "Crisp, articulated educational tone", "lang": "a"},
    {"id": "af_sky", "type": "pure", "name": "Sky (US Female)", "desc": "Light, youthful, cheerful", "lang": "a"},
    {"id": "af_alloy", "type": "pure", "name": "Alloy (US Female)", "desc": "Neutral, modern, balanced", "lang": "a"},
    {"id": "af_nova", "type": "pure", "name": "Nova (US Female)", "desc": "Confident, energetic", "lang": "a"},
    {"id": "af_jessica", "type": "pure", "name": "Jessica (US Female)", "desc": "Warm, measured pacing", "lang": "a"},

    # --- US Male ---
    {"id": "am_adam", "type": "pure", "name": "Adam (US Male)", "desc": "Deep, authoritative, standard male", "lang": "a"},
    {"id": "am_michael", "type": "pure", "name": "Michael (US Male)", "desc": "Warm, friendly storytelling tone", "lang": "a"},
    {"id": "am_echo", "type": "pure", "name": "Echo (US Male)", "desc": "Resonant, clear diction", "lang": "a"},
    {"id": "am_eric", "type": "pure", "name": "Eric (US Male)", "desc": "Calm, casual conversational", "lang": "a"},
    {"id": "am_liam", "type": "pure", "name": "Liam (US Male)", "desc": "Youthful, energetic male", "lang": "a"},
    {"id": "am_onyx", "type": "pure", "name": "Onyx (US Male)", "desc": "Deep baritone, smooth resonance", "lang": "a"},

    # --- British English ---
    {"id": "bf_emma", "type": "pure", "name": "Emma (UK Female)", "desc": "Standard British RP, clear and poised", "lang": "b"},
    {"id": "bf_isabella", "type": "pure", "name": "Isabella (UK Female)", "desc": "Soft British accent, gentle cadence", "lang": "b"},
    {"id": "bm_george", "type": "pure", "name": "George (UK Male)", "desc": "Distinguished, classic British narrative", "lang": "b"},
    {"id": "bm_daniel", "type": "pure", "name": "Daniel (UK Male)", "desc": "Warm British male, modern broadcast feel", "lang": "b"},

    # --- Hybrid Blends (Custom Voice Mixtures) ---
    {
        "id": "hybrid_heart_bella_70_30",
        "type": "blend",
        "name": "Hybrid: Heart (70%) + Bella (30%)",
        "desc": "Keeps Heart's warmth while gaining Bella's bright, crisp phonemic articulation",
        "lang": "a",
        "components": [("af_heart", 0.7), ("af_bella", 0.3)]
    },
    {
        "id": "hybrid_heart_nicole_60_40",
        "type": "blend",
        "name": "Hybrid: Heart (60%) + Nicole (40%)",
        "desc": "Educational blend: friendly yet highly articulate for complex phonological words",
        "lang": "a",
        "components": [("af_heart", 0.6), ("af_nicole", 0.4)]
    },
    {
        "id": "hybrid_heart_sarah_50_50",
        "type": "blend",
        "name": "Hybrid: Heart (50%) + Sarah (50%)",
        "desc": "Ultra-smooth, gentle storytelling blend with reduced sibilance",
        "lang": "a",
        "components": [("af_heart", 0.5), ("af_sarah", 0.5)]
    },
    {
        "id": "hybrid_adam_michael_60_40",
        "type": "blend",
        "name": "Hybrid: Adam (60%) + Michael (40%)",
        "desc": "Balanced male narrator: Adam's clarity blended with Michael's warmth",
        "lang": "a",
        "components": [("am_adam", 0.6), ("am_michael", 0.4)]
    },
    {
        "id": "hybrid_heart_adam_duet_70_30",
        "type": "blend",
        "name": "Hybrid: Heart (70%) + Adam (30%)",
        "desc": "Gives Heart a slightly richer, grounded lower mid-range frequency response",
        "lang": "a",
        "components": [("af_heart", 0.7), ("am_adam", 0.3)]
    }
]

def main():
    repo_root = Path(__file__).parent.parent
    output_dir = repo_root / "audio" / "voice_samples"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Initializing Kokoro Pipelines ('a' American, 'b' British)...")
    pipeline_a = KPipeline(lang_code="a")
    pipeline_b = KPipeline(lang_code="b")

    samples_manifest = []

    print(f"\nTest Sentence:\n  \"{SENTENCE}\"\n")
    print(f"Generating samples across {len(VOICE_SPECS)} pure and hybrid voices...\n")

    for spec in VOICE_SPECS:
        v_id = spec["id"]
        v_name = spec["name"]
        pipeline = pipeline_a if spec["lang"] == "a" else pipeline_b
        out_filename = f"{v_id}.wav"
        out_path = output_dir / out_filename
        rel_path = f"audio/voice_samples/{out_filename}"

        print(f"Generating [{spec['type'].upper()}]: {v_name}...")
        t0 = time.time()

        if spec["type"] == "pure":
            voice_param = v_id
        else:
            # Create hybrid blended voice tensor
            blended_tensor = None
            for comp_id, weight in spec["components"]:
                t = pipeline.load_voice(comp_id)
                if blended_tensor is None:
                    blended_tensor = weight * t
                else:
                    blended_tensor += weight * t
            voice_param = blended_tensor

        for _, _, audio in pipeline(SENTENCE, voice=voice_param, speed=1.0):
            sf.write(str(out_path), audio, 24000)
            break

        dur = time.time() - t0
        print(f"  -> Saved: {out_filename} ({dur:.2f}s)")

        samples_manifest.append({
            "id": v_id,
            "name": v_name,
            "type": spec["type"],
            "desc": spec["desc"],
            "lang": "US" if spec["lang"] == "a" else "UK",
            "audio_path": rel_path
        })

    # Save manifest JSON for web comparison
    manifest_file = output_dir / "samples_manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(samples_manifest, f, indent=2)

    print(f"\nAll voice samples generated in: {output_dir}")
    print(f"Manifest written to: {manifest_file}")

if __name__ == "__main__":
    main()
