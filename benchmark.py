#!/usr/bin/env python3
"""Benchmark runner for hunnu-lang."""

import subprocess
import time
import json
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class BenchmarkResult:
    name: str
    runs: list[float]
    mean: float = 0.0
    std_dev: float = 0.0
    min_time: float = 0.0
    max_time: float = 0.0
    success: bool = True
    error: Optional[str] = None

    def __post_init__(self):
        if self.runs:
            self.mean = statistics.mean(self.runs)
            self.min_time = min(self.runs)
            self.max_time = max(self.runs)
            if len(self.runs) > 1:
                self.std_dev = statistics.stdev(self.runs)


@dataclass
class BenchmarkConfig:
    hunnu_path: str = "./build/hunnu"
    benchmarks_dir: str = "./benchmarks"
    results_dir: str = "./results"
    default_runs: int = 5
    timeout: int = 60


def run_hunnu(
    hunnu_path: str, program_path: str, timeout: int = 60
) -> tuple[float, bool, str]:
    start = time.perf_counter()
    try:
        result = subprocess.run(
            [hunnu_path, program_path], capture_output=True, text=True, timeout=timeout
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
            runs=[],
            success=False,
            error=f"Benchmark file not found: {benchmark_path}",
        )

    timings = []
    success = True
    error_msg = ""

    for _ in range(runs):
        elapsed, success_flag, error = run_hunnu(
            config.hunnu_path, str(benchmark_path), config.timeout
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

    benchmark_files = sorted(Path(config.benchmarks_dir).glob("*.hn"))
    results = []

    print(f"Running hunnu-lang benchmarks")
    print(f"Binary: {config.hunnu_path}")
    print(f"Benchmarks: {len(benchmark_files)}")
    print(f"Runs per benchmark: {runs or config.default_runs}")
    print("-" * 60)

    for benchmark_file in benchmark_files:
        name = benchmark_file.stem
        result = run_benchmark(config, name, runs)
        results.append(result)

        if result.success:
            print(
                f"{name:20s} | mean: {result.mean * 1000:8.2f}ms | std: {result.std_dev * 1000:6.2f}ms"
            )
        else:
            print(f"{name:20s} | FAILED: {result.error}")

    print("-" * 60)

    if output_json:
        json_path = results_dir / f"benchmark_{int(time.time())}.json"
        with open(json_path, "w") as f:
            json.dump(
                {
                    "timestamp": time.time(),
                    "config": {
                        "hunnu_path": config.hunnu_path,
                        "runs": runs or config.default_runs,
                    },
                    "results": [
                        {
                            "name": r.name,
                            "mean_ms": r.mean * 1000,
                            "std_dev_ms": r.std_dev * 1000,
                            "min_ms": r.min_time * 1000,
                            "max_ms": r.max_time * 1000,
                            "success": r.success,
                            "error": r.error,
                        }
                        for r in results
                    ],
                },
                f,
                indent=2,
            )
        print(f"\nResults saved to: {json_path}")

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Hunnu-lang Benchmark Runner")
    parser.add_argument(
        "--hunnu",
        "-p",
        default="./build/hunnu",
        help="Path to hunnu binary (default: ./build/hunnu)",
    )
    parser.add_argument(
        "--benchmarks",
        "-d",
        default="./benchmarks",
        help="Benchmark directory (default: ./benchmarks)",
    )
    parser.add_argument("--runs", "-n", type=int, help="Number of runs per benchmark")
    parser.add_argument("--test", "-t", help="Run a single benchmark by name")
    parser.add_argument(
        "--json", "-j", action="store_true", help="Save results as JSON"
    )
    parser.add_argument(
        "--timeout", default=60, type=int, help="Timeout in seconds (default: 60)"
    )

    args = parser.parse_args()

    config = BenchmarkConfig(
        hunnu_path=args.hunnu,
        benchmarks_dir=args.benchmarks,
        default_runs=args.runs or 5,
        timeout=args.timeout,
    )

    if args.test:
        result = run_benchmark(config, args.test, args.runs)
        if result.success:
            print(
                f"{result.name}: {result.mean * 1000:.2f}ms (std: {result.std_dev * 1000:.2f}ms)"
            )
        else:
            print(f"{result.name}: FAILED - {result.error}")
    else:
        run_all_benchmarks(config, args.runs, args.json)


if __name__ == "__main__":
    main()
