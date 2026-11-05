#!/usr/bin/env bash
# PreToolUse guard for GitHub MCP create_pull_request.
# Blocks PRs whose diff against their base is over PR_DIFF_LIMIT lines
# (default 1000) and tells Claude to split the work into a PR stack.
# Fails open: if the diff can't be measured, the PR is allowed.

LIMIT=${PR_DIFF_LIMIT:-1000}
input=$(cat)
base=$(jq -r '.tool_input.base // empty' <<<"$input")
head=$(jq -r '.tool_input.head // empty' <<<"$input")
[[ -n "$base" && -n "$head" ]] || exit 0
head=${head##*:} # fork PRs pass "owner:branch"

git rev-parse --git-dir >/dev/null 2>&1 || exit 0
git fetch -q origin "$base" "$head" 2>/dev/null

ref() { git rev-parse -q --verify "origin/$1" >/dev/null && echo "origin/$1" ||
        { git rev-parse -q --verify "$1" >/dev/null && echo "$1"; }; }
b=$(ref "$base") h=$(ref "$head")
[[ -n "$b" && -n "$h" ]] || exit 0

total=$(git diff --numstat "$b...$h" -- . \
  ':!*package-lock.json' ':!*.lock' ':!pnpm-lock.yaml' ':!*.snap' \
  | awk '$1 != "-" {s += $1 + $2} END {print s + 0}')

(( total > LIMIT )) || exit 0

cat >&2 <<EOF
Blocked: PR $head -> $base changes $total lines (limit $LIMIT; lockfiles and snapshots excluded).
Split it into a stack of PRs, each under $LIMIT lines, then create them:
1. Group the changes by concern in dependency order (e.g. schema/types -> core logic -> API/UI -> tests that need it). Each slice must build and pass its own tests.
2. Make one branch per slice, each cut from the previous one: $base <- ${head}-1 <- ${head}-2 <- ... Move commits or files with git (cherry-pick, checkout <ref> -- <paths>); don't rewrite code to fit.
3. Push every branch, then create the PRs bottom-up with create_pull_request, setting base to the previous branch (the first one targets $base).
4. Start each PR body with a "Stack" list linking all PRs in order and marking the current one; update earlier PR bodies once later PRs exist.
5. Leave the original branch $head untouched until the stack is created.
If one indivisible change (e.g. generated code) is over the limit on its own, stop and ask the user instead of splitting it.
EOF
exit 2
