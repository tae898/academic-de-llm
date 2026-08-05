# Grep patterns

Every pattern is a finder, not a verdict. Read each hit before changing it. Tier numbers match `SKILL.md`, and both files are ordered by measured frequency in agent-written text rather than by evidential strength.

## Tools

`rg` ([ripgrep](https://github.com/BurntSushi/ripgrep)) is the documented default. It behaves identically on Linux, macOS, and Windows, and it is the only common tool that handles the Unicode and multiline patterns below.

Three patterns cannot be expressed in POSIX ERE at all, because multiline matching and Unicode property classes do not exist there. GNU grep can do two of them with `-P`; macOS ships BSD grep with no PCRE compiled in, so there is no single `grep` invocation that works on both platforms. Those three are marked **rg only**. Every other pattern has a portable `grep -E` fallback that works on GNU, BSD, and ugrep.

Run step zero from `SKILL.md` before any of this. Excluding code blocks, tables, and frontmatter is what keeps the false-positive rate survivable.

## Tier 1: formatting

Highest yield. Measured across 35 agent-era READMEs, 51k words.

### Em dash (91% of files, 122 per 10k words)

```bash
rg -n '—'
grep -rInE '—' .          # portable
```

Exclusions are not optional here. On one real paper this returned 8 hits and 2 were worth fixing; the rest were three code comments, a table "not applicable" cell, and two numeric en dashes. Never touch a dash inside code, a table placeholder, or an en dash in a numeric range (`0.88–0.98`).

### Inline-header bold list (49% of files, 46 per 10k words)

```bash
rg -n '^\s*[-*] \*\*[^*]+\*\*\s*[:—-]'
grep -rInE '^[[:space:]]*[-*] \*\*[^*]+\*\*[[:space:]]*:' .    # portable, colon form only
```

A real hit is three sentences wearing a costume. Not a hit when the items are genuinely parallel and meant to be scanned, such as a flag reference.

### Title case headings (83% of files, 22 per 10k words)

```bash
rg -n '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]'
grep -rInE '^#{1,6} .*[a-z] [A-Z][a-z]+ [A-Z]' .               # portable
```

False positives on headings full of proper nouns ("Deploying With Docker And Kubernetes" is a hit; "Using PostgreSQL With Django" is not).

### Emoji (11% of files, 2.7 per 10k words) — rg only

```bash
rg -n '\p{Emoji_Presentation}'
rg -n '^#{1,6} .*\p{Emoji_Presentation}'      # emoji in headings specifically
```

No portable equivalent. `grep -E '[\x{1F300}-\x{1FAFF}]'` fails with "Invalid range end" because `\x{...}` is not ERE syntax, and the `-P` form does not exist on macOS.

### Curly quotes (0% of files here, still common in text from word processors) — rg only

```bash
rg -n '[\x{201C}\x{201D}\x{2018}\x{2019}]'
```

Written as codepoint escapes on purpose. A literal `["]` pattern gets straightened by editors and autocorrect, which silently inverts the check into one that matches every straight quote and no curly ones.

### Heading level skips — rg only

```bash
rg -nU '(?m)^##\s.*\n(?:.*\n)*?^####\s'
```

Needs multiline matching. GNU `grep -P` is line-based and returns nothing here even on files that do skip a level, which is worse than an error because it looks like a pass.

### Thematic breaks and stray boldface

```bash
rg -n '^\*\*\*$'
rg -n '\*\*[^*\n]{1,40}\*\*' -c        # boldface density per file
```

Do not match `^---$` for thematic breaks. It hits the YAML frontmatter delimiter in every Markdown file that has frontmatter, including this skill's own.

## Tier 2: structure

Model-level habits, so they survive across vendors and model generations.

| Pattern | Pattern string | A real hit looks like |
|---|---|---|
| Copula avoidance (34% of files) | `\b(serves as\|stands as\|functions as\|boasts\|features\|maintains\|offers)\b` | A plain `is`/`are` dressed up |
| Superficial `-ing` analysis | `, (highlighting\|underscoring\|emphasizing\|ensuring\|reflecting\|contributing to\|allowing\|enabling)` | An `-ing` clause after a comma that editorializes about the sentence it hangs off. Not a hit when the word is a noun ("the logging config") |
| Negative parallelism | `not just .* but`, `not .*, but rather`, `rather than simply` | A false contrast erected so the next clause can knock it down. Not a hit when correcting a real prior claim |
| Undue emphasis | `stands as`, `is a testament`, `plays a (crucial\|pivotal\|vital) role`, `indelible mark` | Generic importance where a specific fact belongs |
| Vague attribution | `Observers have`, `Experts (argue\|say)`, `Industry reports`, `several sources`, `it is widely` | Attribution to nobody. Name them or drop it |
| False ranges | `from .{0,40} to .{0,40}, from` | "from X to Y" where X and Y are not on a common scale |
| Challenges formula | `[Dd]espite .* (faces\|challenges)` | "Despite its X, it faces several challenges", then vague optimism |
| Rule of three | (no pattern) | Read comma lists of exactly three. Delete a third that measures nothing |
| Elegant variation | (no pattern) | One thing called three names across a page. One thing, one name |

```bash
rg -n '\b(serves as|stands as|functions as|boasts|features|maintains|offers)\b'
grep -rInE '\b(serves as|stands as|functions as|boasts|features|maintains|offers)\b' .   # portable
```

## Tier 3: excess vocabulary

26% of files, 2.4 per 10k words. Source: Kobak et al. 2025, measured against a 2021 to 2022 counterfactual over 14.2M abstracts.

```bash
# Their ten strongest markers, plus the highest frequency ratios. Count per file.
rg -oN '\b(delves?|delving|showcasing|showcases?|underscores?|underscoring|crucial|comprehensive|enhancing|exhibited|insights|notably|particularly|additionally|potential|findings)\b' \
  | cut -d: -f1 | sort | uniq -c | sort -rn

# portable
grep -rInoE '\b(delves?|delving|showcasing|showcases?|underscores?|underscoring|crucial|comprehensive|enhancing|exhibited|insights|notably|particularly|additionally|potential|findings)\b' . \
  | awk -F: '{print $1}' | sort | uniq -c | sort -rn
```

Density is the signal, not presence. Every one of these is a legitimate word. One per paragraph is nothing; four doing no work is the tell. A banned-word list is the failure mode of every other tool in this space.

Wikipedia's independently compiled list, for cross-checking:

```bash
rg -oN '\b(tapestry|testament|realm|landscape|intricate|meticulous|pivotal|robust|vibrant|enduring|commendable|garner|foster(ing)?|interplay|align with)\b'
```

## Tier 4: paste-era artifacts

Measured 0% in both corpora. These are web-interface citation renderings, so they only appear in text pasted out of a chat window. Keep the check because it costs one command, but it will almost never fire on agent-written text.

```bash
rg -n 'contentReference|oaicite|turn0search[0-9]|\[cite: ?[0-9]+\]|span_[0-9]+\]\(start_span|grok_card|grok_render_citation_card_json|attached_file|ppl-ai-file-upload|【|utm_source='

# portable
grep -rInE 'contentReference|oaicite|turn0search[0-9]|\[cite: ?[0-9]+\]|span_[0-9]+\]\(start_span|grok_card|grok_render_citation_card_json|attached_file|ppl-ai-file-upload|【|utm_source=' .
```

## Unsourced patterns

Own observation, kept separate on purpose. See `sources.md`.

```bash
rg -n 'may potentially|can sometimes|might possibly|could potentially|generally tends'   # stacked hedges
rg -n '^(Moreover|Furthermore|Additionally|Consequently)'                                # glue words: >1 consecutive
rg -n "In summary|In conclusion|Ultimately|Let's dive|Here's the thing|Let me be clear"  # bookends
rg -n 'significantly|dramatically|substantially|considerably|markedly'                   # intensifier with no number
```

All four have portable `grep -rInE` equivalents with the same pattern string.

Anchor `In this section` to the start of a sentence. Mid-sentence it is usually legitimate scoping ("every measurement reported in this section").

## False positives seen in practice

| Corpus | Pattern | Hits | Real | The rest were |
|---|---|---|---|---|
| One LaTeX/Markdown paper | em dash | 8 | 2 | 3 code comments, 1 table placeholder, 2 numeric en dashes |
| One LaTeX/Markdown paper | `In this section` | 1 | 0 | a legitimate scoping reference |
| 278 marketplace entries | writing-tool keywords | 48 | 0 | `docs` matched doc tools, `write` matched SQL, `style` matched UI themes |

A pass that changed every hit would have corrupted a table and three code samples.

## Never touched

Code blocks, inline code, identifiers, CLI flags, file paths. YAML, TOML, and JSON frontmatter or config. Markdown tables, including cells that use a dash as a placeholder. Task lists, footnotes, and citation blocks. Quoted error messages and log lines. Direct quotations from other people. En dashes in numeric ranges. Anything written before November 2022.
