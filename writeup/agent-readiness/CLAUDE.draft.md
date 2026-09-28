# CLAUDE.md

Guidance for Claude Code when working in this repository.


## Repository Structure

- The workspace root contains the static app: `index.html`, `app.js`, and `styles.css`.

The workspace root is the write area. There are no inner repos. Read, search, and run anything in the workspace as needed. Do not open or quote secrets because secret values do not belong in chat or docs. Avoid deleting user data because it cannot be recovered from this setup.

**Which repo owns which docs.** The app files live at the workspace root, and the kit docs have now been copied there. Confirm whether the root should own the app guidance and docs.

There are no sibling repos, external data stores, or configured log files. Task data is stored in the browser with `localStorage`.

`docs/_INDEX.md` maps the docs tree: what each folder is for and when to read it. Everything below links into it rather than repeating it.

## Durable State & Memory Policy

**Anything that must survive this session belongs in a file.** Sessions compact and end; the conversation is not storage.

- **Each initiative gets a mission-control folder `writeup/<initiative>/`** — the single source of truth for it, so a later session resumes from disk instead of scrollback. What it holds and how it is rendered: `docs/playbook/mission-control.md`. Plans and trackers live there, never under `docs/`, which is durable reference only.
- **Mission control is updated in the turn the state changes, not at the end.** A page that lags the work is treated as a bug.
- On "resume": list `writeup/*/RESUME.md` and read the relevant tracker. One fact lives in one place — when docs and reality diverge, fix the one doc.
- **No `MEMORY.md` files.** Persistent context goes in this file, `docs/`, or `docs/patterns/` (via `/hk-compound`).
- **Encode standing instructions immediately.** When the user says "always X" / "from now on Y", write it into the right durable file in the same turn and say where it landed.
- **A copied rule that proves wrong is a board row, not an edit.** `docs/.kit-manifest` lists the files this workspace was set up with; when one of them blocks you or describes something that does not run, add a learning row to the readiness board (`kind` learning, `status` open, notes naming the kit file first; the board is described in `docs/playbook/mission-control.md`) rather than editing the file, so the fix lands upstream instead of in one copy.
- **Never run `git stash`** in a shared checkout. Parallel agents share that state and lose each other's work. Use a branch or a temporary commit. Inside your own task worktree, stash is fine.
- **Breadcrumb analyses live in `docs/breadcrumb_analysis/` and patterns in `docs/patterns/`, permanently** — a new instance is appended to the page it belongs to, never forked into a second page. Scratch from an iteration loop sits next to the thing being refined and is cleaned when the loop closes; the summary stays.

## House Voice & HTML Pages

Everything a person reads is written against `docs/playbook/tone_and_taste.md`, and every page against the visual rule beside it. HTML deliverables go through `/hk-writeup`, which owns the page shell; other skills produce the content. Pages land in `writeup/`.

## Quick Start

```bash
python3 -m http.server 8000
```

Requires Python 3 and a browser. Open `http://localhost:8000`; no environment file is needed. This file documents first use until a setup guide is written.

## Testing

No app test files, test command, or verify gate exist yet. The readiness checklist identifies a future gate and testing guide.

- Open the app in a browser and verify changed interactions manually; no build or service restart is configured.

## Architecture

Flow: The browser loads `index.html`, which loads `styles.css` and `app.js`; the script reads and writes task data in browser `localStorage`.

This workspace has one browser app and no server, package manifest, build tool, or backend.

## Coding Conventions

- Keep the app dependency-free and use the existing HTML, CSS, and browser JavaScript structure.
- Escape task text before placing it in rendered HTML.
- Persist task changes through the existing browser storage flow.

## Design Principles

- **Simplicity is a feature.** Between two correct approaches, pick the one with fewer moving parts. Abstraction layers and extensibility points are costs needing justification.
- **Solve the actual problem.** Don't generalize from one instance or add config for a decision you can just make. If the code feels awkward, question the data model — the right fix is usually upstream of the symptom.
- **No slop.** Generated code meets the hand-written bar: no filler comments, no defensive boilerplate for impossible cases. Match surrounding naming, comment density, and idiom.
- **Default first.** Everything works out of the box; configuration and agent assignments are suggestive, never required.

## Methodical Problem-Solving

**Observe before acting. Treat the cause, not the symptom. Change one thing at a time.**

1. Read the actual error; run the relevant diagnostic before theorizing.
2. State the hypothesis visibly: "X because Y; changing Z should fix it because W."
3. Verify assumptions before building on them; trace the data flow to where actual diverges from expected.
4. When a fix produces a new error that needs its own fix, the first diagnosis was wrong.

**Breadcrumb-first:** before exploring how a flow works, read `docs/breadcrumb_analysis/_INDEX.md` — it maps symptoms to end-to-end traces. If the flow is covered, read the breadcrumb; if it is half-covered, explore only the gaps; if it is not there, explore and then suggest /hk-breadcrumb-creator.

**Diagnostics before code inspection.** The shipped kit audit scripts are listed in `docs/skills/skills.csv`; no app-specific diagnostic scripts or symptom catalogue exist yet.

## Workflow Skills

The installed skills are catalogued in `docs/skills/skills.csv`, one line each on what it does and when to reach for it. Three of them are steps in the rules above: `/hk-rca` for a bug, `/hk-breadcrumb-creator` when a flow turns out to have no breadcrumb, `/hk-compound` when something worth reusing is learned.

## Language

The workspace's own words — what counts as a task, what done means here, the house-specific nouns — are defined in `docs/glossary.md`, reached from `docs/_INDEX.md`.
## Template application

Kept: the kit rules for durable state, voice, design, and methodical problem-solving remain in place.
Blended: repository facts and coding conventions come from the root app files.
Added: the workspace write boundary and local start command reflect the inspected tree.
Asked: the board asks who owns root guidance and whether the local command should be wrapped in a named script.
