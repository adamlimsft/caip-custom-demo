#!/usr/bin/env python3
"""Local checks for a custom demo kit folder (stdlib only).

Usage: python check_kit.py <kit_dir> [--zip <zip_path>] [--max-path 100]

Checks: JSON validity, Python compiles, path length, no spaces, README starts with an H1,
markdown table width, and (with --zip) root-level layout + test unzip + file count.
Warns if a README or AI guide has a contact line or help offer (not wanted).
Exit code 0 when no FAIL. Never executes kit code.
"""
import argparse
import json
import os
import sys
import tempfile
import zipfile

# Phrases that READMEs must not contain (contact intro / help offer). Reported as warnings.
UNWANTED = ("feel free to email/message me", "i'm happy to help",
            "if you'd like a hand setting this up")


def rel_files(root):
    out = []
    for d, _, files in os.walk(root):
        for f in files:
            out.append(os.path.relpath(os.path.join(d, f), root).replace(os.sep, "/"))
    return sorted(out)


def check_readme(path):
    """Return (problems, warnings) for one README or AI guide."""
    lines = open(path, encoding="utf-8").read().splitlines()
    probs, warns = [], []
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or not lines[i].startswith("# "):
        return ["first line is not an H1"], warns
    for n, line in enumerate(lines):
        low = line.lower().replace("\u2019", "'")
        for phrase in UNWANTED:
            if phrase in low:
                warns.append(f"line {n+1}: contains \"{phrase}\" (no contact line or help offer)")
    # tables
    for n, line in enumerate(lines):
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) > 5:
                probs.append(f"line {n+1}: table has {len(cells)} columns (>5)")
            prev = lines[n - 1].strip() if n else ""
            if not prev.startswith("|") and prev:
                probs.append(f"line {n+1}: no blank line before table")
            if not prev.startswith("|") and any(c == "" for c in cells):
                probs.append(f"line {n+1}: empty header cell")
    return probs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kit")
    ap.add_argument("--zip")
    ap.add_argument("--max-path", type=int, default=100)
    a = ap.parse_args()
    fails, warns = [], []
    files = rel_files(a.kit)
    for f in files:
        full = os.path.join(a.kit, f)
        if " " in f:
            fails.append(f"space in path: {f}")
        if len(f) > a.max_path:
            fails.append(f"path {len(f)} chars: {f}")
        elif len(f) > 60:
            warns.append(f"path over 60 chars: {f}")
        if f.endswith(".json"):
            try:
                json.load(open(full, encoding="utf-8"))
            except Exception as e:
                fails.append(f"invalid JSON {f}: {e}")
        if f.endswith(".py"):
            try:
                compile(open(full, encoding="utf-8").read(), f, "exec")
            except SyntaxError as e:
                fails.append(f"Python does not compile {f}: {e}")
        if f.endswith(".ipynb"):
            try:
                nb = json.load(open(full, encoding="utf-8"))
                for k, c in enumerate(nb.get("cells", [])):
                    if c.get("cell_type") == "code":
                        src = "".join(c.get("source", []))
                        src = "\n".join(l for l in src.splitlines()
                                        if not l.lstrip().startswith(("%", "!")))
                        compile(src, f"{f}#cell{k}", "exec")
            except SyntaxError as e:
                fails.append(f"notebook cell does not compile {f}: {e}")
            except Exception as e:
                fails.append(f"invalid notebook {f}: {e}")
        name = os.path.basename(f).lower()
        if name == "readme.md" or (f.startswith("ai/") and f.endswith(".md")):
            probs, rwarns = check_readme(full)
            fails.extend(f"{f}: {p}" for p in probs)
            warns.extend(f"{f}: {w}" for w in rwarns)
    if "README.md" not in files:
        fails.append("no top-level README.md")
    if "Use_Case_Explanation.md" not in files:
        fails.append("no top-level Use_Case_Explanation.md")
    if a.zip:
        try:
            with zipfile.ZipFile(a.zip) as z:
                names = [n for n in z.namelist() if not n.endswith("/")]
                stem = os.path.splitext(os.path.basename(a.zip))[0]
                tops = {n.split("/")[0] for n in names}
                if len(tops) == 1 and tops.pop() == stem:
                    fails.append("zip has a top folder named like the zip")
                if "README.md" not in names:
                    fails.append("README.md not at zip root")
                if any(len(n) > a.max_path for n in names):
                    fails.append("zip path over limit")
                bad = z.testzip()
                if bad:
                    fails.append(f"corrupt member: {bad}")
                with tempfile.TemporaryDirectory() as t:
                    z.extractall(t)
                    if len(rel_files(t)) != len(files):
                        fails.append(f"zip has {len(rel_files(t))} files, kit has {len(files)}")
        except zipfile.BadZipFile as e:
            fails.append(f"bad zip: {e}")
    print(json.dumps({"files": len(files), "fail": fails, "warn": warns,
                      "passed": not fails}, indent=2))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
