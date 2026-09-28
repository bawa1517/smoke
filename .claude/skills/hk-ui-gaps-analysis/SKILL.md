---
name: hk-ui-gaps-analysis
description: "Read every frontend component that fetches or submits and write up the ones missing a loading, empty, error or pending state, or that leave the user at a dead end, as one HTML page with a score out of 10; the worst gaps are confirmed in Chrome. Triggers on: 'missing loading states', 'empty states', 'ui gaps', 'what happens when the request fails', 'dead ends', or /hk-ui-gaps-analysis."
allowed-tools: Bash, Read, Grep, Glob, Write, Agent, mcp__chrome-devtools__*
model: sonnet
generated: true
generated_from: taskit/taskit-backend/data/task_presets.json#ui-gaps-analysis
---

This skill lives in `docs/skills/audits/hk-ui-gaps-analysis/`. Read `docs/skills/audits/hk-ui-gaps-analysis/SKILL.md` and follow it exactly.

Every supporting file it mentions (REFERENCE.md, templates, `scripts/`, examples) sits beside it in that directory. Wherever it says "this skill's directory" or uses a path relative to itself, resolve it against `docs/skills/audits/hk-ui-gaps-analysis/`.
