# Patterns

Regex strings, ordered by what they are worth on an academic document.
Structure first: it is the only section with a measured baseline behind it and
the only one that applies to every document here.

Two rules before you match anything.

**Run the skip pass first.** Code blocks and inline code, frontmatter, tables including dash placeholders, task lists, footnotes, quotations, error messages, identifiers, CLI flags, file paths, en dashes in numeric ranges, and anything written before November 2022. Report what you skipped.

**Every pattern is a finder, not a verdict.** Read each hit in context before changing it. The false-positive table at the bottom is what happens when you do not.

**Case.** Structure and vocabulary are matched **case-insensitively**, which is how the precision and recall figures below were scored. Matching them case-sensitively silently drops every sentence-initial instance, and `Unlike prior work, this study...` is the most common form of one of them. Markup is the opposite: title case cannot be detected without case.

## Structure

Model-level habits, so they survive across vendors and model generations. The
section with a measured baseline behind it, and the one to run on every
document. Rises 2-4x against pre-ChatGPT text in both abstracts and full
papers, and held while the vocabulary below decayed.

These four are re-scored every review cycle: one judge panel labels every hit
real or a words-matched false positive, a second panel reads the same texts cold
to find what the patterns missed. Currently **74% recall at 51% precision**,
against 8% and 32% for the version that shipped in v0.3.1. Per-trigger strengths
are in the notes column; see `research/EVAL.md`.

| Pattern | Regex | A real hit |
|---|---|---|
| Copula avoidance | `\b(serves? as\|serving as\|stands? as\|functions? as\|boasts?\|offers?\|remains?\|positions? \w+ as\|presents? a\|provides? an? [\w\s]{0,24}?(solution\|approach\|framework\|means\|basis))\b` | A plain `is` or `are` dressed up. `serves as` is real every time. `provides` only in the copular form (`provides an effective solution`), which is why it is narrowed: bare, it scored 1 in 6. Not a hit when the verb does real work, since "maintains 35 FPS" is behaviour over time |
| Superficial `-ing` analysis | `[, ](highlighting\|underscoring\|emphasizing\|ensuring\|reflecting\|contributing to\|providing\|enhancing\|allowing\|helping\|supporting\|maintaining\|thereby \w+ing)\b` | An `-ing` clause that editorialises about the sentence it hangs off. **The space alternative is load-bearing**: requiring a comma missed "sensor signals enabling precise detection". `enabling` was dropped after 0 real in 16 matches; `helping`, `supporting`, `maintaining` were added from confirmed misses |
| Negative parallelism | `not just .{0,60} but\|not only .{0,60} but\|unlike .{0,80}?\b(this work\|this study\|we\|our)\b` | A false contrast erected so the next clause can knock it down. `unlike X, this work Y` is the form that occurs. **Precision 0% on this corpus**: the cold-reading panel finds instances the adjudicating panel then rejects. Treat hits as a hint, not a finding |
| Undue emphasis | `\b(pivotal\|invaluable)\b\|\bis (crucial\|essential\|vital\|critical)\b\|plays a (crucial\|pivotal\|vital) role\|is a testament\|significant potential\|highlighting the importance` | Generic importance where a specific fact belongs. The strongest of the four at 89% real. `is crucial` and `is essential` are near-certain. Bare `pivotal` is weaker and kept anyway, because a miss costs more than a false positive |
| Vague attribution | `Observers have`, `Experts (argue\|say)`, `Industry reports`, `several sources`, `it is widely` | Attribution to nobody. Name them or drop the claim |
| False ranges | `from .{0,40} to .{0,40}, from` | "from X to Y" where X and Y are not on a common scale |
| Challenges formula | `[Dd]espite .* (faces\|challenges)` | "Despite its X, it faces several challenges", then vague optimism |
| Rule of three | no regex | Read comma lists of exactly three. Delete a third that measures nothing |
| Elegant variation | no regex | One thing called three names across a page. One thing, one name |

## Vocabulary

Source: Kobak et al. 2025, measured against a 2021 to 2022 counterfactual over
15.1M abstracts. **This list is a snapshot and decays**: `crucial` fell 85% and
`delve` vanished between 2024 and 2026, while `robust` rose 50%. Re-measure
before trusting it.

