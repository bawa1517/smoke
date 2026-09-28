#!/usr/bin/env python3
"""Regenerate the board-driven sections of mission-control.html from board.csv.

board.csv is the only place task, bug, decision, suggestion and learning
state is written. Five kinds share one row shape (id, kind, title, status,
priority, depends_on, closes_when, notes) and render as four sections:

  decision   -> "What needs the owner": numbered, priority first, open only;
                decided rows behind one fold.
  task, bug  -> "The work": one table, a kind label per row, open rows by
                priority then dependency order, closed rows behind one fold.
                The first open row is what happens next. A bug row exists
                only when no task closes it; otherwise the task carries it.
  suggestion -> "Noticed inside the code": a plain list, not a table, one
                line per suggestion (title, then the file from notes in
                small mono). A suggestion is something a session noticed
                inside one of the workspace's repos that the scaffold must
                not change; it never carries a patch. Noted ones sit inside
                one fold; taken and dropped ones fold away under a second.
  learning   -> "Learnings for harness-kit": a plain list like suggestions.
                What a learning row is and how to write one is covered in
                the kit's `initiate-scaffold.md`, hard rule 6. Open ones
                sit in one fold; folded and dropped under a second.

Every row's notes sit behind a click (a <dialog>), never in the table cell.
Rows are named by title wherever the page lists them; ids are filing keys
for the detail dialog and depends_on, never a name shown to the reader.
The script rewrites the HTML between <!-- BOARD:START --> and <!-- BOARD:END -->.

Usage: python3 render_board.py   (from this directory)
"""
import csv
import html
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PAGE = HERE / "mission-control.html"
START, END = "<!-- BOARD:START -->", "<!-- BOARD:END -->"
PRIO_ORDER = {"P0": 0, "P1": 1, "P2": 2}
CLOSED = {"task": {"done"}, "bug": {"fixed", "worked around"}, "decision": {"decided"},
          "suggestion": {"taken", "dropped"}, "learning": {"folded", "dropped"}}
NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def in_words(n):
    return NUMBER_WORDS[n] if 0 <= n < len(NUMBER_WORDS) else str(n)


def esc(s):
    return html.escape(s or "")


def load():
    with open(HERE / "board.csv", newline="") as f:
        return list(csv.DictReader(f))


def is_closed(r):
    return r["status"] in CLOSED[r["kind"]]


def by_priority(rows):
    return sorted(rows, key=lambda r: PRIO_ORDER.get(r["priority"], 9))


def ordered_open_tasks(tasks, done_ids):
    """Ready tasks (no open dependency) by priority, then waiting ones."""
    open_tasks = [r for r in tasks if not is_closed(r)]
    ready = [r for r in open_tasks if not r["depends_on"] or r["depends_on"] in done_ids]
    waiting = [r for r in open_tasks if r not in ready]
    return by_priority(ready) + by_priority(waiting)


def pill(text):
    cls = {"done": "ok", "fixed": "ok", "decided": "ok", "worked around": "ok",
           "open": "warn", "blocked": "bad"}.get(text, "warn")
    return f'<span class="pill {cls}">{esc(text)}</span>'


def detail_button(r):
    return (f'<button class="more" onclick="document.getElementById(\'d-{esc(r["id"])}\').showModal()">'
            f'detail</button>')


def dialog(r):
    return (f'<dialog id="d-{esc(r["id"])}"><form method="dialog">'
            f'<p class="kicker">{esc(r["kind"])} · {esc(r["priority"])} · {esc(r["status"])}</p>'
            f'<h3>{esc(r["title"])}</h3>'
            f'<p><strong>Closes when.</strong> {esc(r["closes_when"]) or "—"}</p>'
            f'<p><strong>Notes.</strong> {esc(r["notes"]) or "—"}</p>'
            + (f'<p><strong>After.</strong> {esc(r["depends_on"])}</p>' if r["depends_on"] else "")
            + f'<p class="file">{esc(r["id"])}</p>'
            f'<button class="more">close</button></form></dialog>')


def table(rows, cols, numbered=False):
    out = ['<div class="tablewrap"><table><tr>']
    if numbered:
        out.append("<th>#</th>")
    out += [f"<th>{h}</th>" for h, _ in cols]
    out.append("<th></th></tr>")
    for i, r in enumerate(rows, 1):
        out.append("<tr>")
        if numbered:
            out.append(f'<td class="num">{i}</td>')
        for _, fn in cols:
            out.append(f"<td>{fn(r)}</td>")
        out.append(f"<td>{detail_button(r)}</td></tr>")
    out.append("</table></div>")
    return "\n".join(out)


def fold(summary, inner):
    return (f'<details class="fold"><summary><strong>{summary}</strong></summary>'
            f'<div class="fold-body">{inner}</div></details>')


