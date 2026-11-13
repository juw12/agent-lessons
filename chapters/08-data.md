# Data, numbers and honesty

30 lessons. Most-repeated first.

- When a judge finds a factual error, turn it into a code gate first (e.g. 'departure points match the timetable'); a candidate that fixes facts beats one that scores higher but fails the gate.
- Budgets/tables: round each line before summing so shown lines add up to the shown total; add a gate that sums the displayed numbers.
- He answered: product, you pick customer/price/verdict, don't duplicate (remove dup copy, keep distinct from GlowNews/AI Daily) *(correction from the human)*
- Judges asked for return-ferry times and Sindo all-in fare; data lacks them, queued instead of inventing *(correction from the human)*
- Check currency per price row before converting (SGD rows were divided by FX rate) *(correction from the human)*
- Prefer automation that keeps facts current over more page polish *(correction from the human)*
- Absolute council scores drift by about 0.3 between runs. When a fix round loses on score but wins the pair vote (v4: 8.0 vs 8.3, pair 2-0-1), report both honestly; shipping the bug-fixed version is fine, the best *score* stays the older round.
- Judge on real-scale data: build the stand-in from the user's real session metadata (times, statuses, counts) and fake only titles/folders. Demo data hid every scale bug (408h in 14 days, all Done +0/-0).
- Polish-only rounds (borders, radii, fonts) score higher but tie the swapped pairwise. Rounds that add visible structure win it (r3: countdown label, Recently settled panel).
- Keep a numbers-diff gate (G5) for UI passes on engineering apps: compare all numbers in the verdict/KPI areas before vs after so a restyle cannot silently change results.
- Sample real API data before finalizing a parser: 2 of 5 real opening_hours strings used non-standard forms the first parser missed.
- Keep the source rebuild byte-identical to the gated build before shipping (diff the build, not the source).
- (riak 1.4.0) The council held at 8.25 for three rounds while each pair was non-regressing; visible polish (gauges, hints, captions) wins pair orderings but does not move the absolute score, which tracks the hero art. Stop at plateau and report the number honestly instead of chasing a 10.
- Founder-studio r11: scene richness (props, curb, fountain, neighbour stalls) broke the 8.7 plateau to 8.95 where four rounds of small UI fixes could not. When polish plateaus, pull the big visual lever.
- (mint 3.5.4) A translated UI chip that sends `dataset.example` (English) instead of its visible text quietly gives non-English users English results. Send what the user sees.
- When bot fixlists are mostly ASK items (solo mode, auto-confirm, payment verification), UI rounds stall. Queue them early and stop rather than burning rounds.
- Council noise floor here was about +/-0.3 around 7.0-7.3; after 3 rounds within noise, stop and ship instead of chasing contradictory asks.
- Do not Start-Process long rounds from the shell tool (it can kill them); run round scripts in the foreground with exec_command and poll.
- Round scripts must resolve relative app paths to absolute before chdir; a relative ..\app silently captured the wrong folder.
- Loop: commit the best version BEFORE starting an improvement round, not after. A build script that also refreshes the published demo image destroys the last copy of the previous version; keep the best version's image under another name. Here v0 was lost that way, so a round logged "not kept" became the published version.
- Bench: before waiting for a calm PC, measure per-process CPU time and ancestry: if none of the load is yours there is nothing to stop, and a watcher that samples the load gives "never calm" its numbers.
- Tooling: a start-and-poll helper with a very short wait can return a non-zero exit at once; read the log before assuming the process is still running.
- Real bugs found by art passes (koi fins folding under the body) are worth flagging even when the round is not kept.
- Run: under heavy load `gh` takes 1.5 to 2.5 minutes to start and is not on the PATH of a detached plan; the landing `repo_facts.py` then falls back to unauthenticated PowerShell REST and can overwrite good facts with empty ones. Refresh through the tool's own `facts_for` with an authenticated REST transport and compare with the stored values before merging.
- (inti r3, 2026-11-12) Before choosing a round, read the per-criterion medians of the baseline. With whole-number medians, MIN_GAIN 0.3 is one full point in the heaviest criterion, and a criterion already at 9 cannot pay: round 3 added evidence (already 9) and gained 0.0875.
- (inti r4) Check that a "before" evidence file is really from this round; equal totals hid a stale file from the round before.
- (mlbb-blame r6-7) Read `score.json` from disk before writing a score anywhere; a remembered number was wrong (9.85 vs 9.0).
- (kilat r1) Landing `data.json` is `indent=1`, CRLF, no final newline; round-trip it in that format so the diff stays small.
- (inti r6) More evidence moved the evidence criterion, not robustness or least privilege: six rounds landed between 8.1125 and 8.2625 against a bar of 8.4125. When every judge names the same missing thing for the top anchors (real hardware, a proof, an independent audit), another round of the same kind will not clear the minimum gain; say so before starting it.
- Landing: `ingest` refuses once a page has been rebuilt; edit the stored `data.json` entry instead. The builder shows only the first sentence (200 characters or fewer) of the first 5 limits and the FAQ uses the first 2 at 170 characters, so write each limit as one sentence.
