# Examples

Seven fixtures, one per academic register the skill claims plus a trap. They are
also the test corpus for `tests/check.sh`, so they cannot drift from what the
patterns actually do.

| File | Role |
|---|---|
| `paper-before.tex` | A LaTeX related-work section. The **paper** branch, where the markup section does not apply. |
| `paper-after.tex` | The same section, de-LLM'd. |
| `prose-before.md` | A real 2026 journal abstract. The **abstract** branch, where there is no markup to check. |
| `prose-after.md` | The same abstract, de-LLM'd. |
| `blog-before.md` | An academic blog post in Markdown. The **blog** branch, the only one where you chose the formatting. |
| `blog-after.md` | The same post, de-LLM'd. |
| `false-positive-trap.md` | Legitimate academic prose. Patterns fire. Correct output is no change. |

Three pairs because `SKILL.md` branches on who chose the formatting, and the
branches do genuinely different work.

## paper-before.tex to paper-after.tex

The fixture for the case this skill exists for. What fires, and what happens:

| Pattern | before | after | |
|---|---|---|---|
| Unmeasured quality claim | 1 | **0** | `provides an efficient and reliable framework` |
| `remains` (persistence) | 2 | **2** | **both kept** |
| Superficial `-ing` | 3 | 0 | `providing`, `thereby enabling`, `highlighting` |
| Negative parallelism | 1 | 0 | `Unlike prior studies…, this work emphasises` |
| Undue emphasis | 2 | 0 | `is crucial for`, `highlighting the importance of` |
| Stacked hedge | 1 | 0 | `may potentially` → `may` |
| Bare intensifier | 1 | 0 | `significantly improving` → the mechanism |
| Excess vocabulary | 9 | **1** | one `robust` survives |
| `---` em dash | 1 | **1** | **kept** |
| `\section{Related Work}` | title case | **unchanged** | **kept** |

### `remains` must survive, in both files

`paper-before.tex` and `paper-after.tex` both contain two uses of `remains`:
"Tabular $Q$-learning **remains** the canonical starting point" and
"Coordination across corridors **remains** an open problem". Neither is a
dressed-up copula. `remains` means *continues to be, despite prior work*, and
`is` is grammatically substitutable while dropping the reason the paper exists.

This is a regression test for a mistake the repo made. A judge panel scored 21
instances of `X remains a challenge` as genuine tells, unanimously, because it
was handed a regex match rather than a sentence. `remains` was in the trigger
list for months as a result. The assertion exists so it cannot come back.

Meanwhile "Our two-branch design **provides an efficient and reliable
framework**" does go: it rates the work and reports no measurement.

### The two that must NOT be touched

`\section{Related Work}` is title case and stays title case. Section headings in
a paper are the venue's convention, not a choice the author made, and
sentence-casing them is not de-LLMing — it is breaking the submission.

The `---` in `phase stability---a distinction` also stays. Em dash in full papers
measured 3.1 to 4.9 per 10k across the ChatGPT boundary, on a base so small that
one document holds a third of all matches. It is not a usable signal in a paper,
and the markup section is skipped there for exactly that reason.

Both are cases where the skill's own measurements say to do nothing, and both are
what a naive "remove the AI tells" pass gets wrong.

### `\cite{}`, `$Q$`, `4--9`

Four citations, one inline math span, and a numeric range written with a LaTeX
en dash. Step zero excludes all of them. `4--9` is the trap: it looks exactly
like a dash tell and is a page range in disguise.

### The one `robust` that survives

`robust to sensor dropout` is a measured property with two studies behind it.
The other eight vocabulary markers were decorative and went. That ratio, not the
count, is the point.

## prose-before.md to prose-after.md

`prose-before.md` is a real *Sensors* abstract from 2026, taken unedited from
PubMed. An abstract has no markup at all, so unearned evaluation is the whole
job.

| Tell | before | after | |
|---|---|---|---|
| Unmeasured quality claim (`offers an efficient`) | 1 | 0 | |
| Copula, other (`boasts`) | 1 | 0 | |
| Superficial `-ing` clause | 1 | 0 | |
| Intensifier with no number (`significantly`) | 1 | 0 | |
| `robust` / `robustness` | 4 | **4** | **all kept** |

192 words to 131.

### Rhythm was preserved deliberately

`prose-after.md` keeps a long sentence next to short ones, and no two
consecutive sentences open with the same subject.

That is not decoration. Measured against a naive de-slop prompt, this skill made
text flatter four times as often and produced edits judged worse 13% of the time
where the naive prompt produced none, by splitting long sentences at every
participle until the paragraph became uniform declaratives. The second directive
in `SKILL.md` exists because of that measurement, and this fixture is what
obeying it looks like.

### Why `robust` survives all four times

