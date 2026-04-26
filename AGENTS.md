# Agent Guidelines for hunnu-benchmark

## Overview
This repository contains benchmark code for [hunnu-lang](https://github.com/hunnu-labs/hunnu-lang), a lightweight programming language written in C. The benchmark project tests and measures hunnu-lang's performance.

---

## Hunnu-Lang Reference

Hunnu is a C-based programming language with these features:
- **Variables**: `let x = 10`
- **Functions**: `fn add(a, b) { return a + b }`
- **Control Flow**: `if`, `while`, `for` loops, `break`, `continue`
- **Arrays**: `let arr = [1, 2, 3]`, `arr[0]`
- **Strings**: `"a" + "b"`, `len(s)`
- **Printing**: `print("Hello")`

### Running Hunnu Programs
```bash
./build/hunnu run examples/main.hn
# or shorter:
./build/hunnu examples/main.hn
```

---

## Build, Lint, and Test Commands

### Building Hunnu (from hunnu-lang repo)
```bash
# First time setup
git clone https://github.com/hunnu-labs/hunnu-lang.git hunnu
cd hunnu && mkdir -p build && cd build
cmake ..
make
# Binary at: hunnu/build/hunnu
```

### Running Benchmark Tests
```bash
# Python runner
python3 benchmark.py
python3 benchmark.py --runs 10
python3 benchmark.py --test loop
python3 benchmark.py --json

# Shell script
./run_benchmarks.sh all
./run_benchmarks.sh test fibonacci --runs 5

# npm
npm test
npm run test:loop
npm run bench
```

### Linting
```bash
npm run lint
# or
npx eslint .
# or
ruff check .
# or (C)
make lint  # if custom target exists
```

### Type Checking
```bash
npm run typecheck
# or
npx tsc --noEmit
# or
mypy .
```

### Formatting
```bash
npm run format
# or
npx prettier --write .
# or
ruff format .
# or (C)
clang-format -i src/*.c
```

---

## Code Style Guidelines

### General Principles
- Write clear, self-documenting code with descriptive names
- Keep functions small and focused (single responsibility)
- Prefer composition over inheritance
- Avoid premature optimization
- Handle errors explicitly and gracefully

### C Conventions (for hunnu-lang runtime)
- Use 4 spaces for indentation (no tabs)
- Max line length: 100 characters
- Opening brace on same line as function/if/while
- Use `const` whenever possible
- Prefer `static` for internal functions
- Comment "why", not "what"

### Includes (C)
Order: 1) Project headers, 2) Standard library, 3) System headers

```c
#include "lexer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
```

### Python Conventions
- Follow PEP 8
- Use type hints for function signatures
- Prefer `async/await` over raw coroutines
- Use `dataclasses` or `pydantic` for structured data

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `current_token` |
| Constants | UPPER_SNAKE_CASE | `MAX_TOKEN_LENGTH` |
| Functions | snake_case | `parse_expression` |
| Types/Structs | PascalCase | `Lexer` |
| Enums (values) | UPPER_SNAKE_CASE | `TOKEN_LET` |
| Files | snake_case | `lexer.c` / `lexer.h` |
| Macros | UPPER_SNAKE_CASE | `#define MAX_DEPTH 100` |

### C Types
- Use fixed-width integers from `<stdint.h>`: `int32_t`, `int64_t`, `uint32_t`
- Use `size_t` for sizes and indices
- Use `int` for boolean return types (0 = false, non-zero = true)
- Always initialize pointers to `NULL`
- Check for `NULL` before dereferencing

---

## Error Handling

### C
- Return error codes (0 for success, negative for errors)
- Use `fprintf(stderr, ...)` for error messages
- Never silently ignore return values
- Clean up resources on error (free memory, close files)

### Python
```python
try:
    result = process_data(input)
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    raise UserError("Invalid input") from e
except Exception as e:
    logger.exception("Unexpected error")
    raise InternalError("Processing failed") from e
```

---

## Testing Guidelines

### Benchmark Structure
- Use descriptive test names that explain the expected behavior
- Follow Arrange-Act-Assert pattern
- Keep tests isolated; avoid shared state
- Test edge cases and error conditions
- Measure and report execution time accurately

### C Test Example (if applicable)
```c
void test_lexer_tokenization() {
    const char* input = "let x = 10";
    Lexer lexer;
    lexer_init(&lexer, input);
    
    Token token = lexer_next_token(&lexer);
    assert(token.type == TOKEN_LET);
    
    lexer_free(&lexer);
}
```

### Python Benchmark Example
```python
def benchmark_hunnu_execution():
    """Benchmark hunnu-lang program execution."""
    # Arrange
    program = "examples/loop.hn"
    
    # Act
    start = time.perf_counter()
    result = run_hunnu(program)
    elapsed = time.perf_counter() - start
    
    # Assert
    assert result.returncode == 0
    assert elapsed < MAX_EXPECTED_TIME
```

---

## Project Structure

```
hunnu-benchmark/
├── benchmarks/           # Benchmark programs (.hn files)
├── scripts/              # Benchmark runner scripts
├── results/               # Benchmark output results
├── hunnu/                 # Hunnu language implementation (submodule?)
├── build/                 # Build output
└── AGENTS.md             # This file
```

---

## Security Best Practices

- Never commit secrets, API keys, or credentials
- Use environment variables for configuration
- Validate and sanitize all user input
- Use parameterized queries to prevent injection
- Follow principle of least privilege

---

## Git Workflow

- Write clear, concise commit messages (conventional commits preferred)
- Keep commits focused and atomic
- Create descriptive PR titles and descriptions
- Address all review comments before merging
- Never force push to main branch

---

## Notes for Agents

- Always build and test after changes
- Keep changes small and focused
- Update benchmark examples to demonstrate new features
- Update this file when project setup changes
- Reference hunnu-lang AGENTS.md for language-specific guidelines