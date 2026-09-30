#!/usr/bin/env python3
"""Keep .claude-plugin/marketplace.json in sync and check the skills in skills/.

Layout (standard Claude plugin layout, repo root = plugin root = marketplace):
  .claude-plugin/plugin.json        plugin manifest (name, description, author)
  .claude-plugin/marketplace.json   marketplace listing this repo as one plugin
  skills/<skill-name>/SKILL.md      skills, discovered automatically

Usage (run from the repo root):
  python3 .github/scripts/gen_marketplace.py            # write marketplace.json
  python3 .github/scripts/gen_marketplace.py --check    # CI: fail if out of date or a skill is broken

No `version` is written on purpose: without it, Claude Code tracks commits,
so every push reaches you without a manual version bump.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
SKILLS = ROOT / "skills"


def check_skills() -> list[str]:
    """Return a list of problems with the skills in skills/."""
    problems = []
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir()) if SKILLS.is_dir() else []
    if not dirs:
        problems.append("no skills found in skills/")
    for d in dirs:
        f = d / "SKILL.md"
        if not f.is_file():
            problems.append(f"skills/{d.name}: missing SKILL.md")
            continue
        m = re.match(r"---\s*\n(.*?)\n---", f.read_text(encoding="utf-8", errors="replace"), re.S)
        if not m:
            problems.append(f"skills/{d.name}/SKILL.md: missing frontmatter")
            continue
        name = re.search(r"^name:\s*(\S+)", m.group(1), re.M)
        if not name:
            problems.append(f"skills/{d.name}/SKILL.md: no name in frontmatter")
        elif name.group(1).strip("\"'") != d.name:
            problems.append(f"skills/{d.name}: folder name != frontmatter name '{name.group(1)}'")
        if not re.search(r"^description:\s*\S", m.group(1), re.M):
            problems.append(f"skills/{d.name}/SKILL.md: no description in frontmatter")
    return problems


def build() -> dict:
    plugin = json.loads(PLUGIN.read_text())
    existing = json.loads(MANIFEST.read_text()) if MANIFEST.is_file() else {}
    return {
        "name": existing.get("name") or "lucas-plugins",
        "description": existing.get("description") or "Personal skills, synced from this repo",
        "owner": existing.get("owner") or plugin.get("author") or {"name": "Lucas Segundo"},
        "plugins": [
            {
                "name": plugin["name"],
                "source": "./",
                "description": plugin.get("description", ""),
            }
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if marketplace.json is out of date or a skill is broken")
    args = ap.parse_args()

    if not PLUGIN.is_file():
        sys.exit("error: .claude-plugin/plugin.json not found (run from the repo root)")

    problems = check_skills()
    for p in problems:
        print(f"error: {p}", file=sys.stderr)

    rendered = json.dumps(build(), indent=2) + "\n"
    n = len([p for p in SKILLS.iterdir() if p.is_dir()]) if SKILLS.is_dir() else 0

    if args.check:
        current = MANIFEST.read_text() if MANIFEST.is_file() else ""
        if current != rendered:
            print("marketplace.json is out of date. Run: python3 .github/scripts/gen_marketplace.py")
            sys.exit(1)
        if problems:
            sys.exit(1)
        print(f"marketplace.json is up to date; {n} skills OK.")
        return

    MANIFEST.write_text(rendered)
    print(f"Wrote {MANIFEST.relative_to(ROOT)} ({n} skills in skills/)")
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
