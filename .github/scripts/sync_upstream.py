#!/usr/bin/env python3
"""Copy picked skills from an upstream repo into skills/.

Config: .github/upstream.json
  repo     GitHub repo to copy from, e.g. "mattpocock/skills"
  ref      branch or tag to track
  license  upstream license file, copied into each synced skill
  skills   paths under the upstream skills/ folder; each lands at skills/<basename>/

Lock: .github/upstream.lock.json records the upstream commit and the skills it
copied, so a skill dropped from the config is deleted from skills/ on the next run.

Usage (run from the repo root):
  python3 .github/scripts/sync_upstream.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
CONFIG = ROOT / ".github" / "upstream.json"
LOCK = ROOT / ".github" / "upstream.lock.json"
SKILLS = ROOT / "skills"


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def main() -> None:
    if not CONFIG.is_file():
        sys.exit("error: .github/upstream.json not found (run from the repo root)")
    config = json.loads(CONFIG.read_text())
    lock = json.loads(LOCK.read_text()) if LOCK.is_file() else {"skills": []}

    names = [Path(p).name for p in config["skills"]]
    if len(set(names)) != len(names):
        sys.exit("error: two picked skills share a folder name")

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "upstream"
        git("clone", "--quiet", "--depth", "1", "--branch", config["ref"],
            f"https://github.com/{config['repo']}.git", str(src), cwd=ROOT)
        sha = git("rev-parse", "HEAD", cwd=src)

        missing = [p for p in config["skills"] if not (src / "skills" / p / "SKILL.md").is_file()]
        if missing:
            sys.exit(f"error: not found upstream (renamed or removed?): {', '.join(missing)}")

        # A picked skill must not overwrite one of ours.
        clashes = [n for n in names if (SKILLS / n).exists() and n not in lock["skills"]]
        if clashes:
            sys.exit(f"error: would overwrite your own skills: {', '.join(clashes)}")

        for name in lock["skills"]:
            if name not in names:
                shutil.rmtree(SKILLS / name, ignore_errors=True)
                print(f"removed skills/{name}")

        for path, name in zip(config["skills"], names):
            shutil.rmtree(SKILLS / name, ignore_errors=True)
            shutil.copytree(src / "skills" / path, SKILLS / name)
            shutil.copy(src / config["license"], SKILLS / name / "LICENSE")
            print(f"synced  skills/{name} <- {config['repo']}/skills/{path}")

    LOCK.write_text(json.dumps({"repo": config["repo"], "commit": sha, "skills": names}, indent=2) + "\n")
    print(f"upstream at {sha[:7]}")


if __name__ == "__main__":
    main()
