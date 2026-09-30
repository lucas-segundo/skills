#!/usr/bin/env python3
"""Build a Cowork-installable .plugin file from this repo.

The repo keeps skills as top-level folders (Claude Code marketplace layout).
A .plugin file needs the standalone plugin layout instead:

    .claude-plugin/plugin.json
    skills/<skill-name>/SKILL.md ...

This script reads .claude-plugin/marketplace.json, stages that layout in
dist/<plugin-name>/ and zips it to dist/<plugin-name>.plugin.

Usage (run from the repo root):
  python3 .github/scripts/build_plugin.py              # build
  python3 .github/scripts/build_plugin.py --validate   # build + `claude plugin validate`
"""
import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path.cwd()
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
DIST = ROOT / "dist"
IGNORE = shutil.ignore_patterns(".DS_Store", ".DS_STORE", "__pycache__", "*.pyc")
FIXED_TIME = (2000, 1, 1, 0, 0, 0)  # stable zip timestamps -> same input, same bytes


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def version() -> str:
    # 1.0.<commit count> gives Cowork an increasing version on every push.
    count = git("rev-list", "--count", "HEAD") or "0"
    return f"1.0.{count}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true", help="run `claude plugin validate` on the result")
    args = ap.parse_args()

    if not MANIFEST.is_file():
        sys.exit("error: .claude-plugin/marketplace.json not found (run from the repo root)")
    market = json.loads(MANIFEST.read_text())
    entry = market["plugins"][0]
    name = entry["name"]
    skills = [s.removeprefix("./").rstrip("/") for s in entry.get("skills", [])]
    if not skills:
        sys.exit("error: no skills listed in marketplace.json")

    stage = DIST / name
    out = DIST / f"{name}.plugin"
    shutil.rmtree(stage, ignore_errors=True)
    out.unlink(missing_ok=True)
    (stage / ".claude-plugin").mkdir(parents=True)

    plugin = {
        "name": name,
        "version": version(),
        "description": entry.get("description") or market.get("description", ""),
        "author": market.get("owner", {}),
    }
    sha = git("rev-parse", "--short", "HEAD")
    if sha:
        plugin["description"] += f" (built from {sha})"
    (stage / ".claude-plugin" / "plugin.json").write_text(json.dumps(plugin, indent=2) + "\n")

    for s in skills:
        src = ROOT / s
        if not (src / "SKILL.md").is_file():
            sys.exit(f"error: {s}/SKILL.md not found")
        # Skills stay siblings under skills/, so links like ../other-skill/SKILL.md keep working.
        shutil.copytree(src, stage / "skills" / s, ignore=IGNORE)

    readme = ROOT / "README.md"
    if readme.is_file():
        shutil.copy(readme, stage / "README.md")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p for p in stage.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f.relative_to(stage).as_posix(), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, f.read_bytes())

    print(f"Built {out.relative_to(ROOT)}  (v{plugin['version']}, {len(skills)} skills)")
    print(f"Unpacked copy for inspection: {stage.relative_to(ROOT)}/")

    if args.validate:
        if not shutil.which("claude"):
            sys.exit("error: `claude` CLI not found; install it or drop --validate")
        sys.exit(subprocess.call(["claude", "plugin", "validate", str(stage)]))


if __name__ == "__main__":
    main()
