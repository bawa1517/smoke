---
name: debuggability-audit
description: "Find where a failure leaves no usable evidence: swallowed exceptions, context-free logs, silent fallbacks, error messages with no failing value. Triggers on: 'is this debuggable', 'logging audit', 'exception handling audit', 'debuggability audit', or /debuggability-audit."
argument-hint: "[optional: directory to focus on]"
---

# Debuggability audit

Read the logging and exception handling in a directory and answer one question for each
catch block, error branch and log call: when this fires in production, can the person told
"X failed" find out why from what the system captured, without adding prints and re-running?

Scope: `$ARGUMENTS`, or the whole repo when empty. The page is
`writeup/debuggability-audit-<dir>.html` at the repo root, where `<dir>` is the basename of the
scoped directory, or `repo`. Nothing in the codebase changes. Whether the failure reaches the
person using the UI is `silent-error-audit`; whether an agent could close the loop on an area
is `hk-autonomy-audit`; which flows need a debug page is `hk-debug-readiness-audit`. This
skill asks only what the logs will hold when it breaks.

## How to run

1. Dispatch one subagent on the strongest model available with the prompt below, verbatim, plus
   the scope. It reads only. The strongest model, unlike the sibling audits, because every
   finding here is the call "does a caller upstream already log this", which a cheaper model
   answers from the catch block alone.
2. Take its findings, read `docs/playbook/tone_and_taste.md`, and build the page as
   `docs/skills/knowledge/hk-writeup/SKILL.md` steps 3 to 5 say, in
   `docs/skills/knowledge/hk-writeup/SHELL.html`, with the sections below. Severity and the
   score are content here, so they go on the page as sentences and a plain table.
3. Say in chat where the page is, the score, and the finding count by severity.

## Audit prompt

Scope of analysis: try/except and try/catch blocks, promise `.catch()` handlers, error
callbacks, process-level handlers (`uncaughtException`, `unhandledRejection`), logger setup and
use, error-to-HTTP mapping (exception filters, error middleware), retry and fallback paths, and
log file or transport setup.

Look for each of these classes by name:

1. **Silent swallowing.** Empty catch blocks, `except: pass`, catches that return a default or
   `None` with no log.
2. **Evidence destruction.** Rethrowing or wrapping while dropping the original stack or cause;
   logging `e.message` and discarding the stack and response body; `str(e)` on an HTTP error
   that hides the payload.
3. **Context-free logging.** An error logged with no identifier (which run, which task, which
   request), so the line cannot be joined to the operation that failed.
4. **Wrong level or stream.** Real errors at debug or info, or on `print` / `console.log`, so they
   miss the error log; a warning where the operation actually failed.
5. **Silent fallbacks and retries.** The operation "succeeds" through a fallback and the first
   error is never recorded; retries log each attempt but not why they finally gave up.
6. **Broad catches that flatten distinct failures.** Timeout, bad input, missing config and
   network error all become one message.
7. **Unreachable or unjoinable evidence.** No timestamps or correlation ids; detail held in a
   variable that is never persisted; errors written where no documented log path covers.
8. **Async escape hatches.** Unawaited promises, fire-and-forget tasks, handlers whose rejections
   reach nobody, or only a process handler with no context.
9. **Error messages with no failing value.** "invalid input", "not found", without the input
   or the key that failed.

An error path that reports success while the operation failed belongs to the
`silent-error-audit` skill: note any you pass in one line at the end and leave them out of the
findings.

For each candidate, read the surrounding code and confirm the loss is real: no caller upstream
logs it, the logger in that file really drops the stack, the fallback really hides the error.
A catch that is fine (fully logged with context nearby, or the exception is expected and never
matters) is not a finding. Report at most ten. When one pattern repeats (fourteen copies of the
same context-free catch), report it once with the count and three representative locations.

Severity, 1 to 5, 5 worst, judged on what the person debugging is left with:

- **5** — the failure leaves nothing: an empty catch, a fallback that hides the first error, a
  rejection that reaches nobody.
- **4** — something is logged but it cannot be joined to the run, task or request that failed,
  or the stack and payload are gone.
- **3** — the evidence exists but at the wrong level or stream, or one message covers several
  distinct failures.
- **2** — the evidence is there and joinable but the message lacks the failing value.
- **1** — a nit: wording, a missing timestamp where the transport adds one anyway.

Return, for each finding: a title that is a sentence; the location as basename plus line range
(`transfer.py:45-58`); the literal catch or log line; the severity with one clause on why; one
or two sentences on what evidence is lost; one or two sentences on what the person debugging
will see, and where practical, how a temporary probe test would show it ("force `<call>` to
throw and assert the error log carries the run id; today it carries nothing"). Then: two or
three observations on the codebase's logging habits, two or three places where errors are
captured well, and one paragraph a person could paste into a coding agent to fix the findings
in order, test-first where a probe test exists.

## Score, 0 to 10

The findings set the band, judgment picks the number inside it, and one sentence beside the
score says what moved it. When a set matches two rows, the lower band applies.

| Findings | Band |
|---|---|
| none | 10 |
| nothing above severity 2, or one severity 3 | 8 to 9 |
| two or three severity 3, or one severity 4 | 6 to 7 |
| two severity 4, or four or more severity 3 | 4 to 5 |
| three or more severity 4 | 2 to 3 |
| any severity 5 | 0 to 1 |

## What goes on the page

1. Kicker "Debuggability audit", the scoped directory as the title, chips for the commit and
   the model that read it.
2. Two or three sentences on what the audited code does. Then one bold sentence with the score
   out of 10 and the sentence that derives it. Then a `.tbl` in `.tblwrap` with the finding
   count by severity.
3. Findings, ranked by severity, each a `<details class="row">`: `.row-name` is the severity in
   words ("severity four"), `.row-status` is the title. The body holds what is lost, what the
   debugger sees, the literal line in a `<pre>`, and the location in `.mono`.
4. Observations, then what already works, as short lists.
5. The fix prompt, as one paragraph.
6. Footer `.said`: read by the named model at the named commit; nothing was run or changed.
