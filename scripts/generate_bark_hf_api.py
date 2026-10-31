"""
Generate audio from Suno Bark using Hugging Face Inference API.

This avoids heavy local CPU/GPU compute by delegating audio synthesis
to Hugging Face's hosted inference infrastructure.

Requirements:
    pip install huggingface_hub requests
    export HF_TOKEN="your_huggingface_token"
"""

import os
import argparse
from pathlib import Path
import requests

HF_API_URL = "https://router.huggingface.co/hf-inference/models/suno/bark"

def generate_bark_audio_hf(prompt_text: str, output_path: Path, hf_token: str = None):
    token = hf_token or os.environ.get("HF_TOKEN")
    if not token:
        raise ValueError(
            "HF_TOKEN is required. Please set the HF_TOKEN environment variable "
            "or pass it via --token."
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt_text
    }

    print(f"Sending request to Hugging Face Inference API ({HF_API_URL})...")
    response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)

    if response.status_code == 503:
        # Model is loading on HF warm pool
        error_info = response.json()
        estimated_time = error_info.get("estimated_time", 20.0)
        print(f"Model is currently warming up on HF (estimated wait: {estimated_time}s). Retrying...")
        import time
        time.sleep(estimated_time)
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)

    if response.status_code != 200:
        raise RuntimeError(f"HF API returned status {response.status_code}: {response.text}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Audio received and saved to: {output_path}")

def generate_with_official_client(prompt_text: str, output_path: Path, hf_token: str = None):
    """Alternative using official huggingface_hub InferenceClient."""
    from huggingface_hub import InferenceClient

    token = hf_token or os.environ.get("HF_TOKEN")
    client = InferenceClient(provider="hf-inference", api_key=token)

    print("Generating speech via huggingface_hub InferenceClient (suno/bark)...")
    audio_bytes = client.text_to_speech(prompt_text, model="suno/bark")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    print(f"Audio received and saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate audio with Suno Bark via HF API.")
    parser.add_argument("--prompt-file", type=str, default="data/bark_prompt_a_to_d.txt")
    parser.add_argument("--text", type=str, default=None, help="Direct prompt text")
    parser.add_argument("--output", type=str, default="audio/stories/bark_hf_output.wav")
    parser.add_argument("--token", type=str, default=None, help="HF Token")
    parser.add_argument("--use-client", action="store_true", help="Use huggingface_hub InferenceClient")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    if args.text:
        prompt = args.text
    else:
        p_path = repo_root / args.prompt_file
        with open(p_path, "r", encoding="utf-8") as f:
            prompt = f.read()

    out_file = repo_root / args.output
    if args.use_client:
        generate_with_official_client(prompt, out_file, args.token)
    else:
        generate_bark_audio_hf(prompt, out_file, args.token)
