#!/bin/bash

# Find all .py files recursively
find . -name "*.py" | while read file; do
    # Run black formatter on each file
    black "$file"
done
