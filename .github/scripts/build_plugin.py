#!/usr/bin/env python3
"""Build a Cowork-installable .plugin file from this repo.

The repo already uses the standard plugin layout, so this just stages
.claude-plugin/plugin.json (with a version added), skills/ and README.md
into dist/<plugin-name>/ and zips it to dist/<plugin-name>.plugin.

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
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"
IGNORE = shutil.ignore_patterns(".DS_Store", ".DS_STORE", "__pycache__", "*.pyc")
FIXED_TIME = (2000, 1, 1, 0, 0, 0)  # stable zip timestamps -> same input, same bytes


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true", help="run `claude plugin validate` on the result")
    args = ap.parse_args()

    if not PLUGIN.is_file() or not SKILLS.is_dir():
        sys.exit("error: .claude-plugin/plugin.json or skills/ not found (run from the repo root)")

    plugin = json.loads(PLUGIN.read_text())
    name = plugin["name"]
    # 1.0.<commit count> gives Cowork an increasing version on every push.
    plugin["version"] = f"1.0.{git('rev-list', '--count', 'HEAD') or '0'}"
    sha = git("rev-parse", "--short", "HEAD")
    if sha:
        plugin["description"] = f"{plugin.get('description', '')} (built from {sha})".strip()

    stage = DIST / name
    out = DIST / f"{name}.plugin"
    if stage.exists():
        shutil.rmtree(stage)
    (stage / ".claude-plugin").mkdir(parents=True)
    (stage / ".claude-plugin" / "plugin.json").write_text(json.dumps(plugin, indent=2) + "\n")
    shutil.copytree(SKILLS, stage / "skills", ignore=IGNORE)
    if (ROOT / "README.md").is_file():
        shutil.copy(ROOT / "README.md", stage / "README.md")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p for p in stage.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f.relative_to(stage).as_posix(), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, f.read_bytes())

    n = len([p for p in (stage / "skills").iterdir() if p.is_dir()])
    print(f"Built {out.relative_to(ROOT)}  (v{plugin['version']}, {n} skills)")
    print(f"Unpacked copy for inspection: {stage.relative_to(ROOT)}/")

    if args.validate:
        if not shutil.which("claude"):
            sys.exit("error: `claude` CLI not found; install it or drop --validate")
        sys.exit(subprocess.call(["claude", "plugin", "validate", str(stage)]))


if __name__ == "__main__":
    main()
