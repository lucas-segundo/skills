#!/usr/bin/env python3
"""Generate .claude-plugin/marketplace.json for a repo whose top-level folders are skills.

A skill is any top-level folder (not starting with ".") that contains a SKILL.md.

Usage (run from the repo root):
  python3 .github/scripts/gen_marketplace.py            # write/update marketplace.json
  python3 .github/scripts/gen_marketplace.py --check    # exit 1 if it is out of date (for CI)

Existing name/owner/description/plugin name in marketplace.json are preserved.
No `version` is written on purpose: without it, users track your commits, so
every push reaches them without a manual version bump.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
RESERVED = {
    "claude-code-marketplace", "claude-code-plugins", "claude-plugins-official",
    "claude-plugins-community", "claude-community", "anthropic-marketplace",
    "anthropic-plugins", "agent-skills", "anthropic-agent-skills",
    "knowledge-work-plugins", "life-sciences", "claude-for-legal",
    "claude-for-financial-services", "financial-services-plugins",
    "first-party-plugins", "healthcare",
}


def git_user_name() -> str:
    try:
        out = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
        return out or "Your Name"
    except Exception:
        return "Your Name"


def find_skills() -> list[str]:
    return sorted(
        p.name for p in ROOT.iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / "SKILL.md").is_file()
    )


def frontmatter_name(skill_dir: str) -> str | None:
    text = (ROOT / skill_dir / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    n = re.search(r"^name:\s*(\S+)", m.group(1), re.M)
    return n.group(1).strip("\"'") if n else None


def build(args) -> dict:
    existing = json.loads(MANIFEST.read_text()) if MANIFEST.is_file() else {}
    old_plugin = (existing.get("plugins") or [{}])[0]

    name = args.name or existing.get("name") or "my-skills"
    if name in RESERVED:
        sys.exit(f"error: '{name}' is a reserved marketplace name; pick another with --name")

    skills = find_skills()
    if not skills:
        sys.exit("error: no skill folders (folders containing SKILL.md) found in this directory")

    for s in skills:
        fm = frontmatter_name(s)
        if fm is None:
            print(f"warning: {s}/SKILL.md has no name in its frontmatter", file=sys.stderr)
        elif fm != s:
            print(f"warning: folder '{s}' != frontmatter name '{fm}'", file=sys.stderr)

    plugin = {
        "name": args.plugin or old_plugin.get("name") or "my-personal-skills",
        "source": "./",
        "description": old_plugin.get("description") or "My personal skills",
        "skills": [f"./{s}" for s in skills],
    }
    return {
        "name": name,
        "description": existing.get("description") or "Personal skills, synced from this repo",
        "owner": existing.get("owner") or {"name": args.owner or git_user_name()},
        "plugins": [plugin],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if marketplace.json is out of date")
    ap.add_argument("--name", help="marketplace name (default: my-skills)")
    ap.add_argument("--plugin", help="plugin name (default: my-personal-skills)")
    ap.add_argument("--owner", help="owner name (default: git config user.name)")
    args = ap.parse_args()

    rendered = json.dumps(build(args), indent=2) + "\n"

    if args.check:
        current = MANIFEST.read_text() if MANIFEST.is_file() else ""
        if current != rendered:
            print("marketplace.json is out of date. Run: python3 .github/scripts/gen_marketplace.py")
            sys.exit(1)
        print("marketplace.json is up to date.")
        return

    MANIFEST.parent.mkdir(exist_ok=True)
    MANIFEST.write_text(rendered)
    print(f"Wrote {MANIFEST.relative_to(ROOT)} with {len(json.loads(rendered)['plugins'][0]['skills'])} skills")


if __name__ == "__main__":
    main()
