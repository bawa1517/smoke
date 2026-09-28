#!/usr/bin/env python3
"""PreToolUse guard: block writes into the folders this workspace builds
around but never edits, and the git operations that lose other agents' work.

Fill PROTECTED with the repo folders the scaffold listed. Everything else in
this file is generic. The README next to it says what it blocks and how to
work with it.
"""
import json
import os
import re
import sys

# The folders an agent may read, search and run, but never write to. One
# entry per repo folder, relative to the workspace root.
PROTECTED = (
    # "some-repo",
)

# Commands blocked wherever they point. Add this workspace's paid-test
# invocations here if it has any.
COMMAND_PATTERNS = [
    (re.compile(r"\bgit\s+stash\b"),
     "git stash in a shared checkout loses other agents' work; use a branch or a temporary commit"),
    (re.compile(r"\bgit\s+reset\s+--hard\b"),
     "git reset --hard throws away work other agents may be holding in this checkout"),
    (re.compile(r"\bpush\b.*(?:--force\b|-f\b)"),
     "a force push rewrites history other people have already pulled"),
]

# Bash commands that write to a filesystem target.
WRITE_CMD = re.compile(r"\b(?:sed\s+-i|cp|mv|rm|touch|tee)\b")

# Redirection into a path: `... > path` or `>> path`. A `>` that follows
# `=` or another `>` is text (`==>` in a grep pattern), not a redirect.
REDIRECT = re.compile(r"(?<![=>])>>?\s*([^\s;&|]+)")

# A heredoc body: from `<<WORD` (quoted or not) to the line holding WORD.
HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n.*?^\1\s*$", re.S | re.M)

# Boundaries between simple commands: `;`, `&&`, `||`, `|`, newlines.
SPLIT = re.compile(r"\|\||&&|[;|\n]")

EDIT_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit")


def block(reason: str) -> None:
    sys.stderr.write(f"blocked by .claude/hooks/guard.py: {reason}\n")
    sys.exit(2)


def path_in_protected(path: str, cwd: str) -> str | None:
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    real = os.path.realpath(path)
    for repo in PROTECTED:
        repo_real = os.path.realpath(os.path.join(cwd, repo))
        if real == repo_real or real.startswith(repo_real + os.sep):
            return repo
    return None


def check_edit(tool_input: dict, cwd: str) -> None:
    file_path = tool_input.get("file_path", "")
    if not file_path:
        return
    repo = path_in_protected(file_path, cwd)
    if repo:
        block(
            f"edits inside {repo}/ are its owners' call; put a suggestion on "
            "the readiness board instead."
        )


def candidate_paths(command: str) -> list[str]:
    """Paths a command may write to: every redirect target, plus, in each
    simple command that has a write verb, the tokens after that verb which
    name a protected folder. Heredoc bodies are text, not commands, and are
    dropped first, so a script that merely mentions a repo goes through."""
    command = HEREDOC.sub("", command)
    paths = [m.group(1) for m in REDIRECT.finditer(command)]
    for simple in SPLIT.split(command):
        verb = WRITE_CMD.search(simple)
        if not verb:
            continue
        for token in simple[verb.end():].split():
            token = token.strip("'\"")
            if any(token == repo or token.startswith(repo + "/")
                   or f"/{repo}/" in token or token.endswith("/" + repo)
                   for repo in PROTECTED):
                paths.append(token)
    return paths


def check_bash(tool_input: dict, cwd: str) -> None:
    command = tool_input.get("command", "")
    if not command:
        return
    # A heredoc body is text: a doc that quotes "git stash" is not a stash.
    for pattern, reason in COMMAND_PATTERNS:
        if pattern.search(HEREDOC.sub("", command)):
            block(reason)
    for path in candidate_paths(command):
        repo = path_in_protected(path, cwd)
        if repo:
            block(
                f"writing into {repo}/ from Bash is its owners' call; put a "
                "suggestion on the readiness board instead."
            )


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    cwd = payload.get("cwd") or os.getcwd()

    if tool_name in EDIT_TOOLS:
        check_edit(tool_input, cwd)
    elif tool_name == "Bash":
        check_bash(tool_input, cwd)

    sys.exit(0)


if __name__ == "__main__":
    main()
