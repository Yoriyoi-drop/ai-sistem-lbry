#!/usr/bin/env python3
"""Prepare a training dataset from collected feedback.

Reads `data/feedback.jsonl` and writes `data/train.jsonl` with simple
instruction/response pairs suitable for fine-tuning or LoRA training.
"""
import json
from pathlib import Path


def main():
    data_dir = Path("data")
    feedback_file = data_dir / "feedback.jsonl"
    out_file = data_dir / "train.jsonl"

    # If no local feedback file, attempt to read from Redis list (if available)
    if not feedback_file.exists():
        try:
            import redis, os
            REDIS_FEEDBACK_KEY = os.getenv("REDIS_FEEDBACK_KEY", "infinite:feedback")
            r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)), db=0, decode_responses=True)
            items = r.lrange(REDIS_FEEDBACK_KEY, 0, -1)
            if items:
                data_dir.mkdir(parents=True, exist_ok=True)
                with feedback_file.open("w", encoding="utf-8") as f:
                    for it in items:
                        f.write(it + "\n")
                print(f"Pulled {len(items)} feedback items from Redis into {feedback_file}")
        except Exception:
            pass

    if not feedback_file.exists():
        print("No feedback file found, nothing to do.")
        return

    examples = []
    for line in feedback_file.read_text(encoding="utf-8").splitlines():
        try:
            obj = json.loads(line)
        except Exception:
            continue

        # Prefer corrected_response; fallback to model_response
        response = obj.get("corrected_response") or obj.get("model_response")
        if not response or not obj.get("message"):
            continue

        # Simple format: {"instruction": ..., "output": ...}
        examples.append({
            "instruction": obj.get("message"),
            "output": response,
        })

    if not examples:
        print("No usable examples found.")
        return

    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"Wrote {len(examples)} training examples to {out_file}")


if __name__ == "__main__":
    main()
