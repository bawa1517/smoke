# RESUME — agent-readiness

Read order: this file → `board.csv` → `log.md`. The board holds the state; `mission-control.html` is rendered from it.

## Before you write anything the owner reads

Read `docs/playbook/tone_and_taste.md` before writing a page or message the owner reads, and check the final paragraph against it before sending.

## What this initiative is

This initiative sets up the workspace around the Taskwell static app so a future agent can orient itself, verify changes, and find the current work. Setup is complete for this pass when the kit files are copied, the root entrypoint draft and decisions are ready, and the readiness board names remaining work.

## ⏭️ Next action

There is no active Taskwell API work. The user clarified that the FastAPI contract interview was a demo and asked to leave it there. The decisions are recorded in the FastAPI contract resume note for reference; no OpenAPI YAML or implementation code was created. Resume only if the user asks to turn the demo into real project work.

## Settled decisions (do not re-open)

- The proposed API was for the Taskwell browser UI, for one local user, with no authentication, served from the same origin and bound to loopback only.
- The proposed resource was `Task` with `id`, `text`, and `completed`. Clients would supply positive integer IDs. Text would be trimmed and contain 1–100 Unicode code points. IDs would be immutable; unknown request fields, nulls, and empty PATCH bodies would be rejected.
- The proposed routes were `GET /tasks`, `POST /tasks`, and `GET`, `PATCH`, and `DELETE /tasks/{task_id}`. List results would be newest first by server-recorded creation time, without pagination or filters. Create would accept optional `completed` defaulting to `false`; duplicate existing IDs would return `409`, while deleted IDs could be reused. PATCH would accept either or both `text` and `completed`.
- Successful operations would return `200` with Task objects (including the deleted object for DELETE); invalid input would use FastAPI’s `422`, and missing tasks would return `404`. Domain error details would be stable human-readable strings.
- The proposed persistence was local SQLite across restarts, with a fresh install starting empty. Existing browser `localStorage` data would remain unused. The deliverable discussed was OpenAPI YAML version `1.0.0`, with no implementation code.
- These were design decisions for a demo exercise only. The user asked to leave the exercise parked; no contract file was authored.

## Workspace inspection and baseline

The workspace root contains `app.js`, `index.html`, and `styles.css`. They implement a browser-only task list with starter tasks and `localStorage` persistence; no package manifest, test runner, server, environment template, README, entrypoint, `.gitignore`, docs, scripts, or log configuration was found. The `.git` directory is empty: `git status --short --branch` and `git remote -v` both failed with “not a git repository.” No env, key, pem, or credential files appeared in the listing. There are no inner repos or repo-to-repo links.

| Area | Before scaffolding | Evidence |
|---|---:|---|
| Agent entrypoints | 0/10 | No CLAUDE.md, AGENTS.md, or docs index. |
| Proof and verification | 0/10 | No tests, gate, or test instructions. |
| Debugging readiness | 0/10 | No logs, diagnostic tools, or protocol. |
| Knowledge compounding | 0/10 | No breadcrumbs, patterns, or repeated-error ledger. |
| Disk-anchored work | 0/10 | No tracker or scratch convention. |
| Hygiene | 2/10 | No obvious secret or temp files in listing; no .gitignore or README to check. |
| Cost and delegation | 0/10 | No agent guidance or cost record. |
| Human legibility | 1/10 | Source/UI text exists, but no setup or operator docs. |
| Skills and audits | 0/10 | No workspace skills, presets, or audit findings. |
| Running it locally | 2/10 | Browser app can be opened from HTML, but no setup guide, stack command, config template, or sample-data guide. |
| Guardrails | 0/10 | No entrypoint or enforced boundary. |
| Measured readiness | 0/10 | No scenarios or proof report. |

## Progress and cost (estimates)

- Step 0: copied the mission-control template, filled its initial verdict, and rendered it. Cost: current model; approximately 3 tool calls, token count unavailable.
- Steps 1–2: listed the workspace, read the three app files, attempted the permitted Git status and remote checks, and scored the checklist above. Cost: current model; approximately 4 tool calls, token count unavailable.
- Step 3: copied 124 kit files and created the seeded workspace docs folders plus the Claude hooks. Cost: current model; approximately 4 tool calls, token count unavailable. The copy script recorded the kit commit as `unknown` because the source directory has no readable Git commit.
- Step 4: wrote and revised a 93-line CLAUDE.md draft from the code and kit template. A read-only claims check found the test-guide board claim premature, the diagnostics claim too broad, and the ownership wording unclear; those lines now name the checklist, distinguish app diagnostics from kit audits, and state the owner choice explicitly. Cost estimate: current model plus one read-only review agent; approximately 7 tool calls, token count unavailable.
- Step 5: put the two scaffold choices and three kit learnings on the board, and rendered mission control. Cost: current model; approximately 2 tool calls, token count unavailable.
- The Taskwell API contract interview was a demo. The user asked to leave it parked; its agreed design decisions are recorded for reference, and no OpenAPI contract or implementation was created.
