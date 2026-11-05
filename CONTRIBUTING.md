# Contributing

Thanks for helping improve this skill. Remember its scope: **public health writing**, based on the ECDC inclusive writing guidance. Changes should stay within that scope.

## Raise an issue

Open an issue to report a false positive, a missed term, a wrong suggestion, a bug in `scripts/check_inclusive.py`, or to suggest a new rule. Helpful details: the exact wording, the surrounding sentence, what you expected, and the source (ECDC guide section or another reputable public-health style guide) supporting the change.

## Fork and propose a change

1. Fork the repository and clone your fork.
2. Create a branch: `git checkout -b my-change`.
3. Make your change (see below) and test it.
4. Commit with a clear message and push the branch to your fork.
5. Open a pull request describing what changed and why, linking the supporting source.

## What to edit

- **Rules:** `scripts/rules.json`. Each rule has `id`, `pattern` (regex, case-insensitive), `suggest`, `why`, `sec` (guide section) and optionally `context: true` (needs human judgement) or `replace` (safe automatic fix; use only for terms that can be swapped without changing grammar or meaning).
- **Workflow and guidance:** `SKILL.md`.
- **Overview:** `README.md`.

## Testing

Run the scanner on a small sample containing your new term and a few near-misses, and check for false positives:

```bash
python3 scripts/check_inclusive.py sample.md
python3 scripts/check_inclusive.py sample.md --fix     # only if you added a `replace`
python3 -c "import json,re; [re.compile(r['pattern']) for r in json.load(open('scripts/rules.json'))]"   # regexes compile
```

## Guidelines

- Prefer specific suggestions over blanket bans; mark ambiguous terms `context: true`.
- Cite a source for new rules; don't copy long passages of the ECDC guide, link to it instead.
- Keep the scanner dependency-free (Python standard library only).
- Be respectful and constructive in discussions.
