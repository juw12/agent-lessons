"""Generic leak scan for a public lessons repo: run in CI on every push.

Fails on e-mail addresses, private IPv4 addresses, common token formats, personal Windows paths and
internal hostnames. Placeholders such as <internal-host> are allowed. Private, project-specific terms
belong in the build's redaction rules, which are kept outside the repo.
"""
import re
import sys
from pathlib import Path

PATTERNS = {
    "email address": r"[\w.+-]+@[\w-]+\.(?:com|net|org|io|dev|co|id|tw|cn)\b",
    "IPv4 address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "GitHub token": r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}",
    "API key": r"\bsk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "personal Windows path": r"[A-Za-z]:\\\\Users\\\\(?!<)[A-Za-z0-9_.-]+|C:/Users/[A-Za-z0-9_.-]+",
    "internal hostname": r"\b[\w-]+\.(?:intra|internal|corp|lan)\b",
}
SCANNED = ("*.md", "*.jsonl")


def main():
    root = Path(__file__).resolve().parent.parent
    problems = []
    for pattern in SCANNED:
        for path in root.rglob(pattern):
            if ".git" in path.parts:
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                for label, regex in PATTERNS.items():
                    if re.search(regex, line):
                        problems.append(f"{path.relative_to(root)}:{number}: {label}")
    for problem in problems:
        print(problem)
    if problems:
        sys.exit(f"{len(problems)} possible leaks")
    print("leak scan: clean")


if __name__ == "__main__":
    main()
