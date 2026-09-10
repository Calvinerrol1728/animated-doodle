#!/usr/bin/env bash
# Serve the study app on all interfaces so the Arena preview can reach it.
cd "$(dirname "$0")"
PORT="${PORT:-8000}"
echo "Study Deck → http://0.0.0.0:${PORT}"
exec python3 -m http.server "${PORT}" --bind 0.0.0.0
