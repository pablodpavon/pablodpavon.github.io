#!/bin/zsh
# Regenerate assets/data/status.json and publish it (commit + push of that one file only).
# Runs on a Mac from launchd (daily 09:30 Berlin): com.pablodpavon.site-status.plist.
# The repo path comes from the script location, so the clone can live anywhere.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO"
echo "=== $(date '+%Y-%m-%d %H:%M:%S') publish_status"

# Only ever publish from main, with a clean index, so no unrelated change rides along.
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" != "main" ]]; then echo "not on main ($BRANCH): nothing published"; exit 0; fi
if ! git diff --cached --quiet; then echo "staged changes present: nothing published"; exit 0; fi
git pull --ff-only --quiet origin main

/usr/bin/env python3 tools/status/build_status.py

if git diff --quiet -- assets/data/status.json && git ls-files --error-unmatch assets/data/status.json >/dev/null 2>&1; then
  echo "status.json unchanged"; exit 0
fi
git add -- assets/data/status.json
git commit --quiet -m "Status: $(date -u '+%Y-%m-%d %H:%M') UTC" -- assets/data/status.json
git push --quiet origin main
echo "published"
