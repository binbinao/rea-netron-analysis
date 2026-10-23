#!/usr/bin/env bash
# Re-run the REA JavaScript/Electron analysis that produced the evidence in ../evidence/.
#
# Usage:  ./scripts/analyze.sh [target-app-path]
# Default target: /Applications/Netron.app
#
# Requires: Node.js >=22.19 (or 24.x >=24.11, or 26+) and npm.
# The omp MCP registration is NOT needed here; this calls the REA CLI directly.
set -euo pipefail

TARGET="${1:-/Applications/Netron.app}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT/evidence"

if [[ ! -d "$TARGET" ]]; then
  echo "target not found: $TARGET" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

# Name the output after the version actually installed, so the evidence file and
# the article never drift apart.
VERSION="$(defaults read "$TARGET/Contents/Info.plist" CFBundleShortVersionString 2>/dev/null || echo unknown)"
OUT="$OUT_DIR/netron-${VERSION}-analyze-javascript-application.json"

echo "==> REA analyzing $TARGET (version $VERSION)"
echo "==> writing $OUT (~70s, ~60MB)"

npx -y rea-agents@latest analyze-javascript-application "$TARGET" --json > "$OUT"

echo "==> sha256:"
shasum -a 256 "$OUT"

cat <<EOF

The JSON embeds absolute paths and per-run sequencing, so a re-run is NOT
byte-identical. The identity of the analyzed binary is:
  subject.digest.sha256 in the evidence  ==  sha256 of the app bundle
Compare that against the value recorded in reports/netron-architecture.md.
EOF
