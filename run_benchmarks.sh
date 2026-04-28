#!/bin/bash

set -e

HUNNU_PATH="${HUNNU_PATH:-./hunnu/build/hunnu}"
BENCHMARKS_DIR="${BENCHMARKS_DIR:-./benchmarks}"
RESULTS_DIR="${RESULTS_DIR:-./results}"
RUNS="${RUNS:-5}"
USE_VM=""

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
    --hunnu PATH       Path to hunnu binary (default: ./hunnu/build/hunnu)
    --runs N           Number of runs per benchmark (default: 5)
    --json             Save results as JSON
    --vm               Use VM mode instead of interpreter
    --test NAME        Run a specific benchmark

Environment Variables:
    HUNNU_PATH         Path to hunnu binary
    BENCHMARKS_DIR     Benchmark directory
    RESULTS_DIR        Results output directory
    RUNS               Number of runs per benchmark

Examples:
    $0 all
    $0 test loop --runs 10
    $0 all --hunnu ./build/hunnu --json
    $0 all --vm
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

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --hunnu)
                HUNNU_PATH="$2"
                shift 2
                ;;
            --runs)
                RUNS="$2"
                shift 2
                ;;
            --json)
                JSON_FLAG="--json"
                shift
                ;;
            --vm)
                USE_VM="--vm"
                shift
                ;;
            *)
                break
                ;;
        esac
    done
}

cmd="${1:-all}"
shift || true

parse_args "$@"

case "$cmd" in
    all)
        python3 benchmark.py --hunnu "$HUNNU_PATH" --runs "$RUNS" $JSON_FLAG $USE_VM
        ;;
    test)
        name="${1:-}"
        if [ -z "$name" ]; then
            echo "Error: Benchmark name required"
            echo "Usage: $0 test <benchmark_name>"
            exit 1
        fi
        shift
        parse_args "$@"
        python3 benchmark.py --hunnu "$HUNNU_PATH" --test "$name" --runs "$RUNS" $USE_VM
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
