# Review checklist

Run every three to six months. The whole repo assumes its own numbers rot, and
this is the procedure that catches it.

Evidence that the assumption is correct: between 2024 and 2026, in one journal,
`crucial` fell 85% and `delve` effectively vanished, both back to their
pre-ChatGPT baselines. Over the same window the structural tells held. A skill
built on the 2024 word list would now be detecting a target that no longer
exists.

## 1. Re-read the community source

Open [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
and diff its pattern taxonomy against `references/sources.md` section 2, item by
item. Add new categories. Remove ones it has dropped.

Two errors in the 2026-08 revision came from skipping this: patterns were
attributed to that page without checking (`false ranges` is not on it), and the
per-vendor artifact list was assumed current when new models had shipped.

## 2. Check the published research

- [arXiv:2406.07016](https://arxiv.org/abs/2406.07016) for a version bump.
  Figures changed materially between v1 and v5, and `sources.md` carried the v1
  numbers for two years.
- Search for newer work measuring excess vocabulary or structural tells,
  especially anything covering a register other than biomedical abstracts.
- `references/sources.md` section 6 lists papers consulted and not used. Recheck
  whether any now has extractable numbers.

## 3. Re-measure the corpora

```bash
make review
```

Re-fetches PubMed and arXiv, re-measures, and diffs against
`research/baseline.json`. Anything that moved more than about 30% is worth
acting on.

**Add the current year as a new window** in `research/fetch.py` (`WINDOWS`).
The point is the trend, and a trend needs the latest point.

## 4. Re-run the eval, on current text and current models

Two independent staleness traps, both hit in the 2026-08 revision.

**Corpus recency.** Sample the most recent year available, not whatever was
sampled last time. Testing on 2024 abstracts measures the skill against a slop
profile that is largely extinct. `rewrite.py` samples 2026, 2024 and pre-2022
precisely so the comparison is visible.

**Model recency.** Sort OpenRouter's model list by creation date and read the
top:

```bash
curl -s https://openrouter.ai/api/v1/models -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  | python3 -c "import json,sys,time; [print(time.strftime('%Y-%m-%d',time.gmtime(m.get('created',0))), m['id']) for m in sorted(json.load(sys.stdin)['data'], key=lambda x:-x.get('created',0))[:30]]"
```

Do **not** search for model names you already know. That returns whatever is
still listed, which is how two of three judges ended up a generation stale. Then
apply the rules in `MODELS.md` and update the panel.

```bash
make eval           # costs OpenRouter credits, never runs in CI
```

Keep the previous run under `research/eval/out/archive-<date>-<rewriter>/`.
Comparing across generations is the only direct evidence about whether a finding
survives, which is the question the repo exists to keep asking.

## 5. Update the skill

- Reorder tiers if the ranking changed. The ordering is a measurement, not a
  preference.
- Move a decayed pattern down; note the decay rather than deleting it, so the
  next reviewer can see the trend.
- Refresh the register table in `SKILL.md`.
- Bump `version` and `last_reviewed` in `skills/de-llm/SKILL.md`, and mirror the
  version in `.claude-plugin/plugin.json`.
- Update `research/baseline.json` to the new numbers, with the new date.
- Record what changed and why in `references/sources.md`, including corrections.
  Retractions stay visible; they are the most useful part of the file.

## 6. Verify

```bash
make test           # every pattern assertion, both directions
make measure        # must reproduce every number in sources.md
```

Then confirm the skill stayed tool-agnostic:

```bash
grep -riE 'ripgrep|grep|bash|shell|linux|macos|windows|install' skills/
```

This must return nothing. The skill is prose that names no tool and no operating
system, which is why it works anywhere. `tests/` and CI are Linux and macOS; the
skill itself has no platform.
