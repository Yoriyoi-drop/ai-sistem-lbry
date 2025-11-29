Continuous learning / Retrain notes

This repository includes a minimal continuous-learning scaffold:

- `/feedback` endpoint in `main.py` that appends JSON records to `data/feedback.jsonl`.
- `scripts/prepare_dataset.py` converts feedback into `data/train.jsonl`.
- `scripts/finetune_lora.py` demonstrates a minimal LoRA finetune using `peft` and `transformers`.
- `scripts/retrain.sh` runs prepare + finetune; `.github/workflows/retrain.yml` schedules a nightly job.

How to run locally (dev)

```bash
# Gather feedback via API or add entries to data/feedback.jsonl
python scripts/prepare_dataset.py
python scripts/finetune_lora.py
```

Notes & safety
- The finetune script is an example and assumes you have sufficient compute (GPU recommended) and packages installed.
- Always validate model performance before deploying updated models to production.
- Use human review / evaluation sets to gate promotion of new models.
