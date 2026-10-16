---
name: designing-screens
description: Designs screens and flows as interactive prototypes published as Artifacts, or critiques existing ones. Use when the user asks to design, mock up, prototype, redesign or critique a screen, page, dashboard, table, form or flow.
---

# Screen Designer

Copy this checklist and tick it off:

```
- [ ] 1. Brief
- [ ] 2. Build the prototype
- [ ] 3. Review and fix
- [ ] 4. Publish
- [ ] 5. Present
```

## 1. Brief

Pin down who uses the screen, the job it does, its one primary action and the data behind it. Ask only the real gaps, in one round.

The project's design system (tokens, theme config, components, icons, existing screens) is the source of every value and pattern. No design system: pick a neutral one and list it as an assumption.

## 2. Build the prototype

Every state the screen can be in sits behind a state switcher: populated, empty, no results, loading, error, no permission.

## 3. Review

Fix every failure before publishing:

- One visually dominant action.
- Every value and component from the design system; nothing invented.
- Flat surfaces, one level of cards; prime space goes to data, not greetings or hero banners.
- State has a non-color signal; WCAG AA contrast in every theme.
- Numbers in tables are tabular and right-aligned.
- Mock data is realistic, localized and includes edge cases (long text, zero, huge numbers); interactions work on it.

## 4. Publish

The project may already have an artifact holding all its screens: the one the user names, else look in their artifact list. Several candidates or none: ask whether to add to one or start a new one.

- **Existing artifact**: add the screen as its own file and navigation entry, following its structure. Every existing screen stays intact.
- **New artifact**: one file per screen plus an index page linking them.
- **Removing, renaming or overwriting an existing screen** needs the user's explicit yes first, per screen.

## 5. Present

Where the screen lives in the artifact, any change to other screens (shared navigation, tokens, styles), key design decisions and why, assumptions, and next-iteration directions.

## Critiquing an existing screen

Prioritized issues against step 3, each with its fix. Offer to build the improved version.
