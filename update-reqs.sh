#!/bin/bash
# update requirements*.txt files with uv pip compile
set -euo pipefail

echo "updating requirements*.txt files"
uv pip compile --generate-hashes pyproject.toml -o requirements.txt > /dev/null
uv pip compile --extra dev --generate-hashes pyproject.toml -o requirements-dev.txt > /dev/null
uv pip compile --extra dev --extra manifest-analysis --generate-hashes pyproject.toml -o requirements-manifest-analysis.txt > /dev/null
echo "done"

