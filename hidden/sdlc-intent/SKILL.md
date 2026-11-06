---
name: sdlc-intent
description: Turns an idea, ticket or incident into intent.md, the first artifact of the AI-native SDLC, written for product owners, product managers and other business people. Interviews the user like a business analyst, writes the intent from a template, and leaves it uncommitted for the user. Use when the user says "write an intent", "capture the intent", "draft intent.md", "turn this idea/ticket/incident into an intent", or starts a new change with no intent yet.
---

# Capturing intent

Stage 1 (Plan) of the AI-native SDLC. Next stage: `sdlc-spec`.

Never commit, stage or offer to commit `intent.md`; what to do with it is the user's call.

The user is a product owner, product manager or other business person. Keep the conversation and the intent in business language: no code, file names, APIs, databases, architecture or technology choices. Technical detail belongs to the spec.

Copy this checklist and tick it off:

```
- [ ] 1. Listen
- [ ] 2. Interview until the idea is concrete
- [ ] 3. Write intent.md
- [ ] 4. Let the user correct it
- [ ] 5. Accept (only on the user's word)
```

## Asking questions

Every question in this skill goes through the **AskUserQuestion** tool, never as a text block in chat:

- Batch the questions you can ask now into one call (at most 4 per call; split a larger batch across consecutive calls). A question that depends on an answer you have not heard yet waits for the next call.
- Per question: `header` a short title; `question` self-contained (name the thing asked about, since earlier chat may be hidden while the dialog is open); `options` 2–4 plausible answers, in business language, your recommended one first and labelled "(Recommended)". The user can always pick "Other" for free text.
- After each call, wait for the answers. Never answer for the user or carry on with an assumed default.
- If AskUserQuestion is missing or errors, ask the same questions in chat as a numbered list, each with your recommended answer, then end the turn and wait for the reply.

## 1. Listen

Let the user describe the problem in their own words: what they cannot do today, who is affected, what better looks like, what is out of scope. No formal language needed. Do not propose a solution yet.

## 2. Interview

Ask the questions a business analyst would ask (see **Asking questions**), until each template section has an answer or an explicit unknown:

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
- Location: `docs/changes/<YYYY-MM-DD>-<slug>/intent.md`. Date is today, slug is 2-5 kebab-case words from the title. If the folder exists, ask (AskUserQuestion) whether to update it or pick a new slug.
- Author: the git `user.name` (ask with AskUserQuestion if unset). Status: `draft`.

## 4. Correct

Show the file. Ask with AskUserQuestion whether anything is wrong, offering the parts you are least sure of as options plus "Looks right". Apply fixes and repeat until they pick "Looks right".

## 5. Accept

Ask with AskUserQuestion: "Accept intent.md?" with options "Accept" and "Keep editing". The intent is accepted only when the user (product owner) picks Accept or says so. Then set `Status: accepted`. Tell the user the next step is `/sdlc-spec`. Do not start it yourself.
