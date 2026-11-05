#!/usr/bin/env python3
"""Check (and optionally fix) non-inclusive language, based on the ECDC
'Inclusive writing' editorial guidance (Nov 2026).

Usage:
  check_inclusive.py PATH [PATH ...]          report findings (dirs are walked)
  check_inclusive.py - < text                 read stdin
  check_inclusive.py PATH --json              machine-readable output
  check_inclusive.py PATH --fix               dry run: show safe auto-fixes as a diff
  check_inclusive.py PATH --fix --write       apply safe auto-fixes in place
  options: --strict (also show context-dependent rules that are hidden with --no-context)
           --no-context  hide rules that need human judgement
           --skip-code   ignore fenced code blocks and inline code (default on for .md/.qmd/.Rmd)

Supports .txt .md .qmd .Rmd .tex .rst .html .csv-free prose and .docx (read-only: report only).
Exit code 1 if findings exist, 0 otherwise.
"""
import argparse, difflib, json, os, re, sys, zipfile
from pathlib import Path

RULES = json.loads((Path(__file__).parent / "rules.json").read_text(encoding="utf-8"))
for r in RULES:
    r["_re"] = re.compile(r["pattern"], re.I)
TEXT_EXT = {".txt", ".md", ".markdown", ".qmd", ".rmd", ".tex", ".rst", ".html", ".htm", ".org"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "renv"}


def read_docx(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<[^>]+>", "", xml)
    import html
    return html.unescape(xml)


def code_mask(text):
    """Return text with code (fenced / inline) blanked to spaces, same length."""
    def blank(m): return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"^(```|~~~).*?^\1", blank, text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]+`", blank, text)


def iter_files(paths):
    for p in paths:
        if p == "-":
            yield "-"; continue
        pp = Path(p)
        if pp.is_dir():
            for root, dirs, files in os.walk(pp):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for f in sorted(files):
                    if Path(f).suffix.lower() in TEXT_EXT | {".docx"}:
                        yield str(Path(root) / f)
        else:
            yield str(pp)


def load(path):
    if path == "-":
        return sys.stdin.read()
    if path.lower().endswith(".docx"):
        return read_docx(path)
    return Path(path).read_text(encoding="utf-8", errors="replace")


def scan(text, skip_code, include_context):
    scan_text = code_mask(text) if skip_code else text
    out = []
    for r in RULES:
        if r.get("context") and not include_context:
            continue
        for m in r["_re"].finditer(scan_text):
            line = scan_text.count("\n", 0, m.start()) + 1
            col = m.start() - (scan_text.rfind("\n", 0, m.start()) + 1) + 1
            src = text.splitlines()[line - 1] if text else ""
            out.append(dict(rule=r["id"], line=line, col=col, match=m.group(0), suggest=r["suggest"],
                            why=r["why"], section=r["sec"], needs_judgement=bool(r.get("context")),
                            auto_fixable=("replace" in r), text=src.strip()))
    out.sort(key=lambda f: (f["line"], f["col"], -len(f["match"])))
    keep = []
    for f in out:
        if any(k["line"] == f["line"] and k["col"] <= f["col"] and f["col"] + len(f["match"]) <= k["col"] + len(k["match"]) for k in keep):
            continue
        keep.append(f)
    return keep


def match_case(src, rep, before=""):
    """Capitalise the replacement only if the original was capitalised as a normal
    word, or if an all-caps acronym sits at the start of a sentence."""
    acronym = src.isupper() and len(src) > 1
    if acronym:
        at_start = re.search(r"(^|[.!?:]\s+|\n\s*)$", before) is not None
        return rep[0].upper() + rep[1:] if at_start else rep
    return rep[0].upper() + rep[1:] if src[:1].isupper() else rep


def apply_fixes(text, skip_code):
    mask = code_mask(text) if skip_code else text
    edits = []
    for r in RULES:
        if "replace" not in r:
            continue
        for m in r["_re"].finditer(mask):
            s = m.group(0)
            rep = r["replace"]
            if "replace_singular" in r and not s.lower().endswith("s"):
                rep = r["replace_singular"]
            edits.append((m.start(), m.end(), match_case(s, rep, mask[max(0, m.start() - 4):m.start()])))
    for a, b, rep in sorted(edits, reverse=True):
        text = text[:a] + rep + text[b:]
    return text, len(edits)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--no-context", action="store_true", help="hide terms that depend on context")
    ap.add_argument("--skip-code", action="store_true")
    a = ap.parse_args()

    results, total = {}, 0
    for path in iter_files(a.paths):
        try:
            text = load(path)
        except Exception as e:
            print(f"! cannot read {path}: {e}", file=sys.stderr); continue
        skip = a.skip_code or path.lower().endswith((".md", ".qmd", ".rmd", ".markdown"))
        if a.fix:
            new, n = apply_fixes(text, skip)
            if not n:
                continue
            if path.lower().endswith(".docx") or path == "-":
                print(f"# {path}: {n} fixable term(s); docx/stdin is report-only", file=sys.stderr); continue
            total += n
            if a.write:
                Path(path).write_text(new, encoding="utf-8"); print(f"fixed {n} term(s) in {path}")
            else:
                sys.stdout.writelines(difflib.unified_diff(text.splitlines(True), new.splitlines(True), path, path + " (fixed)"))
            continue
        f = scan(text, skip, not a.no_context)
        if f:
            results[path] = f; total += len(f)

    if a.fix:
        print(f"\n{total} safe fix(es) {'applied' if a.write else 'proposed (use --write to apply)'}", file=sys.stderr)
        return 0
    if a.json:
        print(json.dumps(results, indent=1, ensure_ascii=False))
    else:
        for path, fs in results.items():
            print(f"\n{path}")
            for x in fs:
                tag = "?" if x["needs_judgement"] else "!"
                print(f"  {tag} L{x['line']}:{x['col']}  '{x['match']}' -> {x['suggest']}  [§{x['section']}]")
        print(f"\n{total} finding(s) in {len(results)} file(s).  '!' = clear match, '?' = depends on context.", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
