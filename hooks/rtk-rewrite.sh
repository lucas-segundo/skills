#!/usr/bin/env bash
# PreToolUse hook: rewrite Bash commands to `rtk <cmd>` for token savings.
# Adapted from rtk-ai/rtk hooks/claude/rtk-rewrite.sh. Never blocks a command:
# every error path exits 0 so the original command runs unchanged.
# Needs: rtk >= 0.23.0, jq. `rtk rewrite` exit codes:
#   0 rewrite found (auto-allow), 1 no equivalent, 2 deny rule, 3 ask rule.

export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

command -v jq >/dev/null 2>&1 || exit 0
command -v rtk >/dev/null 2>&1 || exit 0

INPUT=$(cat)
CMD=$(jq -r '.tool_input.command // empty' <<<"$INPUT")
[ -z "$CMD" ] && exit 0

REWRITTEN=$(rtk rewrite "$CMD" 2>/dev/null)
CODE=$?

case $CODE in
  0) [ "$CMD" = "$REWRITTEN" ] && exit 0 ;;
  3) ;;
  *) exit 0 ;;
esac

if [ "$CODE" -eq 3 ]; then
  jq -c --arg cmd "$REWRITTEN" \
    '.tool_input.command = $cmd | {hookSpecificOutput: {hookEventName: "PreToolUse", updatedInput: .tool_input}}' <<<"$INPUT"
else
  jq -c --arg cmd "$REWRITTEN" \
    '.tool_input.command = $cmd | {hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "allow", permissionDecisionReason: "RTK auto-rewrite", updatedInput: .tool_input}}' <<<"$INPUT"
fi
