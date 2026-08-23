from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT / "data" / "social_impact_eval_dataset.json"
RESULTS_DIR = ROOT / "results"


def load_examples(path: Path = DATASET_PATH) -> list[dict[str, Any]]:
    """Load the versioned evaluation examples from disk."""
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload["examples"]


def write_json(path: Path, payload: Any) -> None:
    """Write deterministic, human-readable JSON output."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")

