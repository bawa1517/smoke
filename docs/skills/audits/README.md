# audits

Read-only audits that produce a page. Each skill's tier is a row in [`../skills.csv`](../skills.csv); the full list of categories is [`../README.md`](../README.md).

| Skill | What it does |
|---|---|
| [audit-agent-efficiency](audit-agent-efficiency/SKILL.md) | Read a finished agent's transcript, find the turns it wasted, and put a fix on disk for each one (a CLAUDE.md line, a script, a breadcrumb, a pattern) so the next run is fast. |
| [debuggability-audit](debuggability-audit/SKILL.md) | Find where a failure leaves no usable evidence: swallowed exceptions, context-free logs, silent fallbacks, error messages with no failing value. |
| [hk-arch-audit](hk-arch-audit/SKILL.md) | Score a codebase against eight agent-native principles, one sub-agent each, and write the result up as one page in writeup/. |
| [hk-autonomy-audit](hk-autonomy-audit/SKILL.md) | Judge whether an agent could take one area from symptom to verified fix with no person in the loop, and write up the gaps as one page in docs/loop_audits/ (the one audit page the repo commits). |
| [hk-code-quality-audit](hk-code-quality-audit/SKILL.md) | Find what nobody would miss and what reads as generated, and write it up as one HTML page scored out of 10: dead code, pasted templates, wrappers with one caller, scratch files, hardcoded hosts, unused packages. |
| [hk-chart-validation](hk-chart-validation/SKILL.md) | Check that the charts in a codebase tell the truth: chart type, axis baselines, aggregation, units, labels, tooltips and how they render in Chrome at each width; writes the findings as one HTML page with a score out of 10. |
| [hk-debug-readiness-audit](hk-debug-readiness-audit/SKILL.md) | Rank the flows in this codebase that most need a debug page, up to five, with a build brief for each, as one page in writeup/. |
| [hk-mobile-app-ui-validation](hk-mobile-app-ui-validation/SKILL.md) | Drive a native iOS or Android app on a device or simulator through the mobile MCP, screenshot every screen, measure touch targets, and write up mis-taps, clipped text and screens that trap the user as one HTML page with a score out of 10. |
| [hk-read-path-audit](hk-read-path-audit/SKILL.md) | Audit the documents an agent reads for a job, as one HTML page scored out of 10: their token cost, what they state twice, where they contradict each other or the code, what is read and never used, each with the exact edit; applies the edits when asked. |
| [hk-security-audit](hk-security-audit/SKILL.md) | Run scripts/security_audit.py over the repo, verify each hit by reading the code, and write up to ten security findings as one HTML page with a score out of 10: leaked secrets, endpoints without auth, credential mounts, OAuth tokens passed into sandboxes, egress defaulting to allow, shell=True calls. |
| [hk-test-case-audit](hk-test-case-audit/SKILL.md) | Write up this repo's test gaps as one HTML page scored per suite: what has no test, which tests pass with the code broken, which bill a provider, what to write first. Reads a directory or PR; runs the four suites when asked to score them. |
| [hk-ui-gaps-analysis](hk-ui-gaps-analysis/SKILL.md) | Read every frontend component that fetches or submits and write up the ones missing a loading, empty, error or pending state, or that leave the user at a dead end, as one HTML page with a score out of 10; the worst gaps are confirmed in Chrome. |
| [hk-web-app-ui-validation](hk-web-app-ui-validation/SKILL.md) | Walks a running web app in Chrome at three widths and writes up layout defects, dead ends, broken links, forms and accessibility failures as one page scored out of 10. |
| [silent-error-audit](silent-error-audit/SKILL.md) | Find failures that never reach the person using the UI: errors caught and only logged, runs stuck in PENDING, error fields no component reads, empty states shown over a failed run. |
| [skill-audit](skill-audit/SKILL.md) | Audit a skill under docs/skills and write up, as one HTML page, whether an agent can run it as written: a verdict, a score out of 10, and ranked findings each with a severity out of 5 and the fix to apply. Applies the rewrite when asked. |
