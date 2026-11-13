# agent-lessons

**Hard-won lessons from building and shipping 60+ projects with AI coding agents** (OpenCode, Claude Code, Codex, Copilot,
Gemini, Vector) on a locked-down Windows work laptop, as one person who is an engineer, not a programmer.

Every line here cost at least one failed run. They were written down the moment something broke, by the
agent that broke it, and are published so your agents don't have to learn them again.

- **[`lessons.md`](lessons.md)**: every lesson in one file, ready to paste into an agent's context.
- **[`chapters/`](chapters/)**: the same lessons sorted by topic.
- **[`lessons.jsonl`](lessons.jsonl)**: machine-readable (`chapter`, `text`, `date`, `kind`).
- **[`tools/build.py`](tools/build.py)**: turn *your own* lesson notes into the same format, with private terms stripped.

## The 15 that matter most

Distilled from the patterns that kept coming back across all chapters.

1. **Verify the live thing, not the commit.** Open the deployed URL with a cache-buster (`?cb=<time>`),
   re-probe it after every deploy, and diff it against what you meant to ship. "Pushed" is not "done".
2. **Prove a bug with a real reproduction before and after the fix.** Simulated tests found none of the
   race/crash bugs that a real kill, a real mount or a real protected branch did.
3. **Turn every error a reviewer finds into a code gate.** AI judges cannot give a stable 10/10; the real
   gains came from making each judge-found mistake impossible to repeat.
4. **AI judges are noisy (±0.2 to 0.6 between identical runs).** Re-score the current best in the same
   session, trust blind pairwise votes over small score deltas, pool 2-3 samples, and stop after two rounds
   without gain. On a plateau, change the lever, not the polish.
5. **Check every capture before judging it.** Rounds were lost to bad evidence (a page that had not
   loaded, an error toast, an unstyled sheet), not bad work.
6. **Never invent data to fill a gap.** If the source lacks a number, queue the gap and say so.
   Round each line before summing so shown totals add up; check the currency per row.
7. **Parallel agents need their own checkout.** One worktree or clone per task, fetch and rebase before
   every push, claim queue items before starting, kill only your own processes, and re-run gates right
   before publishing (another session may have moved files under you).
8. **On Windows, never edit text with PowerShell 5 `Get-Content`/`Set-Content`.** It reads UTF-8 as cp1252,
   writes a BOM and turns every non-ASCII character into mojibake. Edit from Python with `encoding="utf-8"`
   and LF. PowerShell `>` writes UTF-16.
9. **Behind a corporate proxy, a per-URL setting beats the global one.** `http.https://github.com/.proxy`
   overrides `http.proxy` and `HTTPS_PROXY`; on HTTP 407, retry the other route before giving up, and fall
   back to the GitHub REST/Git Data API when git itself is blocked.
10. **Tool calls die; files survive.** Shell calls time out and interpreters restart. Keep helpers in
    files, launch long jobs detached, write results to disk and poll.
11. **Resolve tools to absolute paths** in scheduled tasks and after an agent restart: the child process
    often gets a reduced `PATH` and fails silently.
12. **Test layouts at 320, 390, 768, 1024 and 1440 px**, and assert `scrollWidth == viewport width` on
    every view. One wide table breaks the phone layout.
13. **"Make it like X" means X's interaction model.** Check what the reference actually does before
    building (a 3D walkable space is not a 2D floor plan in the same colours).
14. **The app is the source of truth.** Order of work: app, then brand, then landing page. Fix, don't
    redesign; keep a numbers-diff gate so a restyle can't silently change results.
15. **When the human says "finish it", finish it.** Work around hand-off tasks instead of asking, but
    treat real access walls (org policy, other people's accounts, codes only the human can type) as
    evidence, not obstacles to route around.

## Chapters

<!-- chapters:start -->
| # | Chapter | Lessons |
|---|---|---|
| 1 | [Working with AI agents](chapters/01-agents.md) | 120 |
| 2 | [Verification, tests and gates](chapters/02-verify.md) | 201 |
| 3 | [Git, GitHub and shipping](chapters/03-git.md) | 123 |
| 4 | [Networks, proxies and TLS](chapters/04-network.md) | 27 |
| 5 | [Windows, PowerShell and encodings](chapters/05-windows.md) | 21 |
| 6 | [UI, design and accessibility](chapters/06-ui.md) | 55 |
| 7 | [Apps, PWAs, mobile and 3D](chapters/07-apps.md) | 16 |
| 8 | [Data, numbers and honesty](chapters/08-data.md) | 30 |
| 9 | [Python and scripting](chapters/09-python.md) | 16 |
| 10 | [Product, launch and growth](chapters/10-product.md) | 15 |
| 11 | [Notes, memory and second brain](chapters/11-notes.md) | 5 |
| 12 | [General engineering habits](chapters/12-general.md) | 46 |
<!-- chapters:end -->

## Use it with your agent

**Whole handbook** (large context models): add one line to your `AGENTS.md`, `CLAUDE.md` or
`.github/copilot-instructions.md`:

```text
Before starting, read https://raw.githubusercontent.com/juw12/agent-lessons/main/lessons.md and follow it.
```

**Just what you need** (small context): paste the "15 that matter most" above plus the one or two chapters
for your stack (e.g. `chapters/03-git.md` and `chapters/05-windows.md` for a Windows repo).

**Make your agent keep its own.** The habit that produced this repo is simple: tell your agent
*"after anything breaks, append one line to `lessons.md`: what happened, why, and the fix; read it before
every run"*. After a month you have your own version of this file.

## Build your own from your notes

```bash
python tools/build.py \
  --md path/to/your/lessons.md \
  --md "path/to/README.md::^#+ (Lessons|Gotchas)" \
  --corrections path/to/corrections.jsonl \
  --rules path/OUTSIDE/the/repo/redact.json \
  --out .
```

`redact.json` lists what must never be published (`drop_if_contains`), what to rewrite (`replace`, e.g.
internal hostnames to `<internal-host>`), and patterns that must not survive (`forbidden_after_redaction`).
The build **refuses to write anything** if a forbidden pattern is still present. Keep that file out of the
repo so the list of secrets is not itself published. `tools/check.py` runs a generic leak scan (emails,
IPs, tokens, user paths) and runs in CI on every push.

## Notes

- Lessons are written as they were learned: terse, specific, sometimes about one app. The specifics are
  the point: they tell you exactly what failed and what fixed it.
- Company-internal systems, hosts, people and anything work-related were removed before publishing;
  `<corporate-proxy>`, `<internal-host>` and `<internal-ip>` mark where a value was redacted.
- Rough edges: some lessons mention the author's own tools (Cairn, hone, Vector). The fix inside the
  lesson still applies to your setup.

Text: [CC BY 4.0](LICENSE). Code in `tools/`: MIT. By [Juwen Lie](https://juwenlie.pages.dev).
