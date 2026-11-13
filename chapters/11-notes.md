# Notes, memory and second brain

5 lessons. Most-repeated first.

- Cairn precedent/autopilot: (1) run every new CLI action once against real data before merging; `precedent init` crashed on a missing module-level import that no unit test touched. (2) Write a default template only after the imports ran: an earlier crashed run left a blank profile that blocked the real one (fixed: an untouched template is now replaced). (3) "Keep both" conflict merges can split a CSS block; re-check brace balance after resolving styles.css. (4) Bump the service-worker cache name past whatever main already uses, not past your own branch. (5) The vault root IS the brain here, so brain notes land at `<vault>/notes/`, not `<vault>/brain/notes/`.
- Measure scale with a generated vault, but discard the first read: freshly written files on this PC take ~30 ms each (antivirus). 66 s cold vs 2.5 s warm for 2,060 notes; only the warm number is the app's.
- Kernel: revocation that unmaps another task's memory breaks "a blocked task's buffer stays mapped"; keep deferred-access buffers out of revocable memory. A rights flag cached in a blocked task goes stale when its capability is revoked; recompute or clear it at revocation.
- Run: when the last open gate needs an idle machine, start the watcher first and do the judge calls, the PR body and the notes while it waits; write every note for the 'not measured' outcome and amend only if the measurement lands.
- Wide editable tables: put note rows in a sticky, width-bound block (ResizeObserver), or the text is cut off inside the scroll box.
