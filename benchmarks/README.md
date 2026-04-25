# Benchmark Documentation

Each benchmark is designed to test specific aspects of hunnu-lang's performance.

## Available Benchmarks

### loop.hn

**Purpose:** Measure for-loop performance and integer arithmetic

**What it tests:**
- For loop iteration (1,000,000 iterations)
- Integer addition in accumulator
- Loop variable increment

**Expected runtime:** ~100-200ms (varies by hardware)

**Code:**
```hunnu
fn main() {
    let sum = 0
    for let i = 0; i < 1000000; i = i + 1 {
        sum = sum + i
    }
    print(sum)
}
```

---

### fibonacci.hn

**Purpose:** Measure recursive function performance

**What it tests:**
- Recursive function calls
- Multiple return paths
- Stack usage

**Expected runtime:** ~50-100ms

**Code:**
```hunnu
fn fibonacci(n) {
    if n <= 1 {
        return n
    }
    return fibonacci(n - 1) + fibonacci(n - 2)
}

fn main() {
    let result = fibonacci(20)
    print(result)
}
```

---

### recursion.hn

**Purpose:** Measure tail recursion / factorial performance

**What it tests:**
- Recursive multiplication
- Base case handling

**Expected runtime:** ~10-30ms

**Code:**
```hunnu
fn factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

fn main() {
    let result = factorial(10)
    print(result)
}
```

---

### arithmetic.hn

**Purpose:** Measure arithmetic operations performance

**What it tests:**
- Addition, subtraction, multiplication, division
- Operator precedence
- Multiple expressions per iteration

**Expected runtime:** ~80-150ms

**Code:**
```hunnu
fn main() {
    let a = 10
    let b = 20
    let c = 3
    
    for let i = 0; i < 100000; i = i + 1 {
        let result = (a + b) * c - (a - b) / 2
        let more = a * a + b * b + c * c
    }
    print("done")
}
```

---

### sieve.hn

**Purpose:** Measure conditional logic and prime detection

**What it tests:**
- Nested loops
- Modulo operations
- Multiple conditionals

**Expected runtime:** ~100-200ms

**Code:**
```hunnu
fn is_prime(n) {
    if n <= 1 {
        return 0
    }
    if n == 2 {
        return 1
    }
    if n % 2 == 0 {
        return 0
    }
    for let i = 3; i * i <= n; i = i + 2 {
        if n % i == 0 {
            return 0
        }
    }
    return 1
}

fn main() {
    let count = 0
    for let i = 2; i < 1000; i = i + 1 {
        if is_prime(i) == 1 {
            count = count + 1
        }
    }
    print(count)
}
```

---

### sort.hn

**Purpose:** Measure array operations and nested loops

**What it tests:**
- Array access and assignment
- Nested loop iteration
- Bubble sort algorithm

**Expected runtime:** ~150-250ms

**Note:** This is a placeholder benchmark. Full array support depends on hunnu-lang's current capabilities.

---

## Adding New Benchmarks

1. Create file in `benchmarks/your_name.hn`
2. Test with: `./hunnu/build/hunnu benchmarks/your_name.hn`
3. Verify with benchmark runner: `python3 benchmark.py --test your_name`

## Benchmark Best Practices

- **Iteration count:** Aim for 50-500ms total runtime
- **Deterministic output:** Same input = same output
- **Minimal I/O:** Avoid file operations
- **Clear purpose:** Document what you're testing