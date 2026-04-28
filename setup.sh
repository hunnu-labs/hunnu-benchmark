#!/bin/bash

set -e

echo "Setting up hunnu-benchmark..."
echo ""

# Clone hunnu-lang if not present
if [ ! -d "hunnu" ]; then
    echo "Cloning hunnu-lang repository..."
    git clone https://github.com/hunnu-labs/hunnu-lang.git hunnu
else
    echo "hunnu-lang directory already exists, pulling latest changes..."
    cd hunnu && git pull && cd ..
fi

# Build hunnu-lang
echo ""
echo "Building hunnu-lang..."
cd hunnu
mkdir -p build
cd build
cmake ..
make
cd ../..

# Verify build
if [ -f "hunnu/build/hunnu" ]; then
    echo ""
    echo "Setup complete!"
    echo "Binary location: $(pwd)/hunnu/build/hunnu"
    echo ""
    echo "Running a quick test..."
    ./hunnu/build/hunnu hunnu/examples/main.hn
else
    echo ""
    echo "Error: Build failed. Binary not found at hunnu/build/hunnu"
    exit 1
fi
