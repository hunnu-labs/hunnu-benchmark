#!/usr/bin/env python3
"""Benchmark runner for hunnu-lang."""

__version__ = "1.2.0"

import os
import subprocess
import time
import json
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class BenchmarkResult:
    name: str
    runs: list[float] = field(default_factory=list)
    mean: float = 0.0
    std_dev: float = 0.0
    median: float = 0.0
    p95: float = 0.0
    p99: float = 0.0
    min_time: float = 0.0
    max_time: float = 0.0
    success: bool = True
    error: Optional[str] = None

    def __post_init__(self):
        if self.runs:
            s = sorted(self.runs)
            n = len(s)
            self.mean = statistics.mean(s)
            self.min_time = s[0]
            self.max_time = s[-1]
            self.median = _percentile(s, 50)
            self.p95 = _percentile(s, 95)
            self.p99 = _percentile(s, 99)
            if n > 1:
                self.std_dev = statistics.stdev(s)


def _percentile(sorted_data: list[float], p: int) -> float:
    if not sorted_data:
        return 0.0
    k = (len(sorted_data) - 1) * p / 100.0
    f = int(k)
    c = f + 1
    if c >= len(sorted_data):
        return sorted_data[-1]
    return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])


@dataclass
class BenchmarkConfig:
    hunnu_path: str = "./hunnu/build/hunnu"
    benchmarks_dir: str = "./benchmarks"
    results_dir: str = "./results"
    default_runs: int = 5
    warmup_runs: int = 2
    timeout: int = 60
    mode: str = "interpreter"


def validate_hunnu_binary(hunnu_path: str) -> tuple[bool, str]:
    path = Path(hunnu_path)
    if not path.exists():
        return False, f"Binary not found: {hunnu_path}"
    if not path.is_file():
        return False, f"Not a file: {hunnu_path}"
    if not os.access(str(path), os.X_OK):
        return False, f"Binary not executable: {hunnu_path}"
    return True, ""


