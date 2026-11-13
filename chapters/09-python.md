# Python and scripting

16 lessons. Most-repeated first.

- The Python tool blocks on subprocess and urllib calls, and a 120 s timeout wipes session state. Run long jobs and network checks as scripts via exec_command (for example, tools/verify_live.py), with per-request timeouts.
- The bundled Vector python has no Playwright; `browser_python` in `state/config.json` points at the system one.
- The bundled Vector python lacks Playwright; always use the system Python path above.
- The Python tool's 120 s limit counts `time.sleep`; poll long runs with sleeps <= 100 s and read logs with read_file.
- Kept insisting I post on Reddit/HN myself; those need his own login - built API script + one-click links instead *(correction from the human)*
- Detached `.bat` + log can sit empty forever on this box; `subprocess.run(..., timeout=)` from the python tool is faster and reports real errors. Long suites: `Popen` and poll the log.
- Keep each python tool call under ~90 s of polling; long sleeps killed the council subprocesses twice (^C in score.log).
- PowerShell `& $PY @array` mangled the pairwise arguments; a Python subprocess runner with a list argv fixed it.
- Python `urllib` gets 403 from juwenlie.pages.dev; send a browser User-Agent to verify the card.
- The Python tool session resets often; run long steps as scripts via exec_command and poll.
- A subprocess timeout kills `L new` halfway and leaves half-seeded state. Run long landing commands (new / shoot / publish) detached with Start-Process and logs, then poll. Run Python with `-u` or the log stays empty until exit.
- Words: a dictionary sweep of word pairs found everyday phrases ("not paid" -> Notepad) that 668 real transcripts and 25 hand-written sentences missed.
- Bench: a job that exits in seconds with "wrote ..." has not measured anything; make the script exit non-zero when it measured nothing.
- Pure-Python BPE on 104k chunk types takes about 45 minutes for a 4096 vocabulary.
- (mlbb-blame r6-7) Python helper default arguments bound to a stale line list hide edits; re-read the file each time.
- The Vector python tool sets `PYTHONNOUSERSITE=1`, and a `tolstack` folder in the cwd shadows the installed package. Run project commands from another cwd with that variable removed.
