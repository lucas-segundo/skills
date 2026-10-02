# Verification

Run this as the last step after editing JS/TS files.

1. **Scope:** only the JS/TS files you created or edited for the current prompt, including any changed by commands you ran (codemods, `--fix`, renames). Skip deleted files. Leave out files changed by earlier prompts, by the user, or by other branches. Never the whole project. An empty list means there is nothing to verify.
2. **AI scripts:** if `package.json` has `lint:ai` / `test:ai`, prefer them for steps 3–4. They run the same checks with less output:
   - lint: `npm run lint:ai -- <files>`
   - Jest: `npm run test:ai -- --findRelatedTests <files>`
   - Vitest: `related` can't go through `vitest run`, so call `vitest related --run <files>` directly, with the same `--reporter` as `test:ai`.
3. **Lint:** if the project has a linter, run it on those files (`eslint <files>`, `biome check <files>`). Use the project's own script or binary; skip a tool that isn't installed.
4. **Tests:** if the project has a test runner, run only the tests related to those files (`vitest related --run <files>` or `jest --findRelatedTests <files>`). Use one runner, whichever the project has.
5. **Result:**
   - **Pass:** exit code 0 *and* the output shows the files were linted and tests ran (0 tests or 0 files checked is not a pass). State that lint/tests passed, and which files they covered.
   - **Fail:** fix the cause and rerun. Do not finish, disable rules, or skip tests to make it pass.
   - **Nothing to run:** no linter or test runner in the project, or the prompt changed no JS/TS files. Skip this step and finish; don't claim it passed.
   - **No related tests:** the touched files have no tests (Jest exits 1 with "No tests found"). This is not a failure to fix: say which files have no tests and don't claim they were tested.
