#!/bin/bash
set -e

echo "Setting up hunnu-benchmark..."
echo ""

init_submodule() {
    local sub_name="hunnu"
    local sub_url="https://github.com/hunnu-labs/hunnu-lang.git"

    if [ ! -f ".gitmodules" ]; then
        echo "Initializing submodule '$sub_name'..."
        git submodule add "$sub_url" "$sub_name" 2>/dev/null || true
    fi

    if [ ! -d "$sub_name/.git" ] && [ ! -f "$sub_name/HEAD" ]; then
        echo "Cloning submodule '$sub_name'..."
        git submodule update --init --recursive
    else
        echo "Updating submodule '$sub_name'..."
        git submodule update --remote "$sub_name" 2>/dev/null || git submodule update --init "$sub_name" 2>/dev/null || true
    fi
}

if [ -f ".gitmodules" ]; then
    init_submodule
elif [ ! -d "hunnu" ]; then
    echo "Cloning hunnu-lang repository..."
    git clone https://github.com/hunnu-labs/hunnu-lang.git hunnu
else
    echo "hunnu-lang directory already exists."
fi

echo ""
echo "Building hunnu-lang..."
mkdir -p hunnu/build
(
    cd hunnu/build
    cmake .. 2>&1
    make -j"$(nproc)" 2>&1
)

if [ -f "hunnu/build/hunnu" ]; then
    echo ""
    echo "Setup complete!"
    echo "Binary: $(pwd)/hunnu/build/hunnu"
    echo ""
    echo "Quick test:"
    ./hunnu/build/hunnu hunnu/examples/main.hn
    echo ""
    echo "Run benchmarks: python3 benchmark.py"
else
    echo ""
    echo "Error: Build failed. Binary not found at hunnu/build/hunnu"
    exit 1
fi
