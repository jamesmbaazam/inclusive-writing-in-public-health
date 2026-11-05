# inclusive-writing-in-public-health

Version 0.1.2

A [Claude Code](https://claude.com/claude-code) skill that checks, and helps fix, stigmatising or dehumanising language in public health writing. It combines the [ECDC inclusive writing guidelines](https://www.ecdc.europa.eu/en/publications-data/inclusive-writing-ecdc) (public health specific rules) with the [alex](https://github.com/get-alex/alex) tool (general gendered, ableist, racial and condescending wording), so you get both kinds of check in one pass.

> **Public health only.** The guidance behind this skill was written for public health and infectious disease communication. It may not apply, or may be unhelpful, in other fields or contexts (for example where a term has a fixed technical meaning, or where a community prefers identity-first language). Use judgement, and don't apply it mechanically outside public health.

## Why use it

Words that feel neutral can 'other', stigmatise or exclude people. In public health that can do real harm: stigma lowers uptake of testing, vaccination and care, and it can make outbreaks harder to control. Most stigmatising wording is accidental and easy to miss in your own writing ("vulnerable groups", "high-risk populations", "cases" used for people, "unprotected sex", "vaccine hesitancy", "target populations"). Clearer, more specific wording is usually also better science writing: it says who is affected, by what, and why.

This skill gives you a quick, consistent first pass over a manuscript, report, protocol or slide text, so that you spend your editing time on the judgement calls.

## How it works (plain language)

1. **Point Claude at your text.** A file, a folder or pasted text (`.md`, `.qmd`, `.Rmd`, `.tex`, `.txt`, `.html`, `.docx`).
2. **A scanner looks for flagged wording.** It uses about 50 rules taken from the ECDC guide and prints each hit with a suggested alternative, the reason, and the guide section. Clear matches are marked `!`; wording that is only sometimes a problem is marked `?`.
3. **Optional second check with [alex](https://github.com/get-alex/alex).** Claude first asks whether it may check for alex (Node/`npx`) and, if it is missing, offers to help install it. It only installs with your agreement. With alex available, Claude also runs `npx alex`, a general-purpose tool for gendered, ableist, racial, condescending and profane wording. Alex doesn't know public-health conventions, so it complements the ECDC rules rather than replacing them. If you decline or Node isn't available, this step is skipped.
4. **Claude reads the findings in context.** It drops false positives (quotes, citations, formal case definitions, established terms) and also looks for things a word list can't catch, such as list order implying hierarchy, or a group described without saying why.
5. **Fixes.** A small set of safe terms can be replaced automatically (shown as a diff first). Everything else is rewritten by hand, keeping your meaning, numbers and citations. If a fix needs facts only you have (which countries, which groups, why risk is higher), Claude leaves a placeholder or asks, and doesn't invent them.
6. **Report.** You get a short summary of what changed, what was left for you to decide, and why.

If you only ask for a check, Claude reports and suggests but doesn't edit.

## Install and use

Install by cloning this repository into your Claude Code skills folder (requires [git](https://git-scm.com/) and Claude Code; Python 3 is needed for the scanner):

```bash
git clone https://github.com/jamesmbaazam/inclusive-writing-in-public-health.git \
  ~/.claude/skills/inclusive-writing-in-public-health
```

To update later, run `git pull` inside that folder. To pin a release, run `git checkout v0.1.2`.

The skill's instructions call the scanner at `~/.claude/skills/inclusive-writing-in-public-health/scripts/`, so keep the folder name and location as above. (To use it in a single project instead, clone into `<project>/.claude/skills/` and update that path in `SKILL.md`.)

Then start Claude Code (a new session if one was already open) and ask, for example: *"Check manuscript.md for inclusive language"*, or run `/inclusive-writing-in-public-health`.

You can also run the scanner directly from the cloned folder (Python 3, no dependencies):

```bash
python3 scripts/check_inclusive.py manuscript.md          # report
python3 scripts/check_inclusive.py manuscript.md --fix    # preview safe fixes as a diff
python3 scripts/check_inclusive.py manuscript.md --fix --write
```

## Source of the knowledge base

The rules and recommendations are drawn from the ECDC editorial guidance on inclusive writing. The guide itself is not included here; please read it at the source: <https://www.ecdc.europa.eu/en/publications-data/inclusive-writing-ecdc>

> European Centre for Disease Prevention and Control. Editorial guidance – inclusive writing at ECDC. Stockholm: ECDC; 2026.
> Catalogue number: TQ-01-26-079-EN-N; doi: 10.2900/3750039; ISBN: 978-92-9498-934-5

This skill is an independent adaptation and is not produced, endorsed or reviewed by ECDC. Any errors in how the guidance is encoded are ours. Questions about the guidance itself: ECDC Editorial Office, editors@ecdc.europa.eu.

## Citing this skill

If you find it useful, you are welcome to cite it, though you don't have to. GitHub's "Cite this repository" button (from [`CITATION.cff`](CITATION.cff)) gives APA and BibTeX. Please also cite the ECDC guide above, which is the source of the content.

> Azam J. inclusive-writing-in-public-health: a Claude Code skill for checking inclusive language in public health writing (v0.1.2) [software]. 2026. https://github.com/jamesmbaazam/inclusive-writing-in-public-health

```bibtex
@software{azam_inclusive_writing_in_public_health_2026,
  author  = {Azam, James},
  title   = {inclusive-writing-in-public-health: a Claude Code skill for checking inclusive language in public health writing},
  version = {0.1.2},
  year    = {2026},
  url     = {https://github.com/jamesmbaazam/inclusive-writing-in-public-health},
  license = {MIT}
}
```

## Limitations

- Pattern matching, not understanding: it will miss things and over-flag some.
- English only, as in the source guide.
- The guide says there are "no black-and-white or final answers"; treat suggestions as prompts for discussion, not rules.
- Not legal or clinical advice.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes are recorded in [CHANGELOG.md](CHANGELOG.md).

## Licence

MIT, see [LICENSE](LICENSE). This covers the code and original text in this repository. The ECDC guidance that the rules are based on remains the work of ECDC and is not covered by this licence.
