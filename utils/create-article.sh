#!/bin/bash
# Wrapper script for creating articles from YAML definitions
# Usage: ./scripts/create-article.sh article.yaml [--source-dir ./images]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$1" ]; then
    cat << 'EOF'
Create article from YAML definition

Usage:
  ./scripts/create-article.sh article.yaml [OPTIONS]

Options:
  --source-dir DIR    Directory containing images (default: current)
  --no-dither         Skip image dithering
  --dry-run          Show what would be done without making changes

Examples:
  ./scripts/create-article.sh my-article.yaml
  ./scripts/create-article.sh my-article.yaml --source-dir ./article-images
  ./scripts/create-article.sh my-article.yaml --dry-run
EOF
    exit 1
fi

cd "$REPO_DIR"
python3 scripts/create_article.py "$@"
