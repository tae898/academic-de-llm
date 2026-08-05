# Examples

Six fixtures. They are also the test corpus for `tests/check.sh`, so they
cannot drift from what the patterns actually do.

| File | Role |
|---|---|
| `before.md` | A realistic slopped README. Nine pattern families fire. |
| `after.md` | The same document, de-LLM'd. The diff is the demo. |
| `prose-before.md` | A real 2026 journal abstract. The **prose** branch, where Tier 1 finds nothing. |
| `prose-after.md` | The same abstract, de-LLM'd. |
| `false-positive-trap.md` | Legitimate prose. Patterns fire. Correct output is no change. |
| `slopped.md` | Pattern coverage. One planted instance of everything, including the rare ones `before.md` has no natural home for. |

The two pairs exist because `SKILL.md` branches on register and the branches do
genuinely different work. See "The prose pair" below.

## before.md to after.md

`before.md` is modelled on the densest real READMEs in the measurement corpus,
not invented. What fires, and what happened to it:

| Pattern | before | after | |
|---|---|---|---|
| Em dash | 3 | **2** | one converted, two protected |
| Inline-header bold list | 8 | **5** | three converted, five kept |
| Title case headings | 3 | 0 | |
| Copula avoidance | 2 | **1** | one false positive survives |
| Superficial `-ing` | 2 | 0 | |
| Negative parallelism | 1 | 0 | |
| Challenges formula | 1 | 0 | |
| Vague attribution | 1 | 0 | |
| Stacked hedge | 1 | 0 | |

The three bolded rows are the point of the fixture. A pass that drove every
count to zero would be **wrong**.

### The two em dashes that must survive

```
| Inspect latency | 4ms | 22ms | — |          <- table "not applicable" cell
// backoff doubles each attempt — capped …    <- code comment
```

Step zero excludes both. The third dash, in the opening line of prose, is the
only one that should change. A tool that reports "3 em dashes fixed" on this
file has corrupted a table and a code comment.

### The five bold list items that must survive

The `### Flags` list is an inline-header bold list, and the pattern cannot tell
it apart from the hollow `## Key Features` list three sections earlier. Both
look identical to a regex. The difference is judgment:

- `Key Features` is three sentences wearing a costume. It becomes one sentence.
- `Flags` is a reference table people scan for an argument name. It stays.

This is the single hardest call the skill asks for, so the fixture contains one
of each.

### The copula hit that is not a copula

`after.md` still matches the copula pattern once, on the heading
`## Key features`. The regex includes `features` as a verb; here it is a plural
noun in a heading. Nothing to fix. It is in the tests as a permanent reminder
that the count never reaches zero on real text.

### What was preserved on purpose

"this **may** vary depending on your Redis configuration" keeps its hedge.
Stripping `may potentially` down to `may` removes the stacked hedge without
touching the uncertainty. Deleting the hedge entirely would make the sentence
claim more than the benchmark supports, which the Prime Directive forbids.

"pending, active, and failed" survives as a rule of three, because those are
three real states and deleting one loses information.

The challenges formula became a fact: "Despite its comprehensive feature set,
queuectl faces several challenges around cluster mode, which the maintainers are
actively working to address" is 22 words that say nothing. "queuectl does not
support Redis cluster mode" is 8 words that say the thing. The vague
attribution ("Observers have noted…") had no fact under it at all and was
deleted rather than rewritten.

## false-positive-trap.md

The more important fixture. Legitimate technical prose that trips the finders
anyway. **The correct output is no changes at all.**

Eleven hits across five patterns, zero of them real:

| Hits | Pattern | Why every one is rejected |
|---|---|---|
| 4 | em dash | table placeholder, code comment, Python string literal, quoted error |
| 3 | inline-header bold list | a flag reference: parallel, scanned not read |
| 2 | `crucial` | one doing real work in live prose, one inside a 2019 quotation |
| 1 | title case | `## Amazon Web Services`, one proper noun, already correct |
| 1 | copula `stands as` | inside the same 2019 quotation |

The quoted 2019 design document is the sharpest case. It is dense with tells
(`stands as`, `crucial`, `robust`, `serving as`, `underscoring`) and it predates
ChatGPT by three years, so it cannot be machine-generated whatever it looks
like. It is also someone else's words, which step zero excludes twice over.

One case is worth knowing about because it is luck rather than design.
`## Using PostgreSQL With Django` does **not** fire the title-case pattern:
`[A-Z][a-z]+` cannot match `PostgreSQL`, because the internal capitals break the
run. Nothing in the pattern understands proper nouns. `## Amazon Web Services`,
right below it, fires normally. Do not mistake the first for a guard.

The file also holds an en dash in a numeric range and a real rule of three.

Cleaning up bad prose is easy. Correctly changing nothing is the harder test,
and it is the one most tools in this space fail.

## The prose pair

`prose-before.md` is a real *Sensors* abstract from 2026, taken unedited from
PubMed. It is here because every other fixture is Markdown, and the skill's
prose branch had no worked example.

**Tier 1 finds nothing.** No em dashes, no bold lists, no headings, because an
abstract has no markup. On this branch the formatting tier is skipped entirely
and Tier 2 is the whole job.

| Tell | before | after | |
|---|---|---|---|
| Copula avoidance (`boasts`, `offers`) | 2 | 0 | |
| Superficial `-ing` clause | 1 | 0 | |
| Intensifier with no number (`significantly`) | 1 | 0 | |
| `robust` / `robustness` | 4 | **4** | **all kept** |

192 words to 131.

### Why `robust` survives all four times

`robust` is currently the fastest-*rising* vocabulary tell measured, 3.2x its
pre-ChatGPT baseline and up 50% since 2024 while `crucial` and `delve` collapsed
back to baseline. A banned-word list would strip all four.

Read them in context and none can go. "lack of robustness" is a stated defect of
classic RL algorithms. "hyperparameter robustness" is one of three named
experiment types. "model robustness" is a measured outcome. The word is carrying
a technical meaning every time, which is exactly the situation Tier 3 describes:
the signal is density and co-occurrence, not presence.

`significantly` went in the same sentence, because no number supports it and the
underlying claim ("improves sample utilization efficiency") survives without it.
That is the Prime Directive: the tell goes, the claim stays.

### What was dropped, and why it is not a claim

"This work offers an efficient and reliable solution for real-time adaptive
signal control of isolated intersections." The whole sentence went. It is a
self-assessment with no evidence behind it, and the scope it names (isolated
signalized intersections) is already stated earlier. Nothing measurable was
lost.
