---
name: sdlc-intent
description: Turns an idea, ticket or incident into intent.md, the first artifact of the AI-native SDLC, for product owners and other business people. Use when the user says "write an intent", "capture the intent", "draft intent.md", or starts a new change with no intent yet.
---

# Capturing intent

Stage 1 (Plan) of the AI-native SDLC. Next stage: `sdlc-spec`.

Do not commit `intent.md`; that is the user's call.

The user is a product owner, product manager or other business person. Keep the conversation and the intent in business language: no code, file names, APIs, databases, architecture or technology choices. Technical detail belongs to the spec.

## Asking questions

Ask every question with **AskUserQuestion**, never as chat text: batch the ones you can ask now, write options in business language with your recommendation first, and wait for the answers instead of assuming a default.

## 1. Listen

Let the user describe the problem in their own words: what they cannot do today, who is affected, what better looks like, what is out of scope. No formal language needed. Do not propose a solution yet.

## 2. Interview

Ask the questions a business analyst would ask until each template section has an answer or an explicit unknown. Include what is explicitly out of scope (record it under Constraints).

Do not read the code or ask technical questions. If the user brings up a technical detail, ask what business need is behind it and record that need; leave the detail for the spec.

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
