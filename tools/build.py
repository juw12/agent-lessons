"""Build a public, de-duplicated lessons handbook from private lesson notes.

Inputs
  --md FILE[::SECTION_REGEX]   Markdown with "- " bullet lessons. With ::REGEX only the sections whose
                               heading matches are read (e.g. "README.md::^#+ (Lessons|Gotchas)").
  --corrections FILE.jsonl     Optional rows {"date", "goal", "correction"}: what a human corrected.
  --rules FILE.json            PRIVATE redaction rules (keep it outside the repo):
                               {"drop_if_contains": [regex...], "replace": [[regex, text]...],
                                "forbidden_after_redaction": [regex...]}
  --out DIR                    Where to write README chapters, lessons.md and lessons.jsonl.

Every lesson is redacted, dropped if it is about private systems, sorted into a chapter by keywords,
and merged with near-duplicates (the longer, more specific wording wins). The build fails if any
forbidden pattern survives, so nothing private is ever written.
"""
import argparse
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

CHAPTERS = [
    ("agents", "Working with AI agents", [
        "agent", "council", "judge", "model", "llm", "prompt", "opencode", "codex", "copilot", "claude",
        "gemini", "subagent", "session", "parallel", "context", "token", "skill", "mcp", "vector", "autopilot",
    ]),
    ("verify", "Verification, tests and gates", [
        "test", "gate", "verify", "verified", "check", "playwright", "screenshot", "assert", "ci", "audit",
        "reproduc", "regression", "live", "probe", "smoke",
    ]),
    ("git", "Git, GitHub and shipping", [
        "git", "push", "pull request", " pr ", "pr #", "commit", "rebase", "merge", "branch", "gh ", "gh api",
        "pages", "workflow", "actions", "release", "tag", "repo", "worktree",
    ]),
    ("network", "Networks, proxies and TLS", [
        "proxy", "407", "tls", "certificate", "no_proxy", "https_proxy", "timeout", "dns", "firewall", "vpn",
        "network",
    ]),
    ("windows", "Windows, PowerShell and encodings", [
        "powershell", "windows", "utf-8", "utf-16", "bom", "crlf", " lf", "cp1252", "mojibake", "shortcut",
        "taskbar", ".exe", "webview2", "registry", "scheduled task", "cmd /c",
    ]),
    ("ui", "UI, design and accessibility", [
        "css", "layout", "dark", "light", "theme", "font", "contrast", "a11y", "aria", "i18n", "emoji",
        "px", "button", "card", "color", "colour", "design", "typography", "icon", "hero", "mobile",
    ]),
    ("apps", "Apps, PWAs, mobile and 3D", [
        "pwa", "service worker", "android", "ios", "three.js", "webgl", "widget", "3d", "canvas", "game",
        "offline", "install", "apk", "adb",
    ]),
    ("data", "Data, numbers and honesty", [
        "data", "invent", "source", "number", "currency", "fact", "price", "fare", "timetable", "estimate",
        "total", "round", "sum", "csv", "dataset",
    ]),
    ("python", "Python and scripting", [
        "python", "subprocess", "pip", "venv", "urllib", "requests", "asyncio", "script",
    ]),
    ("product", "Product, launch and growth", [
        "landing", "portfolio", "seo", "stars", "users", "pricing", "founder", "launch", "readme", "brand",
        "marketing", "growth",
    ]),
    ("notes", "Notes, memory and second brain", [
        "obsidian", "vault", "note", "journal", "brain", "memory",
    ]),
]
GENERAL = ("general", "General engineering habits")

# Correction logs mix real lessons with status notes ("None so far", "R4 8.83 kept"); keep only the lessons.
CORRECTION_PREFIX = re.compile(r"^(?:none(?: so far| yet)?\s*[;:,-]?\s*)?(?:lesson|noted|test gotcha|js gotcha)\s*[:;-]\s*", re.I)
CORRECTION_NOISE = re.compile(r"^(?:none\b|no correction|no user input|r\d+\s|round \d+ )", re.I)

DATE_PREFIX = re.compile(r"^\s*(?:\*\*)?(20\d\d-\d\d-\d\d)(?:\*\*)?\s*(?:\(([^)]{1,60})\))?\s*[:\-–]?\s*")


def read_markdown(spec):
    path, _, section_regex = spec.partition("::")
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    wanted = re.compile(section_regex) if section_regex else None
    inside = wanted is None
    heading_date = ""
    entries = []
    current = None
    for line in lines:
        if line.startswith("#"):
            if wanted is not None:
                inside = bool(wanted.search(line))
            found = re.search(r"20\d\d-\d\d-\d\d", line)
            heading_date = found.group(0) if found else heading_date
            current = None
            continue
        if not inside:
            continue
        if re.match(r"^\s*- ", line):
            current = {"text": line.strip()[2:].strip(), "date": heading_date}
            entries.append(current)
        elif current is not None and line.strip() and line.startswith(("  ", "\t")):
            current["text"] += " " + line.strip()
        elif not line.strip():
            current = None
    return entries


def read_corrections(path):
    entries = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        correction = (row.get("correction") or "").strip()
        correction = CORRECTION_PREFIX.sub("", correction).strip()
        if len(correction) < 40 or CORRECTION_NOISE.match(correction):
            continue
        entries.append({"text": correction, "date": row.get("date", ""), "kind": "correction"})
    return entries


