"""Basic tests for the benchmark runner itself."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from benchmark import _percentile, BenchmarkResult, validate_hunnu_binary


def test_percentile_empty():
    assert _percentile([], 50) == 0.0


def test_percentile_single():
    assert _percentile([10.0], 50) == 10.0
    assert _percentile([10.0], 95) == 10.0


def test_percentile_values():
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    assert _percentile(data, 50) == 5.5
    assert _percentile(data, 0) == 1.0
    assert _percentile(data, 100) == 10.0


def test_benchmark_result_stats():
    r = BenchmarkResult(name="test", runs=[1.0, 2.0, 3.0, 4.0, 5.0])
    assert r.mean == 3.0
    assert r.min_time == 1.0
    assert r.max_time == 5.0
    assert r.median == 3.0


def test_benchmark_result_failure():
    r = BenchmarkResult(name="fail", success=False, error="oops")
    assert not r.success
    assert r.error == "oops"


def test_validate_hunnu_binary_missing():
    valid, msg = validate_hunnu_binary("/nonexistent/hunnu")
    assert not valid
    assert "not found" in msg


if __name__ == "__main__":
    test_percentile_empty()
    test_percentile_single()
    test_percentile_values()
    test_benchmark_result_stats()
    test_benchmark_result_failure()
    test_validate_hunnu_binary_missing()
    print("All tests passed!")
