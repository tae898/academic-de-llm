#!/usr/bin/env python3
"""Score a candidate regex against the data already collected. No API calls.

Recall comes from `recall.json`, the instances judges quoted when reading cold.
Precision comes from `labels.json`, the frozen adjudications.

Both files already exist, so trying a pattern variant is free. Use this before
spending anything on a fresh adjudication round.

    python3 research/eval/tune.py                # current vs candidate patterns
"""
import collections, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adjudicate import PATTERNS   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# Candidates built from the confirmed misses in recall.json.
#
# The single biggest recall killer was the comma prefix on the -ing triggers:
# "sensor signals enabling precise and robust detection" has no comma, so the
# pattern never saw it. Requiring the comma bought precision at a ruinous cost.
# The last candidate tried, kept so the next person does not repeat it.
#
# Round 2 dropped every weak trigger: recall 52% -> 46% to buy precision
# 35% -> 40%. Wrong trade here. An agent reads each hit, so a false positive
# costs a glance and a miss costs the fix entirely.
#
# Round 3 (below) dropped only the true zeros, `offer` 0/7 and `boasts` 0/2.
# Against the 701-label set that is 51% recall and 43% precision, against 52%
# and 42% for what is shipped. No meaningful gain, so it was not adopted.
#
# One finding worth keeping either way, visible in the per-trigger table:
# third person singular is the tell and the base form is an ordinary verb.
#   remains 87% vs remain 25%   provides 36% vs provide 11%   offers 35% vs offer 0%
# "the framework provides X" dresses up "is". "we provide X" does not.
CANDIDATE = {
    'copula avoidance':
        r'\b(serves? as|serving as|stands? as|functions? as|remains?|'
        r'provides?|offers|presents? a)\b',
    'superficial -ing':
        r'[, ](highlighting|underscoring|emphasizing|ensuring|reflecting|'
        r'contributing to|providing|enhancing|enabling|allowing|thereby \w+ing)\b',
    'undue emphasis':
        r'\bpivotal\b|\bis (crucial|essential|vital|critical)\b|'
        r'plays a (crucial|pivotal|vital) role|is a testament|'
        r'significant potential|highlighting the importance',
    'negative parallelism':
        r'not just .{0,60} but|not only .{0,60} but|'
        r'unlike .{0,80}?\b(this work|this study|we|our)\b',
}


def norm(s):
    return re.sub(r'\W+', ' ', (s or '').lower()).strip()


def confirmed_instances():
    """Spans at least two of three judges quoted independently.

    Each instance keeps the surrounding text as well as the quote. A judge
    quoting "sensor signals enabling precise detection" drops the leading comma,
    so testing a comma-anchored regex against the quote alone scores it zero when
    it would have matched the document. That would have overstated the
    improvement of any candidate that drops the comma.
    """
    d = json.load(open(os.path.join(HERE, 'out', 'recall.json')))['results']
    found = collections.defaultdict(lambda: collections.defaultdict(set))
    for r in d:
        if not r.get('parsed'):
            continue
        for pat, qs in (r['parsed'] or {}).items():
            if pat not in PATTERNS or not isinstance(qs, list):
                continue
            for q in qs:
                if isinstance(q, str) and len(q.split()) >= 3:
                    found[(r['i'], pat)][norm(q)].add(r['judge'])
    out = collections.defaultdict(list)
    for (i, pat), qs in found.items():
        for q, js in qs.items():
            allj = set(js)
            for q2, j2 in qs.items():
                if q2 != q and (q in q2 or q2 in q):
                    allj |= j2
            if len(allj) >= 2:
                out[pat].append((q, i))
    return out


def score(regexes, inst, labels, texts):
    rows = {}
    for pat, rx in regexes.items():
        caught = 0
        for q, i in inst.get(pat, []):
            if re.search(rx, q, re.I):
                caught += 1
                continue
            # fall back to the document: locate the quote and test its neighbourhood,
            # so a dropped comma in the quote does not count as a miss
            t = texts.get(i, '')
            nt = norm(t)
            pos = nt.find(q[:40])
            if pos >= 0 and re.search(rx, nt[max(0, pos - 3):pos + len(q) + 3], re.I):
                caught += 1
        total = len(inst.get(pat, []))
        kr = kf = 0
        for l in labels:
            if l['pattern'] != pat or l['arm'] != 'A':
                continue
            if re.search(rx, l['context'], re.I):
                if l['real']:
                    kr += 1
                else:
                    kf += 1
        rows[pat] = dict(recall=caught / total if total else 0, caught=caught, total=total,
                         precision=kr / (kr + kf) if (kr + kf) else 0, real=kr, surfaced=kr + kf)
    return rows


def main():
    inst = confirmed_instances()
    labels = json.load(open(os.path.join(HERE, 'labels.json')))['labels']
    texts = {r['i']: r['A'] for r in
             json.load(open(os.path.join(HERE, 'out', 'rewrites.json')))['results']}
    cur = score({k: v['regex'] for k, v in PATTERNS.items()}, inst, labels, texts)
    new = score(CANDIDATE, inst, labels, texts)

    print(f"{'pattern':<24}{'recall now':>13}{'recall new':>13}{'prec now':>11}{'prec new':>11}")
    print('-' * 74)
    for pat in PATTERNS:
        c, n = cur[pat], new[pat]
        print(f"{pat:<24}{c['caught']}/{c['total']} {c['recall']*100:>5.0f}%"
              f"{n['caught']}/{n['total']} {n['recall']*100:>5.0f}%"
              f"{c['precision']*100:>10.0f}%{n['precision']*100:>10.0f}%")
    tc = sum(v['caught'] for v in cur.values()); tt = sum(v['total'] for v in cur.values())
    nc = sum(v['caught'] for v in new.values())
    cr = sum(v['real'] for v in cur.values()); cs = sum(v['surfaced'] for v in cur.values())
    nr = sum(v['real'] for v in new.values()); ns = sum(v['surfaced'] for v in new.values())
    print('-' * 74)
    print(f"{'ALL':<24}{tc}/{tt} {tc/tt*100:>5.0f}%{nc}/{tt} {nc/tt*100:>5.0f}%"
          f"{cr/cs*100:>10.0f}%{nr/ns*100:>10.0f}%")
    print("\n  Precision here is measured only on hits that already have labels, so a")
    print("  candidate that surfaces genuinely new spans is not fully priced. Adjudicate")
    print("  the new hits before trusting the precision column.")


if __name__ == '__main__':
    main()
