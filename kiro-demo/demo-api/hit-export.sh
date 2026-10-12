#!/usr/bin/env bash
# Calls /reports/export several times in a row and prints each HTTP status.
# Before rate limiting: all 200. After: 200s, then 429s.
# Usage: ./hit-export.sh [count]   (default 6; the server must be running)

COUNT="${1:-6}"
for i in $(seq 1 "$COUNT"); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -H "X-API-Key: demo-key-alpha" http://127.0.0.1:8000/reports/export)
  echo "Request $i -> $code"
done
