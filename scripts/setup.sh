#!/usr/bin/env bash
# ==============================================================================
# Setup script for Alphabet Phonics Corpus (Kokoro TTS + Suno Bark)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

echo "======================================================"
echo " Setting up Alphabet Phonics Corpus Environment"
echo "======================================================"

# 1. Determine or create virtual environment
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
    VENV_DIR="${REPO_ROOT}/.venv"
    if [[ ! -d "${VENV_DIR}" ]]; then
        echo "[1/4] Creating virtual environment at .venv..."
        python3 -m venv "${VENV_DIR}"
    else
        echo "[1/4] Existing virtual environment found at .venv."
    fi
    # Activate virtual environment
    # shellcheck disable=SC1091
    source "${VENV_DIR}/bin/activate"
else
    echo "[1/4] Active virtual environment detected: ${VIRTUAL_ENV}"
fi

# 2. Upgrade pip and build tools
echo "[2/4] Ensuring pip and packaging tools are up to date..."
pip install --upgrade pip setuptools wheel

# 3. Install dependencies from requirements.txt
echo "[3/4] Installing dependencies (Kokoro TTS, Suno Bark, PyTorch, SoundFile)..."
pip install -r "${REPO_ROOT}/requirements.txt"

# 4. Initialize Database
echo "[4/4] Syncing SQLite database from data/corpus.json..."
python "${REPO_ROOT}/scripts/init_db.py"

echo ""
echo "======================================================"
echo " Setup complete!"
echo "======================================================"
echo "To activate manually:"
echo "  source .venv/bin/activate"
echo ""
echo "Available scripts:"
echo "  - Generate Kokoro A-Z audio : python scripts/generate_all_audio.py"
echo "  - Generate Bark A-D speech  : python scripts/generate_bark_narration.py"
echo "  - Start local web player    : python -m http.server 8000"
echo "======================================================"
