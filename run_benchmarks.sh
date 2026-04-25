#!/bin/bash

set -e

HUNNU_PATH="${HUNNU_PATH:-./build/hunnu}"
BENCHMARKS_DIR="${BENCHMARKS_DIR:-./benchmarks}"
RESULTS_DIR="${RESULTS_DIR:-./results}"
RUNS="${RUNS:-5}"

mkdir -p "$RESULTS_DIR"

run_benchmark() {
    local name="$1"
    local file="$BENCHMARKS_DIR/${name}.hn"
    
    if [ ! -f "$file" ]; then
        echo "Benchmark not found: $file"
        return 1
    fi
    
    echo "Running: $name"
    "$HUNNU_PATH" "$file"
}

show_help() {
    cat << EOF
Hunnu-lang Benchmark Runner

Usage: $0 [COMMAND] [OPTIONS]

Commands:
    all         Run all benchmarks
    test        Run a specific benchmark by name
    list        List available benchmarks
    help        Show this help message

Options:
    --hunnu PATH       Path to hunnu binary (default: ./build/hunnu)
    --runs N           Number of runs per benchmark (default: 5)
    --json             Save results as JSON
    --test NAME        Run a specific benchmark

Examples:
    $0 all
    $0 test loop --runs 10
    $0 all --hunnu ./build/hunnu --json
EOF
}

list_benchmarks() {
    echo "Available benchmarks:"
    for f in "$BENCHMARKS_DIR"/*.hn; do
        if [ -f "$f" ]; then
            basename "$f" .hn
        fi
    done
}

cmd="${1:-all}"
shift || true

case "$cmd" in
    all)
        python3 benchmark.py "$@"
        ;;
    test)
        name="${1:-}"
        if [ -z "$name" ]; then
            echo "Error: Benchmark name required"
            echo "Usage: $0 test <benchmark_name>"
            exit 1
        fi
        python3 benchmark.py --test "$name" "$@"
        ;;
    list)
        list_benchmarks
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $cmd"
        show_help
        exit 1
        ;;
esac