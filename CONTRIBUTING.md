# Contributing to hunnu-benchmark

Thank you for your interest in contributing!

## Ways to Contribute

1. **Add new benchmarks** - Create new `.hn` files in `benchmarks/`
2. **Improve benchmark runner** - Enhance `benchmark.py`
3. **Fix bugs** - Submit issues and PRs
4. **Documentation** - Improve README and docs

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch

## Adding a New Benchmark

1. Create your benchmark in `benchmarks/name.hn`:

```hunnu
fn main() {
    // Your benchmark code
    // Keep iteration count appropriate for timing
    let result = 0
    for let i = 0; i < 100000; i = i + 1 {
        result = result + i
    }
    print(result)
}
```

2. Test it manually:
```bash
./hunnu/build/hunnu benchmarks/name.hn
```

3. Verify it works correctly with the benchmark runner:
```bash
python3 benchmark.py --test name
```

## Benchmark Guidelines

- Name files descriptively: `algorithm_name.hn`
- Use reasonable iteration counts (aim for 50-500ms runtime)
- Output should be deterministic
- Avoid external I/O operations
- Test edge cases separately

## Code Style

- Follow existing patterns in the codebase
- Use 4 spaces for indentation (Python)
- Add type hints to Python functions
- Keep functions small and focused

## Commit Messages

Use conventional commits:
- `feat: add new benchmark for sorting`
- `fix: correct timeout handling`
- `docs: update README`

## Submitting PRs

1. Update tests if needed
2. Run benchmarks to verify no regressions
3. Describe your changes clearly
4. Link related issues

## Questions?

Open an issue for discussion before starting major changes.