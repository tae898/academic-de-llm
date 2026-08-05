# Patterns

Regex strings, ordered by measured frequency in agent-written prose.

Two rules before you match anything.

**Run the skip pass first.** Code blocks and inline code, frontmatter, tables including dash placeholders, task lists, footnotes, quotations, error messages, identifiers, CLI flags, file paths, en dashes in numeric ranges, and anything written before November 2022. Report what you skipped.

**Every pattern is a finder, not a verdict.** Read each hit in context before changing it. The false-positive table at the bottom is what happens when you do not.

## Tier 1: formatting

Highest yield. Percentages are files affected across 35 agent-era READMEs, 51k words.

| Pattern | Regex | A real hit | Measured |
|---|---|---|---|
| Em dash | `—` | Prose using a dash for emphasis or clause separation. Comma if the tail is a modifier, full stop if it is its own claim, parentheses if it is an aside. Never a semicolon. | 91%, 122/10k |
| Inline-header bold list | `^\s*[-*] \*\*[^*]+\*\*\s*[:—-]` | Three sentences wearing a costume. Not a hit when items are genuinely parallel and meant to be scanned, such as a flag reference. | 49%, 46/10k |
| Title case heading | `^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]` | `## Getting Started With The Config`. Not a hit when the capitals are proper nouns (`Using PostgreSQL With Django`). | 83%, 22/10k |
| Emoji | `\p{Emoji_Presentation}` | Emoji as bullets, separators, or heading decoration. | 11%, 2.7/10k |
| Curly quotes | `[\x{201C}\x{201D}\x{2018}\x{2019}]` | Curly quotes where straight ones belong. Written as codepoint escapes because a literal pattern gets straightened by editors, which silently inverts the check. | 0% here, common from word processors |
| Heading level skip | `(?m)^##\s.*\n(?:.*\n)*?^####\s` | H2 straight to H4. Needs multiline matching. | |
| Thematic break | `^\*\*\*$` | A rule inserted before a heading. Do **not** match `^---$`, which hits YAML frontmatter in every Markdown file. | |
| Excessive boldface | `\*\*[^*\n]{1,40}\*\*` | Count per file. Bolding terms mid-paragraph as "key takeaways". | |

## Tier 2: structure

Model-level habits, so they survive across vendors and model generations.

| Pattern | Regex | A real hit |
|---|---|---|
| Copula avoidance (34%) | `\b(serves as\|stands as\|functions as\|boasts\|features\|maintains\|offers)\b` | A plain `is` or `are` dressed up |
| Superficial `-ing` analysis | `, (highlighting\|underscoring\|emphasizing\|ensuring\|reflecting\|contributing to\|allowing\|enabling)` | An `-ing` clause after a comma that editorializes about the sentence it hangs off. Not a hit when the word is a noun, as in "the logging config" |
| Negative parallelism | `not just .* but`, `not .*, but rather`, `rather than simply` | A false contrast erected so the next clause can knock it down. Not a hit when correcting a real prior claim |
| Undue emphasis | `stands as`, `is a testament`, `plays a (crucial\|pivotal\|vital) role`, `indelible mark` | Generic importance where a specific fact belongs |
| Vague attribution | `Observers have`, `Experts (argue\|say)`, `Industry reports`, `several sources`, `it is widely` | Attribution to nobody. Name them or drop the claim |
| False ranges | `from .{0,40} to .{0,40}, from` | "from X to Y" where X and Y are not on a common scale |
| Challenges formula | `[Dd]espite .* (faces\|challenges)` | "Despite its X, it faces several challenges", then vague optimism |
| Rule of three | no regex | Read comma lists of exactly three. Delete a third that measures nothing |
| Elegant variation | no regex | One thing called three names across a page. One thing, one name |

## Tier 3: excess vocabulary

26% of files, 2.4 per 10k words. Source: Kobak et al. 2025, measured against a 2021 to 2022 counterfactual over 15.1M abstracts.

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

## Tier 4: paste-era artifacts

Zero hits across 167k words of agent-written text. These are web-interface citation renderings and only appear when a human pastes out of a chat window. Cheap to check, so check, but do not expect anything.

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
| 278 marketplace entries | writing-tool keywords | 48 | 0 | `docs` matched doc tools, `write` matched SQL, `style` matched UI themes |
| `examples/false-positive-trap.md` | em dash | 4 | 0 | table placeholder, code comment, string literal, quoted error |

A pass that changed every hit would have corrupted a table and three code samples.
