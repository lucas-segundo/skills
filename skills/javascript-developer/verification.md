# Verification

Run this as the last step after editing JS/TS files.

1. **Scope:** only the files you changed or created in this task. Never the whole project.
2. **Lint:** if the project has a linter, run it on those files (`eslint <files>`, `biome check <files>`). Use the project's own script or binary; skip a tool that isn't installed.
3. **Tests:** if the project has a test runner, run only the tests related to those files (`vitest related --run <files>` or `jest --findRelatedTests <files>`). Use one runner, whichever the project has.
4. **Result:**
   - **Pass:** state that lint/tests passed, and which files they covered.
   - **Fail:** fix the cause and rerun. Do not finish, disable rules, or skip tests to make it pass.
   - **Nothing to run:** say no linter or test runner was found. Do not claim it passed.
