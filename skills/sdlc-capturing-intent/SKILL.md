---
name: sdlc-capturing-intent
description: Turns an idea, ticket or incident into intent.md, the first artifact of the AI-native SDLC. Interviews the user like an analyst, writes the intent from a template, and commits it. Use when the user asks to capture, write, or draft an intent or intent.md. Manual use only.
disable-model-invocation: true
---

# Capturing intent

Stage 1 (Plan) of the AI-native SDLC. Next stage: `sdlc-writing-specs`.

Copy this checklist and tick it off:

```
- [ ] 1. Listen
- [ ] 2. Interview until the idea is concrete
- [ ] 3. Write intent.md
- [ ] 4. Let the user correct it
- [ ] 5. Commit
- [ ] 6. Accept (only on the user's word)
```

## 1. Listen

Let the user describe the problem in their own words: what they cannot do today, who is affected, what better looks like, what is out of scope. No formal language needed. Do not propose a solution yet.

## 2. Interview

Ask the questions an analyst would ask, a few at a time, until each template section has an answer or an explicit unknown:

- **Problem:** who hits it, how often, what it costs today (time, money, calls, errors).
- **Outcome:** what is true when this is done? How would we measure it?
- **Users and systems:** who uses it, which systems and teams are touched.
- **Constraints:** security, privacy, compliance, budget, deadlines, tech that must or must not be used.
- **Scope:** what is explicitly out.

Read the repo only to name affected systems correctly. Never design the solution here: that is the spec's job.

## 3. Write intent.md

Use [intent-template.md](intent-template.md).

- Write in the originator's terms, not engineering terms.
- Anything unknown or disputed goes to **Open questions**. Never fill gaps by guessing.
- Location: `docs/changes/<YYYY-MM-DD>-<slug>/intent.md`. Date is today, slug is 2-5 kebab-case words from the title. If the folder exists, ask whether to update it or pick a new slug.
- Author: the git `user.name` (ask if unset). Status: `draft`.

## 4. Correct

Show the file. Ask the user what Claude misunderstood. Apply fixes and repeat until they have none.

## 5. Commit

Commit only `intent.md` with message `docs(sdlc): capture intent for <slug>`. Do not push unless the user asks.

## 6. Accept

The intent is accepted only when the user (product owner) says so. Then set `Status: accepted` and commit with `docs(sdlc): accept intent for <slug>`. Tell the user the next step is `/sdlc-writing-specs`. Do not start it yourself.
