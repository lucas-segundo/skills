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
