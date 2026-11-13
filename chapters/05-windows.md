# Windows, PowerShell and encodings

21 lessons. Most-repeated first.

- Never edit files with PowerShell 5 `Get-Content`/`Set-Content`: it reads UTF-8 as cp1252 and writes a BOM, so every non-ASCII character becomes mojibake (`≥` -> `â‰¥`). Edit from Python with `encoding="utf-8"` and keep LF; add a test that tracked text files have no BOM and no mojibake.
- PowerShell drops an empty `--query ""` argument, which shifts every later argument. Omit the flag instead of passing an empty string.
- Landing.py crashes when printing to a cp1252 console. Set PYTHONIOENCODING=utf-8 first.
- PowerShell `(Get-Content f -Raw).Replace(..) | Set-Content -Encoding utf8` reads UTF-8 as ANSI and writes back mojibake ("·" -> "Â·") plus a BOM. Edit source files with Python (read_text/write_text encoding='utf-8') only; if it happens, fix with text.encode('cp1252').decode('utf-8').
- Files stored with CRLF in the index but rewritten as LF give whole-file diffs; check `git ls-files --eol` and convert back to CRLF before committing.
- Read council score.json with encoding="utf-8" (default cp1252 crashes on Windows).
- Keyboard focus on an illustrated hit target: stacked drop-shadows on the SVG trace the silhouette and beat a box/ellipse outline. Keep a transparent solid outline so Windows high-contrast mode still paints a ring.
- `add_card.py` rewrote `apps.json` with LF while the repo file is CRLF (diff showed the whole file). Restore CRLF before committing so the diff is only the new card.
- Writing JSON with Python on Windows: open in binary or newline='\n' and keep the original indent, or the diff becomes the whole file.
- Start dev servers with PowerShell Start-Process, not a REPL-spawned Popen: REPL children's subprocesses die (0xC000013A) or hang.
- Buddy voice (vs Wispr Flow / Handy): 1) Hugging Face is blocked at the office; sherpa-onnx ships the same ASR models as GitHub release assets (k2-fsa/sherpa-onnx asr-models) - use those, with resumable Range downloads; bz2 unpack of 200 MB takes minutes under load, so do it in the background. 2) Benchmark before picking defaults: Parakeet V3 (Handy's pick) lost to Whisper base.en on our English corpus (13.6% vs 7.5% WER); Silero VAD removed all Whisper silence hallucinations (4/4 -> 0/4). 3) Score cleaned output against the intended meaning and normalise digits/number words, or a correct "at four" counts as an error. 4) Other agents saturating the CPU doubled latency (0.88 -> 2.1 s): compare engines inside one run, report both numbers. 5) Windows gotchas: PowerShell `*>` logs are UTF-16; a cp1252 console crashed a bench on a Chinese print (set PYTHONIOENCODING=utf-8); Python write_text turns LF into CRLF - write bytes. 6) Compress-Archive on a 440 MB PyInstaller folder takes far longer than the build itself under load and the zip size looks stuck meanwhile; check the file lock before assuming it died. 7) The skill's shared portfolio state clone can hold another session's unpushed commit - edit the catalog in a fresh clone instead.
- Card: the catalog `apps.json` is LF in the skill's clone; check the bytes before "restoring" CRLF. In a shared clone with someone else's untracked files, add your files by name instead of `git add -A`.
- PowerShell `*>` writes UTF-16 logs; Python write_text on Windows writes CRLF (pass newline="\n"); run anything over ~60 s as a detached script with a log file.
- Windows: tool output captured on Windows carries `\r\n`; normalise it before pasting into an LF file, and read line endings with `git ls-files --eol`.
- Windows: `CREATE_NO_WINDOW` combined with `DETACHED_PROCESS` shows a console on the desktop; use `CREATE_NO_WINDOW` alone for background jobs.
- Windows: before blaming a console window on your own jobs, check its ancestry; a parent `svchost.exe` means the Task Scheduler started it.
- Use cmd.exe and the file tools for logs; a cold torch import takes about 2 minutes. Never run a broad file listing or search.
- WebView2 folder save asks twice (Save changes, then Allow) and the default button is the cancel one: tell the user in the UI.
- (kilat r1) `Path.write_text` on Windows turns LF into CRLF; write bytes when a tracked file must keep its line endings.
- (mlbb-blame r6-7) A PowerShell `... | Set-Content file` pipeline keeps the file locked until the command ends.
- `Path(windows_path).name` does nothing useful on Linux; use `PureWindowsPath` for paths written on Windows. Wait for the Linux CI run before calling a release done (the first v0.3.0 run failed there).
