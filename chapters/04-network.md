# Networks, proxies and TLS

27 lessons. Most-repeated first.

- Playwright on the corporate PC: clear HTTP(S)_PROXY and set NO_PROXY=localhost before `connect_over_cdp`; in the sync API wait with `page.wait_for_timeout()`, not `time.sleep()` (frames don't update while sleeping).
- Urllib proxy fallback: build a NEW Request per opener (ProxyHandler.set_proxy mutates the request), and only treat a 4xx as a refusal when the body is your server's JSON error; office proxies answer loopback with their own 400 page. Playwright behind <corporate-proxy>: launch with --proxy-bypass-list=<internal-ip>;localhost;<local> via args, not the proxy= option.
- When the corporate proxy (<corporate-proxy>) returns 407 for git, the local proxy works: `git -c http.https://github.com/.proxy=http://localhost:3128 push`, and `HTTPS_PROXY=http://localhost:3128` for gh. Playwright checks against a local server can starve on networkidle while the proxy is flaky; clear HTTP(S)_PROXY and set NO_PROXY=* for the test process.
- `~/.gitconfig` sets `http.https://github.com/.proxy=http://<corporate-proxy>`, which beats `http.proxy` and `HTTPS_PROXY`. To alternate routes, pass both `-c http.https://github.com/.proxy=<p>` and `-c http.proxy=<p>` (localhost:3128 or <corporate-proxy>).
- Verify map tiles and web fonts load in every judged screenshot (proxy 3128 was down); use system proxy <corporate-proxy> with a retrying uploader for GitHub API writes; resample bots before trusting a small score delta *(correction from the human)*
- (founder-studio v2) cmd `set VAR=* && ...` keeps the trailing space in the value; use PowerShell `$env:NO_PROXY='*'` or proxied loopback calls fail.
- Proxy port was 3128 not 3129; script updated accordingly *(correction from the human)*
- (cairn vibe r7) When the office proxy flips (407 / local proxy down / direct reset), commit locally, write the vault note as "push pending", and retry in a few minutes rather than stopping; gh works through HTTPS_PROXY=<corporate-proxy> like git's url-specific proxy.
- (riak 1.4.0) The network proxy can change mid-session (407 from the old one, refused from the new one, then back); rotate proxies on 407/refused/timeout instead of hard-coding one.
- When HTTP(S)_PROXY points at a local proxy that is down, localhost calls from Python children are refused (test_api stub "10061"). Run tests with NO_PROXY=*.
- The corporate proxy can 407 for a few minutes; retry the push in a loop (20 s apart) before falling back to the REST API.
- Git proxy flips between localhost:3128 and <corporate-proxy>; on 407 retry with the other one.
- Proxy: the landing skill's `state/config.json` has its own `proxy` key that overrides `HTTPS_PROXY`. When a tool reads its proxy from a config file that is not yours: back the file up, override the key for one command, wait for the process to exit, restore the bytes and compare them with the backup.
- Landing.py forces config.proxy (<corporate-proxy> -> 407 here); run it via a wrapper that temporarily sets proxy to localhost:3128 and restores config in finally.
- Proxy: gh needs the normal proxy env, but local Playwright needs HTTP(S)_PROXY="" and NO_PROXY=*. Set them per command, not globally.
- When the local proxy dies mid-run, finish all offline work (tests, notes, logs) and queue pushes; do not restart another app's proxy.
- A status-file wait loop must break on the key the script really writes (`finished`), or it waits out the full timeout.
- Python http.server readiness checks must bypass HTTP_PROXY (ProxyHandler({})), or they hang on a corporate proxy.
- Network: when the local proxy (localhost:3128) is down, git still uses it via the URL-specific key `http.https://github.com/.proxy` in ~/.gitconfig; `-c http.proxy=` alone does not override it. Override that exact key per command or via GIT_CONFIG_COUNT env (here to the corporate <corporate-proxy>) without editing the user's config.
- (cpu-eco-toggle 2026-11-12) When <corporate-proxy> answers 407, use the local proxy http://localhost:3128 for git (http.proxy plus the github.com-specific key) and for urllib/API calls; set landing state/config.json "proxy" only for the run and restore it after.
- (mlbb-blame r6-7) `landing.py` takes its proxy from `state/config.json` before `HTTPS_PROXY`, so the env var does not help; a wrapper that patches `load_config` in memory published through localhost:3128 without editing the skill.
- (mlbb-blame r6-7) When git gets 407 from <corporate-proxy>, check that localhost:3128 is listening and pass `-c http.https://github.com/.proxy=http://localhost:3128`; that worked without changing any global config.
- (mlbb-blame r4-r5) e2e tests that load a CDN script (Tesseract.js) need the office proxy: read it from `HONE_PROXY` (default <corporate-proxy>) and pass it to the browser launch, with loopback bypassed.
- (cpu-eco-toggle) `check --fonts` "font fetch timed out" was the network, not the page: rerun with HTTPS_PROXY/HTTP_PROXY set to the working proxy and D6 passed.
- (inti r4) Size a long job's timeout from its measured rate on the day, and give long batch tools a resume, before starting them.
- (kilat r1) With the screen locked the PC runs 30 to 80 times slower; do not read a timeout under load as a bug.
- He said: no need me, u can do it before - on git 407 retry with -c http.https://github.com/.proxy=localhost:3128 (per-URL proxy overrides http.proxy) instead of handing the push back *(correction from the human)*
