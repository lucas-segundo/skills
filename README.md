# lucas-skills

Private Claude plugin with my personal skills.

```
.claude-plugin/plugin.json        plugin manifest
.claude-plugin/marketplace.json   marketplace (this repo = one plugin)
skills/<skill-name>/SKILL.md      the skills
hooks/hooks.json                  plugin hooks
```

## Install

claude.ai admin settings → Skills → Add → Sync from GitHub → pick this repo.

## Add or remove a skill

1. Create or delete `skills/<skill-name>/SKILL.md` (the folder name must match `name:` in the frontmatter).
2. Check it: `python3 .github/scripts/gen_marketplace.py --check`
3. Commit and push, then re-sync.

## Caveman

`skills/caveman` is the terse-reply skill. `hooks/hooks.json` runs a `UserPromptSubmit` hook that reminds Claude to use caveman (lite) on every prompt. Edit the `echo` text there to change the level or remove the hook to turn it off.

## SDLC

Three manual skills, one per artifact of the AI-native SDLC. Each reads the previous artifact, stops if it is not `accepted`, and commits its file to `docs/changes/<YYYY-MM-DD>-<slug>/`:

1. `/intent` → `intent.md` (what is wanted and why)
2. `/spec` → `spec.md` (requirements, design, flagged concerns; you name the policy skills)
3. `/plan` → `plan.md` (files, order of work, risks, proof)
