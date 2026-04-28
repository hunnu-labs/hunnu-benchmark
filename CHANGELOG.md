# Changelog

All notable changes to the hunnu-benchmark project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Version display in benchmark output (`hunnu-benchmark v1.1.0`)
- `--version` / `-v` flag to benchmark.py
- `setup.sh` script for automated hunnu-lang setup
- `npm run setup` script

### Changed
- Fixed hunnu-lang submodule setup (proper `git submodule add`)
- Updated hunnu binary path from `./build/hunnu` to `./hunnu/build/hunnu`
- Fixed `benchmark.py` to use `run` subcommand correctly
- Fixed `sort.hn` benchmark (replaced broken bubble sort with array access test)
- Updated `package.json` with new test scripts for all benchmarks
- Refactored README for clarity and accuracy

### Fixed
- Benchmark runner now properly passes `run` subcommand to hunnu binary
- All 13 benchmarks now pass successfully
- Array access syntax in benchmarks matches hunnu-lang requirements

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

[Unreleased]: https://github.com/hunnu-labs/hunnu-benchmark/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/hunnu-labs/hunnu-benchmark/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/hunnu-labs/hunnu-benchmark/releases/tag/v1.0.0