Their strongest markers, plus the highest frequency ratios:

```
\b(delves?|delving|showcasing|showcases?|underscores?|underscoring|crucial|
comprehensive|enhancing|exhibited|insights|notably|particularly|additionally|
potential|findings)\b
```

Wikipedia's independently compiled list, for cross-checking:

```
\b(tapestry|testament|realm|landscape|intricate|meticulous|pivotal|robust|
vibrant|enduring|commendable|garner|foster(ing)?|interplay|align with)\b
```

**Count per paragraph rather than flagging occurrences.** Every one of these is legitimate English. One is nothing. Four in a paragraph, none doing work, is the signal. A banned-word list is the failure mode of every other tool in this space.

## Markup

Only for a document whose formatting you chose. No academic corpus can
measure these: an abstract has no markup and the full-text corpus does not
preserve it. See `sources.md`.

| Pattern | Regex | A real hit |
|---|---|---|
| Em dash | `—` | Prose using a dash for emphasis or clause separation. Comma if the tail is a modifier, full stop if it is its own claim, parentheses if it is an aside. Never a semicolon. Doubled in arXiv abstracts 2020 to 2026; flat in full papers, so it is the one entry here that applies to prose too |
| Inline-header bold list | `^\s*[-*] \*\*[^*]+\*\*\s*[:—-]` | Three sentences wearing a costume. Not a hit when items are genuinely parallel and meant to be scanned, such as a parameter table. |
| Title case heading | `^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]` | `## Getting Started With The Config`. Not a hit when the capitals are proper nouns (`Learning With Gaussian Processes`). |
| Emoji | `\p{Emoji_Presentation}` | Emoji as bullets, separators, or heading decoration. |
| Curly quotes | `[\x{201C}\x{201D}\x{2018}\x{2019}]` | Curly quotes where straight ones belong. Written as codepoint escapes because a literal pattern gets straightened by editors, which silently inverts the check. Common in text pasted through a word processor |
| Heading level skip | `(?m)^##\s.*\n(?:.*\n)*?^####\s` | H2 straight to H4. Needs multiline matching. |
| Thematic break | `^\*\*\*$` | A rule inserted before a heading. Do **not** match `^---$`, which hits YAML frontmatter in every Markdown file. |
| Excessive boldface | `\*\*[^*\n]{1,40}\*\*` | Count per file. Bolding terms mid-paragraph as "key takeaways". |

## Paste artifacts

Zero hits across every corpus measured here. These are web-interface citation
renderings and only appear when someone pastes out of a chat window into a
draft, which is the one thing a manuscript does that an agent-written file does
not. One pass, near-conclusive when it fires.

```
contentReference|oaicite|turn0search[0-9]|\[cite: ?[0-9]+\]|
span_[0-9]+\]\(start_span|grok_card|grok_render_citation_card_json|
attached_file|ppl-ai-file-upload|【|utm_source=
```

Also check DOIs that resolve to unrelated papers, invalid ISBNs, and named references declared but never used.

## Unsourced patterns

Own observation, kept separate on purpose. See `sources.md`.

| Pattern | Regex |
|---|---|
| Stacked hedges | `may potentially\|can sometimes\|might possibly\|could potentially\|generally tends` |
| Glue words, flag only when consecutive | `^(Moreover\|Furthermore\|Additionally\|Consequently)` |
| Bookends | `In summary\|In conclusion\|Ultimately\|Let's dive\|Here's the thing\|Let me be clear` |
| Intensifier with no number | `significantly\|dramatically\|substantially\|considerably\|markedly` |

Anchor `In this section` to the start of a sentence. Mid-sentence it is usually legitimate scoping, as in "every measurement reported in this section".

## False positives seen in practice

| Corpus | Pattern | Hits | Real | The rest were |
|---|---|---|---|---|
| One LaTeX/Markdown paper | em dash | 8 | 2 | 3 code comments, 1 table placeholder, 2 numeric en dashes |
| One LaTeX/Markdown paper | `In this section` | 1 | 0 | a legitimate scoping reference |
| `examples/false-positive-trap.md` | em dash | 4 | 0 | table placeholder, code comment, string literal, quoted error |

A pass that changed every hit would have corrupted a table and three code samples.
