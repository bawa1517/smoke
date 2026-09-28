---
name: hk-ui-gaps-analysis
description: "Read every frontend component that fetches or submits and write up the ones missing a loading, empty, error or pending state, or that leave the user at a dead end, as one HTML page with a score out of 10; the worst gaps are confirmed in Chrome. Triggers on: 'missing loading states', 'empty states', 'ui gaps', 'what happens when the request fails', 'dead ends', or /hk-ui-gaps-analysis."
allowed-tools: Bash, Read, Grep, Glob, Write, Agent, mcp__chrome-devtools__*
model: sonnet
generated: true
generated_from: taskit/taskit-backend/data/task_presets.json#ui-gaps-analysis
---

# UI gaps analysis

Finds the screens that go blank, freeze or lie when data is slow, missing or broken. The main work is reading the code: every component that talks to the network gets a row saying which of the four states it handles. The browser is used to confirm the worst rows, because a spinner that exists in code but never shows is still a gap. It changes no source file and touches no shared service.

Scope: states and dead ends (a delete with no undo, an action with no success signal, a route that shows a blank). Layout, contrast, navigation, links, forms and accessibility are `hk-web-app-ui-validation`, which walks the site in Chrome; this skill reads the code and confirms in Chrome only what the code made suspect.

The page is built as `docs/skills/knowledge/hk-writeup/SKILL.md` steps 3 to 5 say, in `docs/skills/knowledge/hk-writeup/SHELL.html`, in the voice of `docs/playbook/tone_and_taste.md`. Read the voice doc before writing a sentence.

## Does this apply?

Look for `.tsx`, `.jsx`, `.vue` or `.svelte` files under the project's source folders (skip `node_modules` and any orchestration or worktree state folder CLAUDE.md names). If there are none, say so in one chat line and stop; write no file.

## Workflow

**1. List the components that fetch or submit.** Grep the frontend for `fetch(`, `axios`, `useQuery`, `useMutation` and for imports of the project's API client modules (its API client folder, and any component or context that imports one or calls `fetch(` directly). Done when every hit's component is on a list.

**2. Fill the state table.** One row per component, four columns: loading, empty, error, pending submit. Each cell is yes, no, or n/a with the line that proves it (a `isLoading` branch, an empty-array branch, a `catch` that reaches the screen, a `disabled={isPending}`). Split the reading across haiku subagents by directory when the list passes 30, one message, in parallel, each returning rows in this shape; the judgment stays with you. Done when every row has four cells.

**3. Walk the dead ends.** For each screen a user can reach, ask what happens at the end of it: a delete with no confirmation and no undo, a modal that closes without saving, a 404 route that shows a blank, an action with no success signal, a spinner owned by a parent the child cannot reach. Read the router for the reachable screens.

**4. Confirm the worst gaps in Chrome.** Start the app with the workspace's dev command (CLAUDE.md). With the Chrome DevTools MCP, `mcp__chrome-devtools__navigate_page` to the screen; `mcp__chrome-devtools__emulate` with `networkConditions` "Slow 3G" to watch the loading state; open a board or list with nothing in it for the empty state; `mcp__chrome-devtools__emulate` with `networkConditions` "Offline" and trigger the action for the error state, then omit `networkConditions` to restore. The backend other people are using stays up. `mcp__chrome-devtools__take_screenshot` each with `filePath` under `writeup/shots/`. Confirm at least every severity 5 and 4 finding; say on the page which findings were confirmed and which were read only.

**5. Verify, then cut.** Reopen each cited line. Drop anything a maintainer would not change. Up to ten findings; fewer is fine, none means the page says the states are covered.

**6. Build the page** at `writeup/ui-gaps-analysis-<subject>.html` at the repo root (`$(git rev-parse --show-toplevel)/writeup/`, gitignored; create the directory if missing), in the order under Page order below. Embed a screenshot from `writeup/shots/` as a base64 data URI where it shows the gap, then delete `writeup/shots/`.

**7. Report back** in one chat line: where the page went, the score, and the count by severity.

## Page order

1. Kicker "UI gaps analysis", the app as the title, chips for the component count, the number confirmed in Chrome, and the model.
2. **Verdict**: one sentence with the score out of 10 and what set it (the band table below), one naming the worst finding, then the state table as a `.tbl`.
3. **Findings**, one `section` per band: Stuck or misled (severity 5 and 4), Waiting blind (3), Nits (2 and 1). Each finding is one `details.row`: `.row-name` is the severity in words ("severity four"), `.row-status` the title as a sentence; the `.dbody` says what the user sees and what they should, quotes the source lines in a `pre`, says whether Chrome confirmed it, and ends with `file:lines` in `.mono`.
4. `.foot`: replace the `.said` sentence with one saying how many components were read, how many gaps were confirmed in Chrome on the named model, and that nothing was changed.

## The checklist

Per component that fetches or submits, and per reachable screen:

- While data loads, the screen shows that it is loading, in the place the data will appear.
- When the list is empty, the screen says so and offers the next step, instead of a blank area or a stale previous result.
- When the request fails, the user sees a message where they were looking, and can retry; nothing throws to a white screen (an error boundary catches render errors).
- While a submit is in flight, the button is disabled or shows progress, and a second click does not send twice.
- After a submit, the user is told it worked, and the screen reflects the change without a reload.
- A destructive action asks first or can be undone.
- Unknown routes and missing ids show a page that says so and links back.

## Severity and score

Severity is 1 to 5, 5 worst: **5** for data loss or a white screen; **4** for a silent failure or a double submit; **3** when the user waits without knowing why or must reload to see their change; **2** when the state exists but is poorly placed or worded; **1** for a wording nit.

The findings set the band; judgment picks the number inside it and the verdict sentence says what moved it. When a set matches two rows, the lower band applies.

| Findings | Band |
|---|---|
| none | 10 |
| nothing above severity 2, or one severity 3 | 8 to 9 |
| two or three severity 3, or one severity 4 | 6 to 7 |
| two severity 4, or four or more severity 3 | 4 to 5 |
| three or more severity 4 | 2 to 3 |
| any severity 5 | 0 to 1 |

## Example: in harness-kit

- The API client folder is `taskit/taskit-frontend/src/services/` (`harness/HarnessTimeService.ts` and `integration/IntegrationService.ts`); `contexts/AuthContext.tsx` also calls `fetch(` directly.
- The router is `taskit/taskit-frontend/src/App.tsx`.
- The dev command is `./dev.sh` at the repo root, which serves the frontend at http://localhost:9200 and the Django API on 9100.
- The orchestration and worktree state folder to skip is `.odin`.
