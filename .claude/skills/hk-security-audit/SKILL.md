---
name: hk-security-audit
description: "Run scripts/security_audit.py over the repo, verify each hit by reading the code, and write up to ten security findings as one HTML page with a score out of 10: leaked secrets, endpoints without auth, credential mounts, OAuth tokens passed into sandboxes, egress defaulting to allow, shell=True calls. Triggers on: 'security audit', 'scan for vulns', 'is this code safe', or /hk-security-audit."
argument-hint: "[directory to scan, default: repo root]"
allowed-tools: Bash, Read, Grep, Glob, Write
generated: true
generated_from: taskit/taskit-backend/data/task_presets.json#security-audit
---

This skill lives in `docs/skills/audits/hk-security-audit/`. Read `docs/skills/audits/hk-security-audit/SKILL.md` and follow it exactly.

Every supporting file it mentions (REFERENCE.md, templates, `scripts/`, examples) sits beside it in that directory. Wherever it says "this skill's directory" or uses a path relative to itself, resolve it against `docs/skills/audits/hk-security-audit/`.
