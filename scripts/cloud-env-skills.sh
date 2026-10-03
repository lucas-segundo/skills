#!/bin/bash
# Cloud env setup script: loads skills/* into ~/.claude/skills (no plugin install).
# Uses SETUP_GITHUB_TOKEN if set (private repo); otherwise relies on existing git auth.
set -euo pipefail

REPO=lucas-segundo/skills
SRC="${SKILLS_SRC:-/home/user/skills}"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

if [ -d "$SRC/.git" ]; then
  git -C "$SRC" pull --ff-only || echo "warn: pull failed, using existing checkout"
else
  url="https://github.com/$REPO"
  [ -n "${SETUP_GITHUB_TOKEN:-}" ] && url="https://x-access-token:${SETUP_GITHUB_TOKEN}@github.com/$REPO"
  git clone --depth 1 "$url" "$SRC"
  git -C "$SRC" remote set-url origin "https://github.com/$REPO"
fi

mkdir -p "$DEST"
count=0
for d in "$SRC"/skills/*/; do
  [ -f "$d/SKILL.md" ] || continue
  rm -rf "$DEST/$(basename "$d")"
  cp -r "$d" "$DEST/$(basename "$d")"
  count=$((count + 1))
done

[ "$count" -gt 0 ] || { echo "error: no skills found in $SRC/skills" >&2; exit 1; }
echo "loaded $count skills into $DEST"
