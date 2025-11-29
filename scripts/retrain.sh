#!/usr/bin/env bash
set -euo pipefail


# Simple retrain driver: prepare dataset and run LoRA finetune
PROJECT_PYTHON="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/.venv/bin/python"
# Prefer user-provided $PYTHON, then active virtualenv, then project venv, then system python3
if [ -n "${PYTHON:-}" ]; then
	PYTHON="$PYTHON"
elif [ -n "${VIRTUAL_ENV:-}" ] && [ -x "${VIRTUAL_ENV}/bin/python" ]; then
	PYTHON="${VIRTUAL_ENV}/bin/python"
elif [ -x "$PROJECT_PYTHON" ]; then
	PYTHON="$PROJECT_PYTHON"
else
	PYTHON=python3
fi

echo "Preparing dataset..."
"$PYTHON" scripts/prepare_dataset.py

echo "Starting finetune (LoRA)..."
"$PYTHON" scripts/finetune_lora.py

echo "Retrain finished."
