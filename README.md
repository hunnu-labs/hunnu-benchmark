# hunnu-benchmark

Benchmark suite for [hunnu-lang](https://github.com/hunnu-labs/hunnu-lang), a lightweight programming language written in C.

## Features

- Comprehensive benchmarks for measuring hunnu-lang performance
- Python-based benchmark runner with statistical analysis
- Shell script runner for quick testing
- JSON export for data analysis
- Easy to extend with new benchmarks

## Prerequisites

- [hunnu-lang](https://github.com/hunnu-labs/hunnu-lang) installed and built
- Python 3.7+

## Quick Start

### 1. Clone and Build hunnu-lang

```bash
git clone https://github.com/hunnu-labs/hunnu-lang.git hunnu
cd hunnu
mkdir -p build && cd build
cmake ..
make
```

This will create the `hunnu` binary at `hunnu/build/hunnu`.

### 2. Run All Benchmarks

```bash
python3 benchmark.py
# or
./run_benchmarks.sh all
# or
npm test
```

## Benchmark Programs

| Benchmark | Description |
|-----------|-------------|
| `loop.hn` | For loop iteration with arithmetic accumulation |
| `fibonacci.hn` | Recursive fibonacci sequence (F20) |
| `recursion.hn` | Recursive factorial calculation |
| `arithmetic.hn` | Multiple arithmetic operations in a loop |
| `sieve.hn` | Prime number detection using sieve algorithm |
| `sort.hn` | Sorting algorithm benchmark |

## Usage

### Python Benchmark Runner

```bash
python3 benchmark.py [OPTIONS]
```

**Options:**
- `--hunnu, -p PATH` - Path to hunnu binary (default: `./build/hunnu`)
- `--benchmarks, -d DIR` - Benchmark directory (default: `./benchmarks`)
- `--runs, -n N` - Number of runs per benchmark (default: 5)
- `--test, -t NAME` - Run a single benchmark by name
- `--json, -j` - Save results as JSON
- `--timeout SECONDS` - Timeout in seconds (default: 60)

**Examples:**
```bash
# Run all benchmarks with default settings
python3 benchmark.py

# Run all benchmarks with 10 iterations
python3 benchmark.py --runs 10

# Run a single benchmark
python3 benchmark.py --test loop

# Run with custom hunnu binary path
python3 benchmark.py --hunnu ./hunnu/build/hunnu

# Save results as JSON
python3 benchmark.py --json
```

### Shell Script Runner

```bash
./run_benchmarks.sh [COMMAND] [OPTIONS]
```

**Commands:**
- `all` - Run all benchmarks (default)
- `test NAME` - Run a specific benchmark
- `list` - List available benchmarks
- `help` - Show help message

**Examples:**
```bash
./run_benchmarks.sh all
./run_benchmarks.sh test fibonacci --runs 10
./run_benchmarks.sh list
```

### npm Scripts

```bash
npm test              # Run all benchmarks
npm run bench         # Run via shell script
npm run test:loop     # Run single benchmark
npm run test:all      # Run with 10 iterations + JSON
npm run lint          # Run linter
npm run format        # Format code
```

## Adding New Benchmarks

1. Create a new `.hn` file in the `benchmarks/` directory:

```hunnu
fn main() {
    // Your benchmark code here
    let result = 0
    for let i = 0; i < 1000000; i = i + 1 {
        result = result + i
    }
    print(result)
}
```

2. Run to verify it works:
```bash
./build/hunnu benchmarks/your_benchmark.hn
```

3. The benchmark will be automatically included in future runs.

## Output Format

### Console Output
```
Running hunnu-lang benchmarks
Binary: ./build/hunnu
Benchmarks: 6
Runs per benchmark: 5
------------------------------------------------------------
loop                | mean:    125.43ms | std:     3.21ms
fibonacci           | mean:     89.12ms | std:     2.45ms
recursion           | mean:     45.67ms | std:     1.89ms
arithmetic          | mean:    110.23ms | std:     2.78ms
sieve               | mean:    156.78ms | std:     4.12ms
sort                | mean:    203.45ms | std:     5.34ms
------------------------------------------------------------
```

### JSON Output
```json
{
  "timestamp": 1714089600,
  "config": {
    "hunnu_path": "./build/hunnu",
    "runs": 5
  },
  "results": [
    {
      "name": "loop",
      "mean_ms": 125.43,
      "std_dev_ms": 3.21,
      "min_ms": 122.15,
      "max_ms": 130.22,
      "success": true
    }
  ]
}
```

## Project Structure

```
hunnu-benchmark/
├── benchmarks/           # Hunnu benchmark programs (.hn files)
├── scripts/              # Helper scripts
├── results/              # JSON output results
├── tests/                # Unit tests
├── hunnu/                # hunnu-lang (optional submodule)
├── benchmark.py          # Python benchmark runner
├── run_benchmarks.sh     # Shell script runner
├── package.json          # npm scripts
└── README.md             # This file
```

## License

MIT