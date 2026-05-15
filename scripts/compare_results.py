#!/usr/bin/env python3
"""Compare two benchmark JSON result files."""

import json
import sys
from pathlib import Path


def load_results(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/compare_results.py <file1.json> <file2.json>")
        sys.exit(1)

    a = load_results(sys.argv[1])
    b = load_results(sys.argv[2])

    ra = {r["name"]: r for r in a["results"]}
    rb = {r["name"]: r for r in b["results"]}
    names = sorted(set(ra.keys()) & set(rb.keys()))

    print(f"{'Benchmark':<20s}  {'mean1 (ms)':<10s}  {'mean2 (ms)':<10s}  {'ratio':<8s}")
    print("-" * 52)
    for name in names:
        m1 = ra[name]["mean_ms"]
        m2 = rb[name]["mean_ms"]
        ratio = m2 / m1 if m1 > 0 else float("inf")
        arrow = "↑" if ratio > 1 else "↓"
        print(f"{name:<20s}  {m1:<10.3f}  {m2:<10.3f}  {arrow} {ratio:.4f}x")


if __name__ == "__main__":
    main()
