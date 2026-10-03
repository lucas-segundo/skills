#!/bin/bash
# Cloud env setup script: paste this into the environment's "Setup script" field
# (or curl it from a raw URL). Fetches lucas-segundo/ai and runs its
# scripts/setup.sh to install the lucas-skills plugin.
# Needs SETUP_GITHUB_TOKEN (fine-grained, read-only contents) in the env variables,
# because lucas-segundo/skills is private.
# Do not append `|| true` / `exit 0`: a failed setup must stay visible.
set -euo pipefail

AI_DIR="${AI_DIR:-/opt/lucas-ai}"

# lucas-segundo/ai is public, no token needed to fetch it.
if [ -d "$AI_DIR/.git" ]; then
  git -C "$AI_DIR" pull --ff-only
else
  git clone --depth 1 https://github.com/lucas-segundo/ai "$AI_DIR"
fi

bash "$AI_DIR/scripts/setup.sh" lucas-skills-plugin
