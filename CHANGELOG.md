# Changelog

All notable changes to the hunnu-benchmark project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-05-15

### Added
- Warmup runs before measurement (`--warmup` / `-w`, default: 2)
- Percentile statistics: median (p50), p95, p99 in output and JSON export
- `--compare` mode: runs all benchmarks in both interpreter and VM, shows speedup ratio
- `--vm-rust` flag for Rust VM mode
- `scripts/compare_results.py` for comparing two JSON result files
- `tests/test_benchmark_runner.py` with unit tests for runner utilities
- `.gitignore` with sensible defaults

### Changed
- **Major refactor** of `benchmark.py`: warmup runs, percentile stats, cleaner output with progress bar
- Refactored `run_benchmarks.sh`: fixed duplicate parse_args bug, cleaner argument handling, added compare/vm-rust/warmup support
- Improved `setup.sh`: uses `git submodule update --init` instead of manual clone, parallel build with `-j`
- Updated `package.json` to v1.2.0 with new scripts: `bench:vm-rust`, `bench:compare`
- Removed stale `.gitkeep` files from empty directories

### Fixed
- Array memory leak in hunnu-lang's `value_free()` — now properly frees individual array elements
- Shell script test command no longer double-parses arguments

## [1.1.0] - 2026-04-27

### Added
- `array.hn` benchmark for array access and iteration
- `string.hn` benchmark for string concatenation and length
- `compound_assign.hn` for compound assignment operators (+=, -=, *=, /=)
- `else_if.hn` for else-if conditional chains
- `float_math.hn` for floating-point arithmetic operations
- `null_check.hn` for null value handling and checks
- `type_conv.hn` for type conversion functions (to_str, to_int)
- Support for VM mode with `--vm` flag
- Binary validation before running benchmarks
- JSON export with `--json` flag

### Changed
- Updated benchmark.py with improved error handling
- Enhanced output format with min/max times and std deviation
- Added `use_vm` option to BenchmarkConfig

## [1.0.0] - 2026-04-25

### Added
- Initial benchmark suite for hunnu-lang
- Core benchmarks: `loop.hn`, `fibonacci.hn`, `recursion.hn`, `arithmetic.hn`, `sieve.hn`, `sort.hn`
- Python-based benchmark runner (`benchmark.py`)
- Shell script runner (`run_benchmarks.sh`)
- npm scripts for easy execution
- Statistical analysis with mean, std deviation, min, max times
- JSON export functionality
- AGENTS.md with agent guidelines

[Unreleased]: https://github.com/hunnu-labs/hunnu-benchmark/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/hunnu-labs/hunnu-benchmark/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/hunnu-labs/hunnu-benchmark/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/hunnu-labs/hunnu-benchmark/releases/tag/v1.0.0
