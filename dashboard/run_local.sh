#!/usr/bin/env bash
# Run the thesis dashboard locally.
# Usage: bash dashboard/run_local.sh
#
# Prerequisites: Python 3.10+, pip install plotly
# Optional: texcount (for more accurate word counts)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

echo "=== Thesis Dashboard Generator ==="
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found. Please install Python 3.10+."
    exit 1
fi

# Install deps if needed
if ! python3 -c "import plotly" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip3 install -r dashboard/requirements.txt
fi

echo "[1/3] Collecting data from git history..."
python3 dashboard/collect_data.py

echo ""
echo "[2/3] Evaluating achievements..."
python3 -c "
from dashboard.achievements import evaluate_and_save
from dashboard.collect_data import HISTORY_FILE
import json
with open('$SCRIPT_DIR/data/history.json') as f:
    history = json.load(f)
evaluate_and_save(history)
"

echo ""
echo "[3/3] Generating dashboard..."
python3 dashboard/generate_dashboard.py

OUTPUT="$SCRIPT_DIR/output/index.html"
echo ""
echo "=== Done! ==="
echo "Dashboard: $OUTPUT"
echo ""

# Try to open in browser
if command -v xdg-open &>/dev/null; then
    xdg-open "$OUTPUT" 2>/dev/null &
elif command -v open &>/dev/null; then
    open "$OUTPUT"
else
    echo "Open the file above in your browser."
fi