def detect_hunnu_version(hunnu_path: str) -> str:
    try:
        result = subprocess.run(
            [hunnu_path, "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "unknown"


def run_hunnu(
    hunnu_path: str, program_path: str, timeout: int = 60, mode: str = "interpreter"
) -> tuple[float, bool, str]:
    cmd = [hunnu_path, "run", program_path]
    if mode == "vm":
        cmd.insert(2, "--vm")
    elif mode == "vm-rust":
        cmd.insert(2, "--vm-rust")

    start = time.perf_counter()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.perf_counter() - start
        success = result.returncode == 0
        error = result.stderr if not success else ""
        return elapsed, success, error
    except subprocess.TimeoutExpired:
        return time.perf_counter() - start, False, "Timeout exceeded"
    except FileNotFoundError:
        return 0.0, False, f"Hunnu binary not found: {hunnu_path}"
    except Exception as e:
        return 0.0, False, str(e)


def run_benchmark(
    config: BenchmarkConfig, benchmark_name: str, runs: Optional[int] = None
) -> BenchmarkResult:
    benchmark_path = Path(config.benchmarks_dir) / f"{benchmark_name}.hn"
    runs = runs or config.default_runs

    if not benchmark_path.exists():
        return BenchmarkResult(
            name=benchmark_name,
            success=False,
            error=f"Benchmark file not found: {benchmark_path}",
        )

    if config.warmup_runs > 0:
        for _ in range(config.warmup_runs):
            _, success_flag, error = run_hunnu(
                config.hunnu_path, str(benchmark_path), config.timeout, config.mode
            )
            if not success_flag:
                return BenchmarkResult(
                    name=benchmark_name,
                    success=False,
                    error=f"Warmup failed: {error}",
                )

    timings = []
    success = True
    error_msg = ""

    for r in range(runs):
        elapsed, success_flag, error = run_hunnu(
            config.hunnu_path, str(benchmark_path), config.timeout, config.mode
        )
        if not success_flag:
            success = False
            error_msg = error
            break
        timings.append(elapsed)

    return BenchmarkResult(
        name=benchmark_name,
        runs=timings,
        success=success,
        error=error_msg if not success else None,
    )


def run_all_benchmarks(
    config: Optional[BenchmarkConfig] = None,
    runs: Optional[int] = None,
    output_json: bool = False,
) -> list[BenchmarkResult]:
    config = config or BenchmarkConfig()
    results_dir = Path(config.results_dir)
    results_dir.mkdir(exist_ok=True)

    valid, msg = validate_hunnu_binary(config.hunnu_path)
    if not valid:
        print(f"Error: {msg}")
        print("Please build hunnu-lang or set --hunnu flag correctly.")
        return []

    version = detect_hunnu_version(config.hunnu_path)
    benchmark_files = sorted(Path(config.benchmarks_dir).glob("*.hn"))
    if not benchmark_files:
        print(f"No benchmarks found in {config.benchmarks_dir}")
        return []

    mode_label = {"interpreter": "Interpreter", "vm": "Bytecode VM", "vm-rust": "Rust VM"}
    print(f"hunnu-benchmark v{__version__}  |  mode: {mode_label.get(config.mode, config.mode)}")
    print(f"binary: {config.hunnu_path}  |  {version}")
    print(f"benchmarks: {len(benchmark_files)}  |  warmup: {config.warmup_runs}  |  runs: {runs or config.default_runs}")
    print()

    results = []
    pad = max((f.stem for f in benchmark_files), key=len)
    width = max(len(pad), 16)

    for benchmark_file in benchmark_files:
        name = benchmark_file.stem
        result = run_benchmark(config, name, runs)
        results.append(result)

        if result.success:
            print(
                f"  {name:<{width}s}  "
                f"mean {result.mean * 1000:>8.2f}ms  "
                f"p50 {result.median * 1000:>8.2f}ms  "
                f"p95 {result.p95 * 1000:>8.2f}ms  "
                f"std {result.std_dev * 1000:>6.2f}ms  "
                f"({len(result.runs)} runs)"
            )
        else:
            print(f"  {name:<{width}s}  FAILED: {result.error}")

    print()
    success_count = sum(1 for r in results if r.success)
    total = len(results)
    bar = "█" * success_count + "░" * (total - success_count)
    print(f"  [{bar}] {success_count}/{total} passed")

    if output_json:
        timestamp = int(time.time())
        json_path = results_dir / f"benchmark_{timestamp}.json"
        with open(json_path, "w") as f:
            json.dump({
                "meta": {
                    "timestamp": timestamp,
                    "version": __version__,
                    "hunnu_version": version,
                    "config": {
                        "hunnu_path": config.hunnu_path,
                        "runs": runs or config.default_runs,
                        "warmup": config.warmup_runs,
                        "mode": config.mode,
                    },
                },
                "results": [
                    {
                        "name": r.name,
                        "mean_ms": round(r.mean * 1000, 3),
                        "median_ms": round(r.median * 1000, 3),
                        "std_dev_ms": round(r.std_dev * 1000, 3),
                        "p95_ms": round(r.p95 * 1000, 3),
                        "p99_ms": round(r.p99 * 1000, 3),
                        "min_ms": round(r.min_time * 1000, 3),
                        "max_ms": round(r.max_time * 1000, 3),
                        "runs": [round(t * 1000, 3) for t in r.runs],
                        "success": r.success,
                        "error": r.error,
                    }
                    for r in results
                ],
            }, f, indent=2)
        print(f"  results saved: {json_path}")

    return results


def cmd_compare(config: BenchmarkConfig, runs: Optional[int] = None, output_json: bool = False):
    """Run benchmarks in interpreter and VM modes, then compare."""
    modes = ["interpreter", "vm"]
    all_results = {}

    for mode in modes:
        print(f"\n{'='*60}")
        print(f"  Mode: {mode}")
        print(f"{'='*60}")
        cfg = BenchmarkConfig(
            hunnu_path=config.hunnu_path,
            benchmarks_dir=config.benchmarks_dir,
            results_dir=config.results_dir,
            default_runs=runs or config.default_runs,
            warmup_runs=config.warmup_runs,
            timeout=config.timeout,
            mode=mode,
        )
        all_results[mode] = run_all_benchmarks(cfg, runs, output_json=False)

    print(f"\n{'='*60}")
    print("  Comparison: Interpreter vs Bytecode VM")
    print(f"{'='*60}")
    pad = max((r.name for r in all_results["interpreter"]), key=len) if all_results["interpreter"] else "benchmark"
    width = max(len(pad), 16)

    for ir, vr in zip(all_results["interpreter"], all_results["vm"]):
        if ir.success and vr.success:
            ratio = vr.mean / ir.mean if ir.mean > 0 else 0
            arrow = "↑" if ratio > 1 else "↓"
            print(
                f"  {ir.name:<{width}s}  "
                f"int {ir.mean * 1000:>8.2f}ms  "
                f"vm  {vr.mean * 1000:>8.2f}ms  "
                f"{arrow} {ratio:.2f}x"
            )
        elif not ir.success:
            print(f"  {ir.name:<{width}s}  int FAILED: {ir.error}")
        else:
            print(f"  {ir.name:<{width}s}  vm  FAILED: {vr.error}")

    if output_json:
        timestamp = int(time.time())
        json_path = Path(config.results_dir) / f"compare_{timestamp}.json"
        json_path.parent.mkdir(exist_ok=True)
        with open(json_path, "w") as f:
            json.dump({
                "meta": {"timestamp": timestamp, "version": __version__},
                "comparison": [
                    {
                        "name": ir.name,
                        "interpreter_ms": round(ir.mean * 1000, 3),
                        "vm_ms": round(vr.mean * 1000, 3),
                        "ratio": round(vr.mean / ir.mean, 4) if ir.success and vr.mean > 0 else None,
                        "interpreter_success": ir.success,
                        "vm_success": vr.success,
                    }
                    for ir, vr in zip(all_results["interpreter"], all_results["vm"])
                ],
            }, f, indent=2)
        print(f"\n  comparison saved: {json_path}")

    return all_results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Hunnu-lang Benchmark Runner")
    parser.add_argument("--hunnu", "-p", default="./hunnu/build/hunnu", help="Path to hunnu binary")
    parser.add_argument("--benchmarks", "-d", default="./benchmarks", help="Benchmark directory")
    parser.add_argument("--runs", "-n", type=int, help="Number of runs per benchmark")
    parser.add_argument("--warmup", "-w", type=int, default=2, help="Warmup runs before measurement")
    parser.add_argument("--test", "-t", help="Run a single benchmark by name")
    parser.add_argument("--json", "-j", action="store_true", help="Save results as JSON")
    parser.add_argument("--timeout", default=60, type=int, help="Timeout in seconds")
    parser.add_argument("--vm", action="store_true", help="Use bytecode VM")
    parser.add_argument("--vm-rust", action="store_true", help="Use Rust VM")
    parser.add_argument("--compare", action="store_true", help="Compare interpreter vs VM modes")
    parser.add_argument("--version", "-v", action="version", version=f"hunnu-benchmark {__version__}")

    args = parser.parse_args()

    mode = "interpreter"
    if args.vm_rust:
        mode = "vm-rust"
    elif args.vm:
        mode = "vm"

    config = BenchmarkConfig(
        hunnu_path=args.hunnu,
        benchmarks_dir=args.benchmarks,
        default_runs=args.runs or 5,
        warmup_runs=args.warmup,
        timeout=args.timeout,
        mode=mode,
    )

    valid, msg = validate_hunnu_binary(config.hunnu_path)
    if not valid:
        print(f"Error: {msg}")
        sys.exit(1)

    if args.compare:
        cmd_compare(config, args.runs, args.json)
    elif args.test:
        result = run_benchmark(config, args.test, args.runs)
        if result.success:
            print(
                f"{result.name}: "
                f"mean {result.mean * 1000:.2f}ms  "
                f"median {result.median * 1000:.2f}ms  "
                f"p95 {result.p95 * 1000:.2f}ms  "
                f"std {result.std_dev * 1000:.2f}ms  "
                f"({len(result.runs)} runs)"
            )
        else:
            print(f"{result.name}: FAILED - {result.error}")
            sys.exit(1)
    else:
        run_all_benchmarks(config, args.runs, args.json)


if __name__ == "__main__":
    main()
