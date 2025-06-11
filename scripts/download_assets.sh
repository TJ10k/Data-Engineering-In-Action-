#!/usr/bin/env bash
# Download the data and screenshots archives and extract them.

set -euo pipefail

ASSETS_URL=${ASSETS_URL:-"https://example.com/assets.tar.gz"}

curl -L "$ASSETS_URL" -o assets.tar.gz

tar -xzf assets.tar.gz

echo "Assets downloaded and extracted."
