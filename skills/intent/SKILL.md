---
name: intent
description: Turns an idea, ticket or incident into intent.md, the first artifact of the AI-native SDLC, written for product owners, product managers and other business people. Interviews the user like a business analyst, writes the intent from a template, and commits it. Use when the user asks to capture, write, or draft an intent or intent.md. Manual use only.
disable-model-invocation: true
---

# Capturing intent

Stage 1 (Plan) of the AI-native SDLC. Next stage: `spec`.

The user is a product owner, product manager or other business person. Keep the conversation and the intent in business language: no code, file names, APIs, databases, architecture or technology choices. Technical detail belongs to the spec.

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

Ask the questions a business analyst would ask, a few at a time, until each template section has an answer or an explicit unknown:

- **Problem:** who hits it, how often, what it costs today (time, money, calls, errors).
- **Outcome:** what is true when this is done? How would we measure it?
- **Users and teams:** who uses it, which teams, customers, partners and business processes are touched.
- **Constraints:** privacy, compliance, budget, deadlines, policies, contracts.
- **Scope:** what is explicitly out.

Do not read the code or ask technical questions. If the user brings up a technical detail, ask what business need is behind it and record that need; leave the detail for the spec. Never design the solution here: that is the spec's job.

## 3. Write intent.md

Use [intent-template.md](intent-template.md).

- Write in the originator's terms, not engineering terms. A reader with no technical background must understand every sentence.
- Never fill gaps by guessing. Add an **Open questions** section only for questions still unanswered: ones you asked that the user could not answer, or ones the user raised that you could not answer. If there are none, leave the section out.
- Location: `docs/changes/<YYYY-MM-DD>-<slug>/intent.md`. Date is today, slug is 2-5 kebab-case words from the title. If the folder exists, ask whether to update it or pick a new slug.
- Author: the git `user.name` (ask if unset). Status: `draft`.

## 4. Correct

Show the file. Ask the user what you misunderstood. Apply fixes and repeat until they have none.

## 5. Commit

Commit only `intent.md` with message `docs(sdlc): capture intent for <slug>`. Do not push unless the user asks.

## 6. Accept

The intent is accepted only when the user (product owner) says so. Then set `Status: accepted` and commit with `docs(sdlc): accept intent for <slug>`. Tell the user the next step is `/spec`. Do not start it yourself.
