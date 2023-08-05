#!/bin/bash

# check if maturin is installed
if ! command -v maturin &> /dev/null
then
    echo "maturin could not be found"
    echo "installing maturin"
    pip install maturin
fi

# Build the project
maturin build -r

# find the most recent wheel
wheel=$(ls -t target/wheels/*.whl | head -1)

# Install the built wheel
pip install "$wheel" --force-reinstall
