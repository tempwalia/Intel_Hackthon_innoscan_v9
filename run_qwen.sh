#!/bin/bash
# Run Qwen model with warnings suppressed

export TOKENIZERS_PARALLELISM=false
export PYTHONWARNINGS="ignore::DeprecationWarning"

cd "$(dirname "$0")"
source .venv/bin/activate
python brd_gen/qwen.py "$@"
