---
name: hk-arch-audit
description: "Score a codebase against eight agent-native principles, one sub-agent each, and write the result up as one page in writeup/."
argument-hint: "[optional: one principle, e.g. 'action parity' or '1']"
disable-model-invocation: true
---

# Agent-native architecture audit

Eight principles, one sub-agent per principle, one page at `writeup/arch-audit-<repo>.html`
where `<repo>` is the basename of `$(git rev-parse --show-toplevel)`.

| # | Principle | What it asks |
|---|---|---|
| 1 | Action parity | Whatever the user can do, the agent can do |
| 2 | Tools as primitives | Tools provide capability, not behaviour |
| 3 | Context injection | The system prompt carries live app state |
| 4 | Shared workspace | Agent and user work on the same data |
| 5 | CRUD completeness | Every entity has create, read, update and delete |
| 6 | UI integration | Agent actions show up in the UI at once |
| 7 | Capability discovery | Users can find out what the agent can do |
| 8 | Prompt-native features | Features are prompts defining outcomes, not code |

## 1. Pick the principles

`$ARGUMENTS` empty means all eight. Otherwise match it to one row: a number, or a word from the
name (`action parity`, `tools`, `primitives`, `context`, `injection`, `shared`, `workspace`,
`crud`, `ui`, `integration`, `discovery`, `prompt`, `features`).

## 2. Run the sub-agents

Read `references/agent-prompts.md` in this skill's directory. Launch one sub-agent per chosen
principle, all in a single message, with the Agent tool, `subagent_type: general-purpose`,
`model: sonnet`, passing the output shape from the top of that file plus the principle's own
section. Each returns an inventory table, a score line `### Score: X/Y (percentage%)`, the
gaps, and what to change.

Done when every launched sub-agent has returned a `### Score:` line. A sub-agent that returns
prose without one is re-run once with the same prompt.

## 3. Build the page

Read `docs/playbook/tone_and_taste.md`, then build the page as
`docs/skills/knowledge/hk-writeup/SKILL.md` steps 3 to 5 say, in
`docs/skills/knowledge/hk-writeup/SHELL.html`. On the page, in order:

1. Kicker "Agent-native audit", the repo name as the title, chips for the commit and the
   principles audited.
2. A table with one row per principle audited: the score, the percentage, and one sentence
   saying what the score means in this codebase ("the agent can do 12 of 20 things a user can;
   the eight missing are all board edits"). Under it, one sentence with the overall percentage
   when all eight ran.
3. What to change, in order of impact: one sentence per item, only items a sub-agent found,
   each naming the principle and the file.
4. What already works, only where it is worth copying elsewhere; skip the section otherwise.
5. Each sub-agent's report as a `<details class="row">` with the principle as `.row-name` and
   its score line as `.row-status`.

Done when `writeup/arch-audit-<repo>.html` exists with one row per principle audited. Say in
chat where it is and the overall percentage.
