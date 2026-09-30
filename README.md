# lucas-skills

Private Claude Code plugin with my personal skills. Each top-level folder containing a `SKILL.md` is a skill.

## Install (Claude Code)

```
/plugin marketplace add git@github.com-lucas:lucas-segundo/skills.git
/plugin install lucas-skills@lucas-plugins
```

Skills are invoked as `/lucas-skills:<skill-name>`.

## Add or remove a skill

1. Create or delete the `<skill-name>/SKILL.md` folder.
2. Regenerate the manifest: `python3 .github/scripts/gen_marketplace.py`
3. Commit and push. Then in Claude Code, run `/plugin marketplace update lucas-plugins` (or enable auto-update).

## Cowork (.plugin file)

Cowork can't sync from a private repo, so the plugin is also packaged as a file.

- **CI:** every push to `main` builds `lucas-skills.plugin` and publishes it to the
  [`latest` release](../../releases/tag/latest). Download it and upload it in Cowork's plugin settings.
- **Locally:** `python3 .github/scripts/build_plugin.py --validate`
  writes `dist/lucas-skills.plugin` plus an unpacked copy in `dist/lucas-skills/` to inspect.
