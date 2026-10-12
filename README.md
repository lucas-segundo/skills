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

`skills/caveman` is the terse-reply skill, synced from [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman). `hooks/hooks.json` runs a `UserPromptSubmit` hook that reminds Claude to use caveman on every prompt. Edit the `echo` text there to change the mode or remove the hook to turn it off.

## SDLC

Three skills, invoked by name or by asking (e.g. "write an intent"), one per artifact of the AI-native SDLC. Each reads the previous artifact, stops if it is not `accepted`, and commits its file to `docs/changes/<YYYY-MM-DD>-<slug>/`:

1. `/sdlc-intent` → `intent.md` (what is wanted and why)
2. `/sdlc-spec` → `spec.md` (requirements, design, flagged concerns; you name the policy skills)
3. `/sdlc-plan` → `plan.md` (files, order of work, risks, proof)

## Pull requests

- `/pr` writes a PR body (from [mattpocock/skills](https://github.com/mattpocock/skills), see Upstream skills).
- `/pr-code-review` reviews a PR with terse one-line inline comments. The `claude.yml` workflow in `lucas-segundo/ai` uses it for reviews.
- `/pr-fix` follows up a PR's review comments: fixes, replies to and resolves your own, reports the rest.

## Upstream skills

Some skills are copied from other repos instead of written here. `.github/upstream.json` lists them per repo (paths under the upstream `skills/` folder); each lands at `skills/<name>/` with the upstream license files. Don't edit them here: changes are overwritten on the next sync.

- Add or drop one: edit the list, run `python3 .github/scripts/sync_upstream.py`, commit.
- Updates: the `Sync upstream skills` workflow runs weekly (or on demand) and opens a PR when a picked skill changed upstream. `.github/upstream.lock.json` records each upstream commit.
