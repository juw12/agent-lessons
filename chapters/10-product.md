# Product, launch and growth

15 lessons. Most-repeated first.

- Order for an app: **app -> brand -> landing**. The app is the source of truth; fix, don't redesign.
- Landing `ingest` refuses pages that were already rebuilt; for a content refresh edit `landing/state/data.json` (back it up first) plus `state/content/<slug>.json`, then build and check.
- After a UI hone, refresh card art (portfolio), landing shot.jpg/g1.jpg and README screenshots in the same run; old images silently show the old UI.
- Bump the app's K.VERSION together with version.json, or users see a false "update ready" toast.
- (cairn vibe r6) A shell call that times out kills the Start-Process children it launched, so long judge/test jobs must be launched without -Wait and polled from short calls; never sleep in the shell.
- The shared portfolio/state clones get `reset --hard` by other jobs running in parallel. Copy the scripts to the chat working folder and render the card there (portfolio_card.py --portfolio-dir <tmp> --url http://<internal-ip>:<port>/ from a local http.server; the browser cannot reach github.io without the proxy).
- Landing: the builder takes the hero pill, a stat and a FAQ answer from `platforms`; set it to where the project really runs. The FAQ keeps only the first sentence of each README answer and at most 8 items, and it quotes the status word ("it's marked ..."); pick one that reads correctly there.
- Landing: the tools call `gh` by bare name; `landing.py new` fails at ingest when `gh` is not on PATH, after the seed page, shot and gallery card already exist. Put the `gh` and `git` folders on PATH and re-run only `ingest.py`.
- Use `CREATE_NO_WINDOW`, not `DETACHED_PROCESS`, for child console programs. The PID a launcher prints can be a shim: kill with `taskkill /T`, and use a fresh log name each time.
- After publishing, copy `p/landing.json` to the profile's `.github/landing.json` (it was 10 entries stale), or Building entries miss their Landing page link.
- Landing: the headline is read back from the site page's `<h1>` by `ingest.py`; edit that `<h1>` (and its `hl` span) and re-run ingest.
- Landing: `landing build` writes to `landing/out/p/<slug>/`, not to the site clone; only `publish` copies it over.
- Docs: a README claim about what an older version lost must name the engine that version used.
- (kilat r1) After a version bump, the profile line, the portfolio card text and the landing page all carry old numbers; check all three, not only the repo.
- (mlbb-blame r4-r5) Landing feature bodies are HTML-escaped plain text. Keep LaTeX and markup out of them and state formulas in words.
