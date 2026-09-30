# lucas-skills

Private Claude plugin with my personal skills.

```
.claude-plugin/plugin.json        plugin manifest
.claude-plugin/marketplace.json   marketplace (this repo = one plugin)
skills/<skill-name>/SKILL.md      the skills
```

## Install

**Claude app / Cowork:** claude.ai admin settings → Skills → Add → Sync from GitHub → pick this repo.

**Claude Code:**

```
/plugin marketplace add git@github.com-lucas:lucas-segundo/skills.git
/plugin install lucas-skills@lucas-plugins
```

Skills are invoked as `/lucas-skills:<skill-name>`.

## Add or remove a skill

1. Create or delete `skills/<skill-name>/SKILL.md` (the folder name must match `name:` in the frontmatter).
2. Check it: `python3 .github/scripts/gen_marketplace.py --check`
3. Commit and push. Then in Claude Code, run `/plugin marketplace update lucas-plugins` (or enable auto-update).

## Cowork (.plugin file)

Cowork can't sync from a private repo, so the plugin is also packaged as a file.

- **CI:** every push to `main` builds `lucas-skills.plugin` and publishes it to the
  [`latest` release](../../releases/tag/latest). Download it and upload it in Cowork's plugin settings.
- **Locally:** `python3 .github/scripts/build_plugin.py --validate`
  writes `dist/lucas-skills.plugin` plus an unpacked copy in `dist/lucas-skills/` to inspect.
