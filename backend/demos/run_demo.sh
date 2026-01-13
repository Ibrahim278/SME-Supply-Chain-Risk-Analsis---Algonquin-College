#!/bin/bash
# Data Collection Agent Demo Runner
# Usage: ./demos/run_demo.sh <url> [output_file]

set -e

# =============================================================================
# CONFIGURATION - Set your API key here
# =============================================================================
OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-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}"  # Set your key here, e.g., "sk-or-v1-..."
OPENROUTER_MODEL="${OPENROUTER_MODEL:-anthropic/claude-haiku-4.5}"
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Data Collection Agent Demo ===${NC}"
echo ""

# Check for URL argument
if [ -z "$1" ]; then
    echo -e "${RED}Error: Please provide a supplier URL${NC}"
    echo ""
    echo "Usage: ./demos/run_demo.sh <url> [output_file]"
    echo ""
    echo "Examples:"
    echo "  ./demos/run_demo.sh https://bcorporation.net"
    echo "  ./demos/run_demo.sh https://example.com output/result.json"
    exit 1
fi

URL="$1"
# Default output to demos/output folder with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DOMAIN=$(echo "$1" | sed -E 's|https?://([^/]+).*|\1|' | sed 's/www\.//' | sed 's/\./_/g')
OUTPUT_FILE="${2:-$SCRIPT_DIR/output/${DOMAIN}_${TIMESTAMP}.json}"

# Export API key and model for Python
if [ -n "$OPENROUTER_API_KEY" ]; then
    export OPENROUTER_API_KEY
    export OPENROUTER_MODEL
    echo -e "${GREEN}Using OpenRouter with model: $OPENROUTER_MODEL${NC}"
elif [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${YELLOW}No LLM API key configured.${NC}"
    echo -e "${YELLOW}Set OPENROUTER_API_KEY in the script or skip LLM analysis.${NC}"
    echo ""
fi

# Activate venv
cd "$BACKEND_DIR"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo -e "${RED}Error: Virtual environment not found at $BACKEND_DIR/venv${NC}"
    echo "Run: python -m venv venv && pip install -r requirements.txt"
    exit 1
fi

# Build command (always outputs to file now)
CMD="python demos/data_collection_demo.py \"$URL\" -o \"$OUTPUT_FILE\""

# Run
echo -e "${GREEN}Running demo...${NC}"
echo ""
eval $CMD
