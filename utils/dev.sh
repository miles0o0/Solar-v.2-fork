#!/bin/bash
# Quick start development workflow for Solar v2
# Usage: ./scripts/dev.sh article.yaml [--source-dir ./images]

set -e

YAML_FILE="${1}"
ARGS="${@:2}"

if [ -z "$YAML_FILE" ]; then
    cat << 'EOF'
Quick start article development workflow

Usage:
  ./scripts/dev.sh article.yaml [OPTIONS]

This script will:
  1. Create article from YAML definition
  2. Build the Hugo site
  3. Start the development server

Options:
  --source-dir DIR    Directory containing images (default: current)
  --no-dither         Skip image dithering
  --dry-run          Show what would be done without making changes

Examples:
  ./scripts/dev.sh my-article.yaml
  ./scripts/dev.sh my-article.yaml --source-dir ./article-images
  ./scripts/dev.sh my-article.yaml --dry-run
EOF
    exit 1
fi

echo "🔨 Creating article from YAML..."
python3 scripts/create_article.py "$YAML_FILE" $ARGS

echo ""
echo "🏗️ Building Hugo site..."
hugo

echo ""
echo "🌐 Starting development server..."
echo "📍 Open http://localhost:1313 in your browser"
hugo server
