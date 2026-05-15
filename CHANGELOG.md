# Changelog

All notable changes to the hunnu-benchmark project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-05-15

### Added
- 4 new benchmarks for advanced hunnu-lang features:
  - `while_loop.hn` for while loop iteration performance
  - `lambda.hn` for lambda/anonymous function call overhead
  - `class_oop.hn` for class instantiation and method dispatch
  - `match.hn` for match expression pattern matching
- npm scripts for all new benchmarks

### Changed
- Updated README benchmark table from 13 to 17 entries
- Added lambda, class, and match syntax to Hunnu Language Features table
- Bumped version to 1.2.0

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
