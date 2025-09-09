#!/usr/bin/env python3
"""
Preview check: Summarize a journey schema for quick console review.

Usage:
  python scripts/preview_schema.py --journey non-lux-lp-demo
"""

import argparse
from pathlib import Path
import yaml
from collections import Counter


def load_schema(journey: str):
    p = Path(f"data/schemas/{journey}/schema.yaml")
    if not p.exists():
        raise SystemExit(f"Schema not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    ap = argparse.ArgumentParser(description="Preview a journey schema")
    ap.add_argument("--journey", required=True)
    args = ap.parse_args()

    schema = load_schema(args.journey)
    items = schema.get("items", [])
    total = len(items)

    controls = Counter((it.get("control") or "").lower() for it in items)
    datatypes = Counter((it.get("data_type") or "").lower() for it in items)
    required = sum(1 for it in items if it.get("mandatory"))
    with_visibility = [it for it in items if (it.get("visibility", {}).get("all") or [])]

    print(f"Journey: {schema.get('key')} – {schema.get('name')} v{schema.get('version')}")
    print(f"Items: {total} (required: {required})")
    print("Control types:")
    for k, v in controls.most_common():
        print(f"  - {k}: {v}")
    print("Data types:")
    for k, v in datatypes.most_common():
        print(f"  - {k}: {v}")
    print(f"Fields with visibility rules: {len(with_visibility)}")
    print("Sample visibility rules (first 10):")
    for it in with_visibility[:10]:
        rules = it.get("visibility", {}).get("all") or []
        print(f"  - {it.get('id')}: {rules}")


if __name__ == "__main__":
    main()