def render(rows):
    tasks = [r for r in rows if r["kind"] == "task"]
    bugs = [r for r in rows if r["kind"] == "bug"]
    decisions = [r for r in rows if r["kind"] == "decision"]
    suggestions = [r for r in rows if r["kind"] == "suggestion"]
    learnings = [r for r in rows if r["kind"] == "learning"]
    done_ids = {r["id"] for r in tasks if is_closed(r)}
    title_by_id = {r["id"]: r["title"] for r in rows}
    out = []
    dialogs = [dialog(r) for r in rows if r["kind"] not in ("suggestion", "learning")]

    # --- owner ---
    open_d = by_priority([r for r in decisions if not is_closed(r)])
    closed_d = [r for r in decisions if is_closed(r)]
    out.append('<section id="owner"><h2 class="label">What needs the owner</h2>')
    if open_d:
        out.append('<p class="totals">Each row is one choice about the scaffold itself, with the answer I propose. Say yes, or say the other answer.</p>')
        out.append(table(open_d, [
            ("Priority", lambda r: esc(r["priority"])),
            ("Decision", lambda r: f"<strong>{esc(r['title'])}</strong>"),
            ("Proposal", lambda r: esc(r["closes_when"])),
        ], numbered=True))
    else:
        out.append('<div class="card"><p>Nothing right now.</p></div>')
    if closed_d:
        out.append(fold(f"{len(closed_d)} decided", table(closed_d, [
            ("Decision", lambda r: f"<strong>{esc(r['title'])}</strong>"),
            ("Status", lambda r: pill(r["status"])),
        ])))
    out.append("</section>")

    # --- work: tasks and bugs in one table, a kind label per row ---
    work = tasks + bugs
    open_w = ordered_open_tasks(work, done_ids)
    closed_w = [r for r in work if is_closed(r)]
    out.append('<section id="work"><h2 class="label">The work</h2>')
    out.append(f'<p class="totals">{len(work)} rows: {len(closed_w)} closed / {len(open_w)} open. '
               "Priority first, then dependency order; the first row is what happens next. "
               "A bug row is broken behaviour with no task around it; a task row names the bug it closes in its detail.</p>")

    def status(r):
        if r["depends_on"] and r["depends_on"] not in done_ids:
            after_title = title_by_id.get(r["depends_on"], r["depends_on"])
            return f'<span class="pill bad">after {esc(after_title)}</span>'
        return pill(r["status"])
    kind = lambda r: f'<span class="pill {"bad" if r["kind"] == "bug" else "warn"}">{esc(r["kind"])}</span>'
    if open_w:
        out.append(table(open_w, [
            ("Priority", lambda r: esc(r["priority"])),
            ("Kind", kind),
            ("What", lambda r: f"<strong>{esc(r['title'])}</strong>"),
            ("Closed when", lambda r: esc(r["closes_when"])),
            ("Status", status),
        ], numbered=True))
    else:
        out.append('<div class="card"><p>Nothing open.</p></div>')
    if closed_w:
        out.append(fold(f"{len(closed_w)} closed", table(closed_w, [
            ("Kind", kind),
            ("What", lambda r: f"<strong>{esc(r['title'])}</strong>"),
            ("Status", lambda r: pill(r["status"])),
        ])))
    out.append("</section>")

    # --- suggestions: a plain list, never a table, never a patch ---
    open_s = [r for r in suggestions if not is_closed(r)]
    closed_s = [r for r in suggestions if is_closed(r)]

    def suggestion_line(r):
        return (f'<li>{esc(r["title"])} <span class="file">{esc(r["notes"])}</span></li>')

    out.append('<section id="noticed"><h2 class="label">Noticed inside the code</h2>')
    if open_s:
        count = in_words(len(open_s)).capitalize()
        thing = "thing" if len(open_s) == 1 else "things"
        summary = f"{count} {thing} noticed inside the code, for the repo owners"
        out.append(fold(summary, "<ul>" + "".join(suggestion_line(r) for r in open_s) + "</ul>"))
    else:
        out.append('<div class="card"><p>Nothing noticed right now.</p></div>')
    if closed_s:
        count = in_words(len(closed_s)).capitalize()
        thing = "one" if len(closed_s) == 1 else "ones"
        out.append(fold(f"{count} acted-on {thing}",
                         "<ul>" + "".join(suggestion_line(r) for r in closed_s) + "</ul>"))
    out.append("</section>")

    # --- learnings: what this deployment taught harness-kit, a plain list ---
    open_l = [r for r in learnings if not is_closed(r)]
    closed_l = [r for r in learnings if is_closed(r)]
    out.append('<section id="learnings"><h2 class="label">Learnings for harness-kit</h2>')
    if open_l:
        count = in_words(len(open_l)).capitalize()
        thing = "thing" if len(open_l) == 1 else "things"
        out.append(fold(f"{count} {thing} this deployment taught, waiting for harness-kit",
                        "<ul>" + "".join(suggestion_line(r) for r in open_l) + "</ul>"))
    else:
        out.append('<div class="card"><p>Nothing learned yet.</p></div>')
    if closed_l:
        count = in_words(len(closed_l)).capitalize()
        thing = "one" if len(closed_l) == 1 else "ones"
        out.append(fold(f"{count} folded into harness-kit or dropped",
                        "<ul>" + "".join(suggestion_line(r) for r in closed_l) + "</ul>"))
    out.append("</section>")

    out += dialogs
    return "\n".join(out)


def main():
    page = PAGE.read_text()
    if START not in page or END not in page:
        sys.exit("markers missing in mission-control.html")
    head, rest = page.split(START, 1)
    _, tail = rest.split(END, 1)
    PAGE.write_text(head + START + "\n" + render(load()) + "\n" + END + tail)
    print("mission-control.html regenerated from board.csv")


if __name__ == "__main__":
    main()
