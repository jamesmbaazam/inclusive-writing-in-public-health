---
name: inclusive-writing-in-public-health
description: Check and fix non-inclusive, stigmatising or dehumanising language in PUBLIC HEALTH writing (manuscripts, reports, protocols, slides, docx/md/qmd/tex), following the ECDC "Inclusive writing" editorial guidance (Nov 2026). Use when the user asks to check, review, edit, audit or fix inclusive language, stigma, person-first wording, "vulnerable/high-risk/hard-to-reach" terms, "case" used for people, combative language ("target", "tackle"), blame-implying wording, or asks for an inclusive-language pass on a document.
---

# Inclusive writing in public health (ECDC guidance)

> **Scope: public health only.** The rules come from guidance written for public-health and infectious-disease communication. They may not apply, or may even be inappropriate, in other fields (e.g. clinical or legal terms with a fixed meaning, other disciplines' conventions, or identity-first language preferred by a community). If the text is not public-health writing, say so to the user and apply the rules sparingly.

Source: European Centre for Disease Prevention and Control. *Editorial guidance – inclusive writing at ECDC*. Stockholm: ECDC; 2026. https://www.ecdc.europa.eu/en/publications-data/inclusive-writing-ecdc (the PDF is not bundled; read it at that link). The guide is **not prescriptive**: it supports judgement. Many issues have no single right answer; when unsure, write as **clear and specific** as possible (plain language). English only.

## Workflow

1. **Locate the text.** A file, a folder, or text pasted in chat (write pasted text to a scratch file first).
2. **Run the scanner** (stdlib Python 3, no installs):
   ```bash
   python3 ~/.claude/skills/inclusive-writing-in-public-health/scripts/check_inclusive.py PATH [PATH...]
   ```
   - `!` = clear match; `?` = context-dependent (may be fine, e.g. "target" in a statistical sense, "general population" in a survey-sampling frame, "MSM" in a cited source).
   - `--no-context` hides `?` rules; `--json` for structured output; handles `.md .qmd .Rmd .tex .txt .rst .html .docx` (docx is report-only). Fenced/inline code is skipped in Markdown/Quarto.
   **Optional second pass with [alex](https://github.com/get-alex/alex)** (general-purpose linter for gendered, racial, ableist, LGBTQ+, condescending and profane wording; it does *not* cover the public-health items above, so it complements rather than replaces step 2):
   ```bash
   command -v npx >/dev/null && npx --yes alex@11.0.1 PATH --why      # .md/.txt (default)
   # plain text: add --text   |   HTML: add --html   |   MDX: add --mdx   |   stdin: echo "..." | npx --yes alex@11.0.1 --stdin
   ```
   - If `npx`/Node is missing, skip this pass and say so in the report; don't install Node unasked. Pinning `@11.0.1` runs a known version; mention to the user that `npx` downloads it from npm on first use.
   - Tested with alex 11.0.1 on Node 26 (macOS/Homebrew; if `npx` isn't found, try `export PATH=/opt/homebrew/bin:$PATH`). First run prints harmless `npm warn deprecated …` lines; ignore them. Output is `line:col  warning  message  rule-id`, then the rule's note with `--why`.
   - Alex parses Markdown/HTML, so it ignores code and front matter, and it honours `.alexrc` / an `alex` field in `package.json` if the project has one. It exits non-zero when it finds something, which is normal.
   - Mute a justified finding with `<!--alex ignore rule-id-->` (or `.alexrc` `allow`) only if the user agrees; otherwise fix or leave it for the author. Not all alex rules suit scientific text (e.g. profanity matches like "butt" or "addict"; use `--why` to see the rule id and judge in context).
   - Merge alex's findings with the scanner's in one list. Where both flag the same span, use the ECDC suggestion.
3. **Read the findings in context, then also read the text yourself.** The scanner is regex-only; it misses things in the "Judgement checks" below. Discard false positives (quotations, proper nouns, titles of cited works, formal case definitions, established terms such as "communities" in STI prevention, identity-first language a group prefers, e.g. many autistic/Deaf people).
4. **Fix.**
   - *Mechanical, safe* terms can be auto-fixed: `check_inclusive.py PATH --fix` (dry-run diff), then `--fix --write` to apply. Safe set: GBMSM, PLHIV, HCW, PWID, birth defects, herd immunity, vaccine hesitancy, mother-to-child transmission. Always review the diff (grammar, article agreement, singular/plural, "define at first use" for *vertical transmission*).
   - *Everything else* needs a rewrite by hand: edit with the Edit tool, keep the author's meaning, numbers and citations intact, and **never alter direct quotations, reference titles, data labels or code** without asking.
   - Where the fix needs facts you don't have (which countries? which groups? why higher risk? age cut-off for "older adults"?), **don't invent them**. Insert a bracketed placeholder like `[name the specific countries]` or ask the user.
5. **Report.** Summarise: files checked, number of changes by category, items left for the author's decision (with reason), and a note on anything you deliberately left unchanged (quotes, preferred identity-first terms). Re-run the scanner to confirm what remains is intentional.

If the user only asked to *check*, report and propose; don't edit. Default to non-destructive: prefer `--fix` dry-run, and edit copies or tracked files only when asked.

## Core principles (what to apply when reading)

**2.1 Avoid dehumanising language**
- Spell out abbreviations for people (GBMSM, PLHIV, HCW, PWID).
- Person-first: people *with/living with/experiencing/who* … not "the homeless", "diabetics", "drug users", "smokers", "prisoners/inmates" (→ people in prison/detention), "prostitute" (→ sex worker), "the elderly" (→ older adults, define age), "healthy people" (→ people without [condition]), "sick people", "infected people" (→ people with an infection). Use *who*, not *that*, for people. Use "patient" only for someone receiving care.
- **"Case"** = an occurrence of disease, not a person. Test: if "case" can be swapped for "disease/infection" it's right; if for "person", rewrite ("7 000 cases were children" → "7 000 cases of measles were diagnosed in children"; "the case is recovering" → "the affected individual is recovering"). Use sparingly for people even when meeting a case definition. Use "contact" sparingly for people.
- Foreign-born → people born outside [country / the reporting country / EU/EEA].

**2.2 Be specific, avoid generalisations**
- Replace vague labels (*vulnerable, marginalised, hard-to-reach, high-risk / at-risk / risk groups, key populations unexplained*) by naming **who**, **at higher risk of what**, and ideally **why** (structural/behavioural cause, not inherent to the group). Define "high risk" concretely where possible.
- Avoid "general population" next to other groups, "sub-populations", "atypical populations". Prefer "group/population" over "community" unless established.
- "EU citizens" → EU residents/population. Migrants → refugees / asylum seekers / undocumented migrants / newly arrived migrants / people born outside the reporting country.
- *Gay, bisexual and other men who have sex with men* for the community (then "men in this group"); *sex between men* for the transmission mode; *sex between men and women* not "heterosexual contact".
- Pregnancy: "pregnant people", "vaccination during pregnancy" (trans men, non-binary, intersex people can be pregnant).
- Geography: name countries instead of "Eastern Europe", "Africa" etc.; footnote the countries if a region is used.
- Define terms readers may read differently (*chemsex*, *bodily fluids*, *sexual contact*, *vertical transmission*): say which fluids / what type of contact.

**2.3 Avoid negative connotations and implicit bias**
- Outdated terms: birth defects → congenital conditions/disorders; herd immunity → population immunity.
- Combative language: *target, tackle, aimed at, trigger* → engage, prioritise, partner with, serve, tailor to, address, intends to reach, prompt; "target population" → priority/key population or intended audience.
- Blame: don't say someone "transmitted/infected others/spread the virus"; use *contracted/acquired*. Avoid "catch/become infected". Compliant/non-compliant → adherent/non-adherent (mention barriers). "Risk behaviour/activity" → name the behaviour and why it raises risk. "Unprotected sex" → condomless sex / sex without a condom or other prevention (PrEP, dental dams). Vaccine hesitancy → vaccine acceptance. Mother-to-child → vertical transmission (define it). Give the *reason* for higher risk or lower uptake, or say the reason is unknown. "Illegal immigrants" → undocumented migrants.
- Power structures: avoid framing a dominant group as "norm"; use neutral, context-specific wording on income/status; mention race, gender or other identities only when relevant and explain why; avoid hierarchical lists (alphabetise countries and similar).

## Judgement checks the scanner cannot do
- Descriptions of how to *recognise* an affected group (symptoms, lesions) that could lead to ostracism.
- Labelling a group without explaining why; implying a group is the danger or source (e.g. advising avoidance of affected communities).
- Hierarchical or "default vs other" ordering in lists and tables.
- Identities mentioned without relevance to the issue.
- Behaviour linked to higher risk with no explanation.
- Tone: stereotype-consistent phrasing, moral judgement, fear-based framing.

## Notes and limits
- Rules live in `scripts/rules.json` (`pattern`, `suggest`, `why`, guide section, optional `replace` for safe fixes, `context` for judgement-needed). Add or tweak rules there; guidance evolves ("this document will be updated regularly").
- Questions about the guidance itself: ECDC Editorial Office, editors@ecdc.europa.eu. Further reading is listed in the Resources section of the ECDC guide (AMA/AAMC narrative guide, C4DISC, UNAIDS terminology guidelines, NIAID HIV language guide, ASU disability language style guide).
- Not legal or clinical advice; the guide itself says there are "no black-and-white or final answers".
