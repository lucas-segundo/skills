# Verification

Last step after editing JS/TS files. Do not end the turn until it has run.

1. **Scope:** only JS/TS files you created or edited this prompt, including files changed by codemods or `--fix`. Skip deleted files. Never the whole project; an empty list means nothing to verify.
2. **Lint:** prefer `npm run lint:ai -- <files>` when `package.json` has it, else the project's linter on those files (`eslint <files>`, `biome check <files>`). Skip a tool that isn't installed.
3. **Tests:** run only tests related to those files, with one runner. Prefer `npm run test:ai -- --findRelatedTests <files>`, else `jest --findRelatedTests <files>`. Vitest: `vitest related --run <files>` (with the same `--reporter` as `test:ai`); `related` can't go through `vitest run`.
4. **Type check:** in a TS project, run the `typecheck` script or `npx tsc --noEmit` once, last, after lint and tests pass. It can't be scoped, so fix errors in the step-1 files and only mention errors elsewhere.
5. **Result:**
   - **Pass:** exit 0 *and* output shows files linted and tests ran (0 tests or 0 files is not a pass). Report the files covered and the `tsc` result, including whether any errors belong to edited files.
   - **Fail:** fix the cause and rerun. Never disable rules or skip tests.
   - **Nothing to run:** no linter or runner, or no JS/TS files changed. Finish; don't claim a pass.
   - **No related tests** (Jest: "No tests found"): not a failure. Name the files without tests; don't claim they were tested.

Whole-project runs only if the user asks.