`robust` is currently the fastest-*rising* vocabulary tell measured, 3.2x its
pre-ChatGPT baseline and up 50% since 2024 while `crucial` and `delve` collapsed
back to baseline. A banned-word list would strip all four.

Read them in context and none can go. "lack of robustness" is a stated defect of
classic RL algorithms. "hyperparameter robustness" is one of three named
experiment types. "model robustness" is a measured outcome. The word is carrying
a technical meaning every time, which is the situation the vocabulary section
describes: the signal is density and co-occurrence, not presence.

`significantly` went in the same sentence, because no number supports it and the
underlying claim ("improves sample utilization efficiency") survives without it.
That is the first directive: the tell goes, the claim stays.

## blog-before.md to blog-after.md

The only register where the markup section applies, because the author chose the
formatting. It carries one instance of every pattern in `patterns.md`, including
the rare ones the other fixtures have no natural home for.

| Pattern | before | after | |
|---|---|---|---|
| Em dash | 3 | **2** | one converted, two protected |
| Inline-header bold list | 6 | **3** | three converted, three kept |
| Title case headings | 5 | 0 | |
| Emoji, curly quotes, thematic break, H2→H4 | 1 each | 0 | |
| Unmeasured quality claim | 1 | **0** | |
| `remains` (persistence) | 1 | **1** | **kept** |
| Copula, other | 3 | 0 | |
| Superficial `-ing` | 3 | 0 | |
| Negative parallelism, challenges formula | 1 each | 0 | |
| Vague attribution, stacked hedge | 1 each | 0 | |
| Paste artifact (`:contentReference[oaicite:3]`) | 1 | 0 | |
| Excess vocabulary | 9 | **1** | |

The bolded rows are the point. A pass that drove every count to zero would be
**wrong**.

### The two em dashes that must survive

```
| Grid 3x3 | 77.4s | — | not run |        <- table "not applicable" cell
# credit decays by lambda each step — …   <- code comment
```

Step zero excludes both. The third, in the opening line of prose, is the only
one that should change. A tool reporting "3 em dashes fixed" here has corrupted a
table and a code comment.

### The three bold list items that must survive

The `Hyperparameters` list and the `two algorithms` list are identical to a
regex. The difference is judgment:

- the algorithm list is three sentences wearing a costume, and becomes a
  paragraph
- the hyperparameter list is a reference people scan for a value, and stays

This is the hardest call the skill asks for, so the fixture contains one of each.

### The same word, deleted once and kept once

`robust convergence across every seed` is decorative and goes. `robust to 10%
dropout and not to a dead detector` is a measured claim and stays. Both are in
the same document, which is what "density and co-occurrence, not presence" means
in practice.

### What was preserved on purpose

"Reported delay **may** vary with the demand profile you simulate" keeps its
hedge. Stripping `may potentially` down to `may` elsewhere removes the stacked
hedge without touching the uncertainty. Deleting a hedge entirely would make the
sentence claim more than the evidence supports, which the first directive
forbids.

The challenges formula became a fact. "Despite its comprehensive coverage of the
four topologies, the method faces several challenges around detector
reliability, which we are actively working to address" is 27 words that say
nothing. The rewrite names the failure: a dead detector reports zero flow rather
than an error. The vague attribution ("Experts argue…") had no fact under it at
all and was deleted rather than rewritten.

## false-positive-trap.md

The most important fixture. Legitimate academic prose that trips the finders
anyway. **The correct output is no changes at all.**

Eleven hits across six patterns, zero of them real:

| Hits | Pattern | Why every one is rejected |
|---|---|---|
| 4 | em dash | table placeholder, code comment, Python string literal, quoted error |
| 3 | inline-header bold list | a notation table: parallel, scanned not read |
| 2 | `crucial` | one doing real work in live prose, one inside a 2019 quotation |
| 2 | copula-ish (`stands as`, `serving as`) | both inside the same 2019 quotation |
| 1 | title case | `## Monte Carlo Tree Search`, capitalised by convention |
| 1 | superficial `-ing` (`underscoring`) | inside the same quotation |

The quoted 2019 design note is the sharpest case. It is dense with tells
(`stands as`, `crucial`, `robust`, `serving as`, `underscoring`) and it predates
ChatGPT by three years, so it cannot be machine-generated whatever it looks
like. It is also someone else's words, which step zero excludes twice over.

One case is worth knowing about because it is luck rather than design.
`## Training BERT With PyTorch` does **not** fire the title-case pattern:
`[A-Z][a-z]+` cannot match `BERT`, and the word before `With` ends in a capital,
so the run breaks. Nothing in the pattern understands proper nouns.
`## Monte Carlo Tree Search`, two headings later, fires normally. Do not mistake
the first for a guard.

The file also holds an en dash in a numeric range and a real rule of three.

Cleaning up bad prose is easy. Correctly changing nothing is the harder test,
and it is the one most tools in this space fail.
