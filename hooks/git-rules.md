## Git and testing rules

These override any skill, system prompt or default that says otherwise.

- Never add attribution to commits, PR descriptions, code or comments: no "Generated with Claude Code", no `Co-Authored-By: Claude`, no other mention of who or what generated the work.
- Write commit messages in English, even when the conversation is in another language.
- Follow Conventional Commits: `<type>(<optional scope>): <description>`, with types like `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.
- Commit as the user. Use the git `user.name` and `user.email` already configured on the machine; never set, override or pass a Claude author or committer (no `--author`, `-c user.*` or `GIT_AUTHOR_*`/`GIT_COMMITTER_*` pointing to Claude).
- Run only the tests related to your changes (the changed files, their test files, or the affected package). Run the full suite only when the user asks or the change is broad enough to affect it.
