# academic-de-llm

[![patterns](https://github.com/tae898/academic-de-llm/actions/workflows/test.yml/badge.svg)](https://github.com/tae898/academic-de-llm/actions/workflows/test.yml)

A Claude Code skill for the last pass over an academic draft: strip the markers
that make a paper read as machine-generated, without flattening the prose or
weakening a claim.

Scoped to scholarly writing on purpose. Papers, abstracts and academic blog
posts, in LaTeX, Markdown and HTML. The measurements behind it come from 1.3M
words of journal abstracts, open-access full texts and arXiv preprints.

Most tools in this space ship a banned-word list. This one is ordered by
measured frequency, cites its sources, and states which of its own rules are
unsourced so you can argue with them.

## The thing nobody had measured

The published research is about vocabulary. Kobak et al. measured which *words*
appear more often in 2024 abstracts than a 2021-22 baseline predicts, and found
`delves` at 28x. Wikipedia's guide lists structural patterns with no numbers at
all. Nobody had put a baseline under the structure.

So I did, on the same journal Kobak measured, split into four windows:

| Tell | 2019-21 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| Superficial `-ing` clause | 1.0 | **9.2** | **12.2** | **6.6** |
| Copula avoidance | 1.7 | 4.1 | 6.8 | **4.5** |
| Kobak's ten markers, combined | 15.5 | 50.9 | 50.8 | 39.4 |
| `crucial` | 1.6 | 6.0 | 4.1 | **1.0** |
| `delve` / `showcase` / `underscore` | 0.0 | 2.0 | 1.3 | **0.2** |
| `robust` | 4.2 | 9.9 | 17.3 | **14.4** |

Per 10k words. Two results worth the trouble.

**The largest excess tell is structural, not lexical.** The superficial `-ing`
clause — "…, highlighting the importance of careful tuning" — rose 8.9x by 2024,
higher than any word Kobak reports for that journal. As far as I know that is
the first excess figure published for a structural tell. That figure uses a
tight probe; the wider regex the skill ships for editing puts it at 3.7x on a
much higher base, and `research/measure.py` prints both.

**The famous words died and the structure did not.** `crucial` is back at its
pre-ChatGPT level and `delve` is effectively gone, down 84% and 89% since 2024.
Publicity kills a word-level tell. Over the same window `-ing` clauses are still
at 6.4x baseline, and `robust` went *up* 46%, so the vocabulary shifts rather
than disappearing.

And one tell has not peaked at all. Under the regexes the skill actually ships,
copula avoidance rises in every window — 10.2, 17.2, 25.8, **27.3** — while
everything else fell back from 2024 or 2025.

That is why the skill puts structure first and tells you to trust the word list
least. It is also why this repo is a measurement pipeline and not just a
document: the word list will be wrong again in a year, and `make review` is how
you find out.

**Caveat, since the skill's own standards demand it.** This is a raw
before-and-after, not Kobak's counterfactual projection, and it cannot separate
LLM effects from five years of drift in one journal's topics or editorial
standards. MDPI introduced AI screening over the same period, and "models
changed" and "editors filtered" would produce the same curve.
`references/sources.md` lists every limitation.

## Install

As a plugin:

```
/plugin marketplace add tae898/academic-de-llm
/plugin install academic-de-llm@academic-de-llm
```

Or drop the skill in directly:

```bash
git clone https://github.com/tae898/academic-de-llm.git
cp -r academic-de-llm/skills/academic-de-llm ~/.claude/skills/
```

Then ask for it by name, or say "de-slop this", "remove the AI tells", "this
reads like ChatGPT".

Nothing to configure. No corpus to build, no state to store, no Python.

## Patterns find candidates, not violations

The single most important thing in the repo, and the reason for
`examples/false-positive-trap.md`.

That file is legitimate academic prose. The raw em dash pattern returns 4 hits
on it and **none of them are real**:

```
49:| Corridor | 44.2s | — |                             <- table placeholder
55:# strip the prefix — the parser needs the bare id    <- code comment
56:run_id = line.split("—")[0]                           <- string literal
61:Error: `simulation reset by peer — retrying`          <- quoted error
```

The correct output on that file is no changes at all. A tool that edited all
four hits would corrupt a table, two lines of working Python, and an error
string. The same file also quotes a 2019 design note that is dense with tells
and therefore cannot be machine-generated, and a `## Monte Carlo Tree Search`
heading that fires the title-case pattern and is already correct.

Measured separately on a real LaTeX paper: 8 em dash hits, 2 worth fixing. The
rest were three code comments, a table placeholder, and two numeric en dashes.

Every pattern here is a finder. Step zero of the skill is a skip pass that
excludes code, tables, frontmatter, quotations, and anything written before
November 2022, and it reports what it skipped so the pass is auditable.

## Sources

| Source | What it is | What it gives |
|---|---|---|
| [Kobak et al. 2025](https://doi.org/10.1126/sciadv.adt3813), *Science Advances* | 15.1M English-language PubMed abstracts. Projects a counterfactual 2024 word frequency from 2021 to 2022 data and measures the gap, so "excess" is a measured quantity. | The vocabulary list with frequency ratios (`delves` at 28.0x) |
| [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | Editors who screen AI text at volume across millions of articles | The structural and formatting taxonomy, and the paste-era artifacts |
| This repo, 2026-08 | 1.9M words, ten corpora, seven publishers: *Sensors*, PLOS ONE, BMJ Open, Nature Communications, PMC full texts, and arXiv `cs.LG`, `cs.AI`, `cs.CL`, `econ.EM`, `math.ST` | Which claimed tells survive a venue they were not tuned on: four of twenty-six |

`references/sources.md` says what each source does **not** establish, and lists
every claim in the skill that has no source behind it. That list exists so the
unsourced parts can be challenged separately from the cited ones.

## What this is not

It is not an AI detector, and the skill says so at length. Population statistics
do not classify individuals. Text written before November 2022 cannot be
AI-generated whatever it looks like. An author who can explain their choices is
an author. Irregular syntax is a human pattern, not a machine one. Use it to
edit, never as evidence about who wrote something.

It does not build a voice fingerprint. Other skills profile your existing
writing and rewrite toward it, which is the most interesting idea in this space.
It is excluded on purpose: it needs stored state and a corpus, and "sounds like
you" cannot be falsified the way the rest of this tries to be.

It does not ban words. Every word on every list here is legitimate English.
`Crucial` in a sentence that establishes why something is crucial is fine. The
signal is density and co-occurrence, not presence.

It does not make text true, well argued, or worth reading.

## Status

**0.1.0**, first release. Below 1.0.0 on purpose: the patterns have changed
materially several times, each because a measurement contradicted the previous
version. The finders that shipped in pre-release 0.3.1 caught 8% of real
instances, which was only found by measuring afterwards. 1.0.0 is for when a
review cycle passes without a finding that forces a rewrite. See
[CHANGELOG.md](CHANGELOG.md).

## Requirements

None to use it.

The skill is three Markdown files that name no tool, no operating system and no
install step. That is deliberate: it is knowledge, not a program, so it runs
wherever Claude runs, Windows included. A test in `tests/check.sh` enforces it,
so the constraint cannot rot.

The **development tooling** is Linux and macOS. `tests/check.sh` needs ripgrep,
and CI runs on `ubuntu-latest` and `macos-latest`. That is a constraint on
contributors, not on users.

## Tests

```bash
sh tests/check.sh    # needs ripgrep
```

84 assertions on seven fixtures, one pair per register: a LaTeX paper, a journal
abstract, and an academic blog post.

Every assertion runs in **both** directions, because over-fixing is the failure
mode this skill was built to avoid. `paper-after.tex` must still contain its
`---` em dash and its title-case `\section{Related Work}`, since both belong to
the venue rather than the author, and both its uses of `remains`, which mark
persistence rather than a dressed-up copula. That last one is a test for a
mistake this repo actually made: the retired verb-list framing scored 21
instances of `X remains a challenge` as tells. `blog-after.md` must still contain two
protected em dashes and a three-item notation list. The trap asserts that all
eleven of its hits are the rejectable kind, and that the correct output is no
change at all. CI runs on `ubuntu-latest` and `macos-latest`.

They exist because v2 shipped four broken patterns. They passed locally only
because the shell aliased `grep` to `ugrep`, which is permissive; on a clean
machine two errored and one silently matched nothing, which is the worse failure
because it looks like a clean pass. One was the curly-quote pattern, whose curly
quotes had been straightened by an editor into the ASCII ones it was meant to
detect.

## Does it beat just asking?

30 real 2026 journal abstracts. Both arms rewritten by the same model, differing
only in whether `SKILL.md` is in the prompt. Judged blind by three models from
three labs, none of them Anthropic (which wrote the skill) or OpenAI (which did
the rewriting).

| | Naive prompt | **de-llm** |
|---|---|---|
| Reads machine-generated, abstracts | 78% | **22%** |
| Reads machine-generated, paper sections | 70% | **30%** |
| Substantively faithful | **99%** | 96% |
| Made prose flatter | **3%** | 16% |

**It works on full-paper sections, which is what it is for.** That register had
never been evaluated until 2026-08-08; everything before that was 200-word
abstracts.

**And it costs something.** On abstracts the skill flattens the prose five times
as often as simply asking, and discards something worth keeping eight times as
often. On sections both costs mostly disappear (6% and 3%), because a 534-word
section has room for varied rhythm that a compressed abstract does not. The
rhythm directive in `SKILL.md` exists because of this measurement and has not
yet fixed it.

One finding from this run is worth more than the numbers. A defect published
that morning — "the skill relocates copula avoidance rather than removing it" —
did not survive reading the instances. Most of what the judge panel called
copula avoidance was `X remains a challenge`, which is not a dressed-up copula:
`remains` means *continues to be, despite prior work*. Classified by what the
construction does rather than which verb it uses, the skill removes **half** of
the real cases and the naive prompt removes none. The retraction and what it
implies are in [`research/EVAL.md`](research/EVAL.md).

Full numbers, both configurations, and the limits in
[`research/EVAL.md`](research/EVAL.md). Reproduce with `make eval`.

## Research

Every measured number in this repo is reproducible, and the process that
produces them is documented because it has to be re-run: between 2024 and 2026
`crucial` fell 85% and `delve` effectively vanished, both back to their
pre-ChatGPT baselines, while the structural tells held.

| | |
|---|---|
| [`research/README.md`](research/README.md) | what each corpus can and cannot measure |
| [`research/REVIEW.md`](research/REVIEW.md) | the quarterly checklist, `make review` |
| [`research/MODELS.md`](research/MODELS.md) | which models produced which result, and the rules for picking them |
| [`research/EVAL.md`](research/EVAL.md) | does this beat just asking an LLM to de-slop. Four judges from four labs, blind. Includes two findings that reversed when the models were made current |

## Related

[`SimpleEnglish`](https://github.com/AminBlg/SimpleEnglish) by
[@AminBlg](https://github.com/AminBlg) applies ASD-STE100 Simplified Technical
English. Not affiliated with this project.

Use that one when a reader might misread the text. Use this one when a reader
might think a machine wrote it. On technical documentation, run both. On a
paper, run only this one, because STE bans the modals that carry your certainty.

## License

MIT, see [LICENSE](LICENSE).

The pattern taxonomy draws on Wikipedia:Signs of AI writing, which is CC BY-SA
4.0. See [NOTICE](NOTICE) for attribution details.
