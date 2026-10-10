#!/usr/bin/env python3
"""Copy picked skills from upstream repos into skills/.

Config: .github/upstream.json, a list of "upstreams", each with:
  repo     GitHub repo to copy from, e.g. "mattpocock/skills"
  ref      branch or tag to track
  license  upstream license files (LICENSE, NOTICE, ...), copied into each synced skill
  skills   paths under the upstream skills/ folder; each lands at skills/<basename>/

Lock: .github/upstream.lock.json records each upstream commit and the skills it
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
    upstreams = json.loads(CONFIG.read_text())["upstreams"]
    locked = json.loads(LOCK.read_text()) if LOCK.is_file() else {}
    synced_before = {name for u in locked.get("upstreams", []) for name in u["skills"]}

    names = [Path(p).name for u in upstreams for p in u["skills"]]
    if len(set(names)) != len(names):
        sys.exit("error: two picked skills share a folder name")

    # A picked skill must not overwrite one of ours.
    clashes = [n for n in names if (SKILLS / n).exists() and n not in synced_before]
    if clashes:
        sys.exit(f"error: would overwrite your own skills: {', '.join(clashes)}")

    with tempfile.TemporaryDirectory() as tmp:
        # Fetch and check every upstream before touching skills/.
        sources = []
        for i, u in enumerate(upstreams):
            src = Path(tmp) / str(i)
            git("clone", "--quiet", "--depth", "1", "--branch", u["ref"],
                f"https://github.com/{u['repo']}.git", str(src), cwd=ROOT)
            missing = [p for p in u["skills"] if not (src / "skills" / p / "SKILL.md").is_file()]
            missing += [f for f in u["license"] if not (src / f).is_file()]
            if missing:
                sys.exit(f"error: not found in {u['repo']} (renamed or removed?): {', '.join(missing)}")
            sources.append(src)

        for name in sorted(synced_before - set(names)):
            shutil.rmtree(SKILLS / name, ignore_errors=True)
            print(f"removed skills/{name}")

        lock = []
        for u, src in zip(upstreams, sources):
            for path in u["skills"]:
                name = Path(path).name
                shutil.rmtree(SKILLS / name, ignore_errors=True)
                shutil.copytree(src / "skills" / path, SKILLS / name)
                for f in u["license"]:
                    shutil.copy(src / f, SKILLS / name / Path(f).name)
                print(f"synced  skills/{name} <- {u['repo']}/skills/{path}")
            sha = git("rev-parse", "HEAD", cwd=src)
            lock.append({"repo": u["repo"], "commit": sha, "skills": [Path(p).name for p in u["skills"]]})
            print(f"{u['repo']} at {sha[:7]}")

    LOCK.write_text(json.dumps({"upstreams": lock}, indent=2) + "\n")


if __name__ == "__main__":
    main()
