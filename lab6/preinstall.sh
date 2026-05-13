#!/usr/bin/env bash
set -e

sudo apt update
sudo apt install -y build-essential cmake gcc g++ make libopencv-dev

echo "Dependencies installed successfully."
