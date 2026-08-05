# Research

Reproduces every measured number in `skills/de-llm/references/sources.md`.

```bash
python3 research/fetch.py     # public endpoints, no API key
python3 research/measure.py   # prints the tables
```

The skill asks readers to check its claims. This is how.

## What is measured where, and why it takes two corpora

| Corpus | Gives | Cannot give |
|---|---|---|
| PubMed, *Sensors* (Basel), 4 windows 2019 to 2026, 251k words | vocabulary and structural tells, before and after ChatGPT in one journal | anything about dashes |
| arXiv `cs.LG`, 2020 vs 2026, 111k words | dash use, via preserved LaTeX markup | it is a different field and venue |
| 35 plugin READMEs, 51k words | formatting tells in agent-written Markdown | no baseline, so prevalence only |

**PubMed normalises every dash to an ASCII hyphen.** The raw XML holds zero
U+2014 and zero U+2013 in all four windows, including the pre-2022 one.
`fetch.py` prints those counts so you can see it rather than take our word.

An earlier version of this skill reported that zero as a finding and concluded
that formatting tells only occur in documents with markup. That was wrong, and
the arXiv numbers are the correction: em dash use roughly doubled in academic
prose between 2020 and 2026.

## What these numbers are not

None of them is a counterfactual projection. Kobak et al. project an expected
2024 frequency from 2021 to 2022 data and measure the gap, which is what lets
them say "excess". These are raw before-and-after comparisons in a fixed venue,
so they cannot separate an LLM effect from drift in topics, authorship, or
editorial policy over the same years.

*Sensors* in particular was chosen **because** the effect is large there. Kobak
measure it near the top of every journal they report. It is not representative.

And over this window MDPI introduced AI screening, so "models stopped producing
the tell" and "editors removed it" are indistinguishable in the decay table.

## Sample size

Each PubMed window is roughly 300 abstracts against Kobak's 15.1 million. Treat
the direction as informative and any single figure as noisy.
