#!/usr/bin/env bash
set -e

if [ ! -f build/lab6 ]; then
    echo "Executable not found. Run ./build.sh first."
    exit 1
fi

./build/lab6
