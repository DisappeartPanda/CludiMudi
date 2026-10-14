#!/bin/bash
# Installiert die Research-Tools (yt-dlp, instaloader) in Cloud-Sessions.
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
pip install -q -r "$CLAUDE_PROJECT_DIR/requirements.txt" 2>/dev/null || echo "Hinweis: Research-Tools konnten nicht installiert werden."
