# de-llm

[![patterns](https://github.com/tae898/de-llm/actions/workflows/test.yml/badge.svg)](https://github.com/tae898/de-llm/actions/workflows/test.yml)

A Claude Code skill that strips the surface markers making text read as
machine-generated, without flattening what it says.

Most tools in this space ship a banned-word list. This one is ordered by
measured frequency, cites its sources, and states which of its own rules are
unsourced so you can argue with them.

## The thing nobody had measured

Every "signs of AI writing" guide predates coding agents. The published research
measured 2024 biomedical abstracts. Wikipedia's guide screens encyclopedia
edits, where AI text mostly arrives pasted out of a chat window. Neither one
measured what an agent writes directly into a file, which is the register most
people now generate text in.

So I measured it. 35 README files from Claude Code plugin repositories, 51,055
words:

| Tell | Files affected | Per 10k words |
|---|---|---|
| Em dash | 91% | **122.4** |
| Inline-header bold list (`- **X**:`) | 49% | **46.4** |
| Title case headings | 83% | **22.3** |
| Copula avoidance (`serves as`, `boasts`) | 34% | 3.1 |
| Excess vocabulary (`crucial`, `robust`) | 26% | 2.4 |
| Emoji | 11% | 2.7 |
| Curly quotes | 0% | 0.0 |
| ChatGPT/Gemini paste artifacts | 0% | 0.0 |

Two results worth the trouble.

Formatting beats vocabulary by ten to fifty times. Every guide leads with the
word lists, and the word lists are the smallest signal in agent-written prose.

The per-vendor artifact strings (`oaicite`, `contentReference`, `grok_card`)
fire **zero times across 167k words**. They are web-interface citation
renderings. They exist only when a human pastes out of a chat window, and an
agent writing to a file never produces them. Older guides call these the
strongest evidence available, and for this register they are dead weight.

This skill is ordered accordingly: formatting first, paste artifacts last.

**Caveat, since the skill's own standards demand it.** There is no baseline
here. This measures prevalence, not excess. Kobak's counterfactual design is
what separates "common" from "more common than it should be," and none of that
is done. A 91% em dash rate is evidence of frequency and nothing more.
`references/sources.md` lists every limitation.

## Install

As a plugin:

```
/plugin marketplace add tae898/de-llm
/plugin install de-llm@de-llm
```

Or drop the skill in directly:

```bash
git clone https://github.com/tae898/de-llm.git
cp -r de-llm/skills/de-llm ~/.claude/skills/
```

Then ask for it by name, or say "de-slop this", "remove the AI tells", "this
reads like ChatGPT".

Nothing to configure. No corpus to build, no state to store, no Python.

## Patterns find candidates, not violations

The single most important thing in the repo, and the reason for
`examples/false-positive-trap.md`.

That file is legitimate technical prose. The raw em dash pattern returns 4 hits
on it and **none of them are real**:

```
11:| Chroma | 12ms | — |                              <- table placeholder
14:# strip the prefix — the parser needs it bare      <- code comment
15:value = line.split("—")[0]                          <- string literal
20:Error: `connection reset by peer — retrying`        <- quoted error
```

The correct output on that file is no changes at all. A tool that edited all
four hits would corrupt a table, two lines of working Python, and an error
string.

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
| This repo, 2026-08 | 35 plugin READMEs and 2,298 plugin descriptions | The ordering |

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

52 assertions on six fixtures. Every pattern fires on the coverage fixture.
The worked example asserts **exact** counts in both directions: `after.md` must
still contain the two protected em dashes and the five-item flag reference,
because a pass that drove every count to zero would have corrupted a table, a
code comment, and a reference list. The trap asserts that all eleven of its hits
are the rejectable kind. CI runs on `ubuntu-latest` and `macos-latest`.

They exist because v2 shipped four broken patterns. They passed locally only
because the shell aliased `grep` to `ugrep`, which is permissive; on a clean
machine two errored and one silently matched nothing, which is the worse failure
because it looks like a clean pass. One was the curly-quote pattern, whose curly
quotes had been straightened by an editor into the ASCII ones it was meant to
detect.

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