def clean(entry, rules):
    text = entry["text"]
    match = DATE_PREFIX.match(text)
    if match:
        entry["date"] = entry.get("date") or match.group(1)
        text = text[match.end():]
    for pattern in rules.get("drop_if_contains", []):
        if re.search(pattern, text):
            return None
    for pattern, replacement in rules.get("replace", []):
        text = re.sub(pattern, replacement, text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < 25:
        return None
    entry["text"] = text[0].upper() + text[1:]
    return entry


def chapter_of(text):
    lowered = " " + text.lower() + " "
    scores = {key: sum(lowered.count(word) for word in words) for key, _, words in CHAPTERS}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else GENERAL[0]


def normalise(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower())


STOPWORDS = set("""a an the and or but if then else of to in on at for with by from as is are was were be been it its
this that these those not no do does did can could should would will just only also than into out up down so very more
most when while after before every each all any one two use used using via per run runs""".split())


def content_words(text):
    return {word for word in re.findall(r"[a-z0-9_.-]{3,}", text.lower()) if word not in STOPWORDS}


def merge_duplicates(entries, threshold, word_threshold=0.5):
    kept = []
    for entry in sorted(entries, key=lambda item: -len(item["text"])):
        key = normalise(entry["text"])
        word_set = content_words(entry["text"])
        duplicate = False
        for other in kept:
            if other["chapter"] != entry["chapter"]:
                continue
            overlap = len(word_set & other["words"]) / max(1, len(word_set | other["words"]))
            if overlap >= word_threshold:
                other["seen"] += 1
                duplicate = True
                break
            matcher = difflib.SequenceMatcher(None, key, other["key"], autojunk=False)
            if matcher.real_quick_ratio() < threshold or matcher.quick_ratio() < threshold:
                continue
            if matcher.ratio() >= threshold:
                other["seen"] += 1
                duplicate = True
                break
        if not duplicate:
            entry["key"] = key
            entry["words"] = word_set
            entry["seen"] = 1
            kept.append(entry)
    for entry in kept:
        entry.pop("key")
        entry.pop("words")
    return kept


def leak_check(entries, rules):
    problems = []
    for entry in entries:
        for pattern in rules.get("forbidden_after_redaction", []):
            if re.search(pattern, entry["text"]):
                problems.append((pattern, entry["text"][:120]))
    return problems


def write_outputs(entries, out):
    titles = dict((key, title) for key, title, _ in CHAPTERS)
    titles[GENERAL[0]] = GENERAL[1]
    order = [key for key, _, _ in CHAPTERS] + [GENERAL[0]]
    chapter_dir = out / "chapters"
    chapter_dir.mkdir(parents=True, exist_ok=True)
    for old in chapter_dir.glob("*.md"):
        old.unlink()

    def line_for(entry):
        tag = " *(correction from the human)*" if entry.get("kind") == "correction" else ""
        return f"- {entry['text']}{tag}"

    all_lines = ["# All lessons (one file, for pasting into an agent's context)", ""]
    counts = Counter(entry["chapter"] for entry in entries)
    for number, key in enumerate([key for key in order if counts[key]], start=1):
        chapter_entries = sorted(
            (entry for entry in entries if entry["chapter"] == key),
            key=lambda item: (-item["seen"], item.get("date", "")),
        )
        name = f"{number:02d}-{key}.md"
        body = [f"# {titles[key]}", "", f"{len(chapter_entries)} lessons. Most-repeated first.", ""]
        body += [line_for(entry) for entry in chapter_entries]
        (chapter_dir / name).write_text("\n".join(body) + "\n", encoding="utf-8", newline="\n")
        all_lines += [f"## {titles[key]}", ""] + [line_for(entry) for entry in chapter_entries] + [""]
    (out / "lessons.md").write_text("\n".join(all_lines), encoding="utf-8", newline="\n")
    with (out / "lessons.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for entry in entries:
            row = {
                "chapter": titles[entry["chapter"]],
                "text": entry["text"],
                "date": entry.get("date", ""),
                "kind": entry.get("kind", "lesson"),
                "times_learned": entry["seen"],
            }
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    readme = out / "README.md"
    if readme.exists():
        table = ["| # | Chapter | Lessons |", "|---|---|---|"]
        for number, key in enumerate([key for key in order if counts[key]], start=1):
            table.append(f"| {number} | [{titles[key]}](chapters/{number:02d}-{key}.md) | {counts[key]} |")
        text = readme.read_text(encoding="utf-8")
        text = re.sub(
            r"<!-- chapters:start -->.*?<!-- chapters:end -->",
            "<!-- chapters:start -->\n" + "\n".join(table) + "\n<!-- chapters:end -->",
            text,
            flags=re.S,
        )
        text = re.sub(r"\*\*\d+ lessons\*\*", f"**{len(entries)} lessons**", text)
        readme.write_text(text, encoding="utf-8", newline="\n")
    return {titles[key]: counts[key] for key in order if counts[key]}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--md", action="append", default=[])
    parser.add_argument("--corrections", action="append", default=[])
    parser.add_argument("--rules", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--threshold", type=float, default=0.72)
    args = parser.parse_args()

    rules = json.loads(Path(args.rules).read_text(encoding="utf-8"))
    raw = []
    for spec in args.md:
        raw += read_markdown(spec)
    for path in args.corrections:
        raw += read_corrections(path)

    cleaned = [entry for entry in (clean(dict(item), rules) for item in raw) if entry]
    for entry in cleaned:
        entry["chapter"] = chapter_of(entry["text"])
    merged = merge_duplicates(cleaned, args.threshold)

    problems = leak_check(merged, rules)
    if problems:
        for pattern, text in problems[:20]:
            print(f"LEAK {pattern!r}: {text}", file=sys.stderr)
        sys.exit(f"refusing to write: {len(problems)} entries still match forbidden patterns")

    counts = write_outputs(merged, Path(args.out))
    summary = {
        "read": len(raw),
        "dropped_private_or_short": len(raw) - len(cleaned),
        "merged_duplicates": len(cleaned) - len(merged),
        "published": len(merged),
        "chapters": counts,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
