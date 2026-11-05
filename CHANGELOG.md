# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed
- README install section now tells users to clone the repository and gives the `git clone`, update and version-pin commands.

## [0.1.1] - 2026-11-05

### Added
- Workflow step asking the user for permission to check for an alex (Node/`npx`) installation and, with their agreement, help install it.

### Changed
- README now states that the skill combines the ECDC guidelines with the alex tool.

## [0.1.0] - 2026-11-05

First release.

### Added
- Claude Code skill (`SKILL.md`) for checking and fixing non-inclusive language in public health writing, based on the ECDC editorial guidance *Inclusive writing at ECDC* (2026).
- `scripts/check_inclusive.py`: dependency-free scanner for `.md`, `.qmd`, `.Rmd`, `.tex`, `.txt`, `.rst`, `.html` and `.docx` (report only for docx). Supports `--json`, `--no-context`, and `--fix` (dry-run diff) / `--fix --write` for safe replacements. Skips code in Markdown.
- `scripts/rules.json`: about 50 rules with suggested alternatives, reasons and guide section references; context-dependent rules are marked.
- Optional second pass with [alex](https://github.com/get-alex/alex) (`npx alex@11.0.1`), tested with alex 11.0.1 on Node 26.
- README, CONTRIBUTING guide, MIT licence and `CITATION.cff`.

### Notes
- Scope is public health only; the rules may not suit other fields.
- The ECDC guide is not bundled; see the README for the source link.

[0.1.1]: https://github.com/jamesmbaazam/inclusive-writing-in-public-health/releases/tag/v0.1.1
[0.1.0]: https://github.com/jamesmbaazam/inclusive-writing-in-public-health/releases/tag/v0.1.0
