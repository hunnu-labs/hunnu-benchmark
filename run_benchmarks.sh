#!/bin/bash
set -e

HUNNU_PATH="${HUNNU_PATH:-./hunnu/build/hunnu}"
BENCHMARKS_DIR="${BENCHMARKS_DIR:-./benchmarks}"
RESULTS_DIR="${RESULTS_DIR:-./results}"
RUNS="${RUNS:-5}"
WARMUP="${WARMUP:-2}"
JSON_FLAG=""
MODE_FLAG=""

show_help() {
    cat << EOF
Hunnu-lang Benchmark Runner

Usage: $0 [COMMAND] [OPTIONS]

Commands:
    all         Run all benchmarks (default)
    test NAME   Run a specific benchmark
    list        List available benchmarks
    compare     Compare interpreter vs VM modes
    help        Show this help message

Options:
    --hunnu PATH       Path to hunnu binary (default: ./hunnu/build/hunnu)
    --runs N           Number of runs per benchmark (default: 5)
    --warmup N         Warmup runs before measurement (default: 2)
    --json             Save results as JSON
    --vm               Use bytecode VM mode
    --vm-rust          Use Rust VM mode

Environment Variables:
    HUNNU_PATH         Path to hunnu binary
    BENCHMARKS_DIR     Benchmark directory
    RESULTS_DIR        Results output directory
    RUNS               Number of runs per benchmark
    WARMUP             Warmup runs before measurement

Examples:
    $0 all
    $0 test loop --runs 10
    $0 all --hunnu ./build/hunnu --json
    $0 all --vm
    $0 compare --json
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

GLOBAL_ARGS=()

parse_global_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --hunnu) HUNNU_PATH="$2"; shift 2 ;;
            --runs) RUNS="$2"; shift 2 ;;
            --warmup) WARMUP="$2"; shift 2 ;;
            --json) JSON_FLAG="--json"; shift ;;
            --vm) MODE_FLAG="--vm"; shift ;;
            --vm-rust) MODE_FLAG="--vm-rust"; shift ;;
            *) GLOBAL_ARGS+=("$1"); shift ;;
        esac
    done
}

parse_global_args "$@"
set -- "${GLOBAL_ARGS[@]}"

cmd="${1:-all}"
shift || true

python_args=(
    --hunnu "$HUNNU_PATH"
    --runs "$RUNS"
    --warmup "$WARMUP"
)

[ -n "$JSON_FLAG" ] && python_args+=("$JSON_FLAG")
[ -n "$MODE_FLAG" ] && python_args+=("$MODE_FLAG")

case "$cmd" in
    all)
        python3 benchmark.py "${python_args[@]}"
        ;;
    test)
        name="${1:-}"
        if [ -z "$name" ]; then
            echo "Error: Benchmark name required"
            echo "Usage: $0 test <benchmark_name>"
            exit 1
        fi
        python3 benchmark.py "${python_args[@]}" --test "$name"
        ;;
    compare)
        python3 benchmark.py "${python_args[@]}" --compare
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
