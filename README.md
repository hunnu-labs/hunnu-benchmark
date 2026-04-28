# hunnu-benchmark

Benchmark suite for [hunnu-lang](https://github.com/hunnu-labs/hunnu-lang), a lightweight programming language written in C.

## Features

- 13 comprehensive benchmarks for measuring hunnu-lang performance
- Python-based benchmark runner with statistical analysis (mean, std dev, min, max)
- Shell script and npm script runners for quick testing
- JSON export for data analysis
- Support for both interpreter and VM modes
- Automated setup script
- Binary validation before running benchmarks

## Prerequisites

- Python 3.7+
- CMake and C compiler (for building hunnu-lang)
- Git

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
./setup.sh
```

This will initialize the hunnu-lang submodule and build the binary automatically.

### Option 2: Manual Setup

```bash
# Initialize submodule
git submodule update --init --recursive

# Build hunnu-lang
cd hunnu && mkdir -p build && cd build && cmake .. && make
```

### Run Benchmarks

```bash
python3 benchmark.py        # Python runner
./run_benchmarks.sh all     # Shell script
npm test                    # npm script
```

## Benchmark Programs

| Benchmark | Description |
|-----------|-------------|
| `loop.hn` | For loop iteration with arithmetic accumulation |
| `fibonacci.hn` | Recursive fibonacci sequence (F20) |
| `recursion.hn` | Recursive factorial calculation |
| `arithmetic.hn` | Multiple arithmetic operations in a loop |
| `sieve.hn` | Prime number detection using sieve algorithm |
| `sort.hn` | Array access and iteration |
| `array.hn` | Array access and iteration |
| `string.hn` | String concatenation and length |
| `compound_assign.hn` | Compound assignment operators (+=, -=, *=, /=) |
| `else_if.hn` | Else-if conditional chains |
| `float_math.hn` | Floating-point arithmetic operations |
| `null_check.hn` | Null value handling and checks |
| `type_conv.hn` | Type conversion functions (to_str, to_int) |

## Usage

### Python Benchmark Runner

```bash
python3 benchmark.py [OPTIONS]
```

**Options:**
- `--hunnu, -p PATH` - Path to hunnu binary (default: `./hunnu/build/hunnu`)
- `--runs, -n N` - Number of runs per benchmark (default: 5)
- `--test, -t NAME` - Run a single benchmark by name
- `--json, -j` - Save results as JSON
- `--vm` - Run benchmarks using VM instead of interpreter
- `--version, -v` - Show version and exit

**Examples:**
```bash
python3 benchmark.py                          # Run all benchmarks
python3 benchmark.py --runs 10                # Run with 10 iterations
python3 benchmark.py --test loop              # Run single benchmark
python3 benchmark.py --json                   # Save results as JSON
python3 benchmark.py --vm                      # Run using VM mode
python3 benchmark.py --version                 # Show version
```

### Shell Script Runner

```bash
./run_benchmarks.sh [COMMAND] [OPTIONS]
```

**Commands:** `all` (default), `test NAME`, `list`, `help`

**Examples:**
```bash
./run_benchmarks.sh all
./run_benchmarks.sh test fibonacci --runs 10
./run_benchmarks.sh list
```

**Environment Variables:** `HUNNU_PATH`, `BENCHMARKS_DIR`, `RESULTS_DIR`, `RUNS`

### npm Scripts

```bash
npm test                   # Run all benchmarks
npm run bench              # Run via shell script
npm run test:loop          # Run single benchmark
npm run test:all           # Run with 10 iterations + JSON
npm run setup              # Run setup script
npm run lint               # Run linter (ruff check)
npm run format             # Format code (ruff format)
```

## Adding New Benchmarks

1. Create a new `.hn` file in `benchmarks/`:
   ```hunnu
   fn main() {
       let result = 0
       for let i = 0; i < 1000000; i = i + 1 {
           result = result + i
       }
       print(result)
   }
   ```

2. Verify it works:
   ```bash
   ./hunnu/build/hunnu run benchmarks/your_benchmark.hn
   ```

3. The benchmark will be automatically included in future runs.

## Hunnu Language Features

| Feature | Syntax |
|---------|---------|
| Variables | `let x = 10` |
| Functions | `fn add(a, b) { return a + b }` |
| If/Else | `if x > 0 { ... } else { ... }` |
| Else If | `if x > 0 { ... } else if x > 5 { ... }` |
| For loop | `for let i = 0; i < 3; i = i + 1 { ... }` |
| While loop | `while x > 0 { ... }` |
| Break/Continue | `break` / `continue` |
| Compound Assignment | `x += 1`, `x -= 2`, `x *= 3` |
| Arrays | `let arr = [1, 2, 3]`, `arr[0]` |
| Strings | `"a" + "b"`, `len(s)` |
| Floats | `let pi = 3.14159` |
| Null | `let x = null` |
| Type Conversion | `to_int()`, `to_float()`, `to_str()` |

## Output Format

### Console Output
```
hunnu-benchmark v1.1.0 - Running hunnu-lang benchmarks (Interpreter mode)
Binary: ./hunnu/build/hunnu
Benchmarks: 13
Runs per benchmark: 5
------------------------------------------------------------
loop                 | mean:   254.31ms | std:   5.12ms | min:  246.78ms
fibonacci            | mean:     0.56ms | std:   0.04ms | min:    0.51ms
...
------------------------------------------------------------
Summary: 13/13 benchmarks passed
```

### JSON Output
```json
{
  "timestamp": 1714089600,
  "config": {
    "hunnu_path": "./hunnu/build/hunnu",
    "runs": 5,
    "use_vm": false
  },
  "results": [
    {
      "name": "loop",
      "mean_ms": 254.31,
      "std_dev_ms": 5.12,
      "min_ms": 246.78,
      "max_ms": 262.45,
      "success": true
    }
  ]
}
```

## Project Structure

```
hunnu-benchmark/
|-- benchmarks/              # Hunnu benchmark programs (.hn files)
|   |-- loop.hn
|   |-- fibonacci.hn
|   `-- ... (13 total)
|-- results/                 # JSON output results
|-- hunnu/                   # hunnu-lang (git submodule)
|   `-- build/hunnu         # hunnu binary (after build)
|-- benchmark.py             # Python benchmark runner
|-- run_benchmarks.sh        # Shell script runner
|-- setup.sh                 # Automated setup script
|-- package.json             # npm scripts
|-- AGENTS.md                # Agent guidelines
|-- CHANGELOG.md             # Version history
`-- README.md                # This file
```

## Development

```bash
# Install dev dependencies (if needed)
pip install -r requirements-dev.txt 2>/dev/null || echo "No requirements-dev.txt found"

# Lint Python code
npm run lint
# or: ruff check .

# Format Python code
npm run format
# or: ruff format .
```

## License

MIT

---

For version history, see [CHANGELOG.md](CHANGELOG.md).