#!/usr/bin/env python3
"""Stage 1: produce the three arms.

    A  the original text, untouched
    B  a naive prompt: "rewrite so it does not read as AI-generated"
    C  the same prompt with the full SKILL.md prepended

One rewriter model produces both B and C, so the skill is the only variable
between them. Without arm B the eval would only show that an LLM can edit,
which is not in question.

    python3 research/eval/rewrite.py [--n 12] [--control 4]
"""
import argparse, io, json, os, random, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REWRITER, SEED, Incremental, call, manifest   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.environ.get('DELLM_DATA', os.path.join(REPO, 'research', 'data'))
SKILL = io.open(os.path.join(REPO, 'skills', 'academic-de-llm', 'SKILL.md'), encoding='utf-8').read()

def prompts(unit):
    """Both arms, with the unit noun substituted.

    The noun matters: telling a model to rewrite "the following abstract" when
    it is holding a Related Work section invites it to compress the section
    into an abstract, which would read as a fidelity failure caused by the
    harness rather than by the skill.
    """
    tail = (f"Preserve every factual claim exactly. Do not add claims. Do not change "
            f"the findings. Output only the rewritten {unit}, no preamble."
            f"\n\n{unit.upper()}:\n")
    naive = f"Rewrite the following {unit} so that it does not read as AI-generated. " + tail
    skilled = SKILL + f"\n\n---\n\nApply the guidance above to the following {unit}. " + tail
    return naive, skilled

# Density scoring picks the abstracts with something to fix. Sampling at random
# would mostly select text the skill correctly leaves alone, which tests the
# skip pass rather than the rewrite.
DENSITY = [
    r'\b(across|additionally|comprehensive|crucial|enhancing|exhibited|insights|notably|particularly|within)\b',
    r'\b(serves as|stands as|functions as|boasts|offers|maintains)\b',
    r', (highlighting|underscoring|emphasizing|ensuring|reflecting|contributing to|allowing|enabling|focusing on)',
    r'not just .{0,40} but|not only .{0,40} but',
    r'plays a (crucial|pivotal|vital) role',
    r'\b(delv|showcas|underscor|pivotal|intricate|robust|seamless)\w*\b',
]


def score(t):
    return sum(len(re.findall(p, t, re.I)) for p in DENSITY) / max(len(t.split()), 1) * 1000


def pick(path, n, lo=140, hi=330):
    """Densest n documents in the word-count band.

    The band defaults to abstract length. A paper section runs longer, so the
    papers eval widens it: the unit an author actually polishes is a section,
    not an 8,000-word manuscript that no pairwise judge can read carefully.
    """
    if not os.path.exists(path):
        sys.exit(f'missing {path}\nrun: python3 research/fetch.py')
    rows = [(score(a), a) for a in io.open(path, encoding='utf-8').read().split('\n\n')
            if lo < len(a.split()) < hi]
    if not rows:
        sys.exit(f'{path}: no documents between {lo} and {hi} words')
    rows.sort(key=lambda r: (-r[0], r[1]))         # deterministic on ties
    return [a for _, a in rows[:n]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=12, help='per post-ChatGPT era')
    ap.add_argument('--pool', default='',
                    help='override the 2026 corpus with a larger pool file, for when '
                         'the default 12 gives too few real hits to say anything')
    ap.add_argument('--eras', default='2026,2024,pre-2022',
                    help='comma-separated. Narrow this rather than cutting n: the unit '
                         'of analysis is the document, so 15 documents is 15, not 45.')
    ap.add_argument('--arm', default='BC', choices=['BC', 'C'],
                    help="C reuses arm B from the previous run. Arm B's prompt has no "
                         "SKILL.md in it, so a change to the skill cannot alter it.")
    ap.add_argument('--control', type=int, default=4,
                    help='pre-2022 abstracts. These cannot be AI-generated, so '
                         'they bound what the style metric actually measures.')
    ap.add_argument('--control-pool', default='',
                    help='override the pre-2022 corpus, so the control comes '
                         'from the same register as the treatment')
    ap.add_argument('--words', default='140,330',
                    help='lo,hi word band. Abstract length by default; widen '
                         'for paper sections (e.g. 250,900)')
    ap.add_argument('--label', default='pubmed/sensors',
                    help='corpus name recorded in the manifest')
    ap.add_argument('--unit', default='abstract',
                    help="what the model is holding: 'abstract' or 'section'")
    a = ap.parse_args()
    random.seed(SEED)
    NAIVE, SKILLED = prompts(a.unit)

    # 2026 is the era that matters: it is what the skill will actually meet.
    # 2024 is kept because its slop profile is different and largely extinct
    # (`crucial` and `delve` are back at their pre-ChatGPT baselines by 2026),
    # so testing only on 2024 would measure the skill against a dead target.
    # pre-2022 cannot be AI-generated and bounds what the style metric means.
    pool2026 = a.pool or f'{DATA}/pubmed/y2026.txt'
    poolpre = a.control_pool or f'{DATA}/pubmed/ypre.txt'
    lo, hi = (int(x) for x in a.words.split(','))
    eras = [e.strip() for e in a.eras.split(',') if e.strip()]
    src = {'2026': (pool2026, a.n), '2024': (f'{DATA}/pubmed/y2024.txt', a.n),
           'pre-2022': (poolpre, a.control)}
    sample = [{'era': e, 'text': t} for e in eras for t in pick(*src[e], lo=lo, hi=hi)]

    corpus = f'{a.label} ' + ' + '.join(f'{e} n={src[e][1]}' for e in eras) + f' [{lo}-{hi}w]'
    out = Incremental('rewrites.json', manifest(corpus, stage='rewrite'))
    print(f'{len(sample)} {a.unit}s, rewriter={REWRITER}', flush=True)

    prevB = {}
    if a.arm == 'C':
        import glob as _g
        for f in sorted(_g.glob(os.path.join(os.path.dirname(out.path), 'archive-*', 'rewrites.json')) +
                        [os.path.join(os.path.dirname(out.path), 'rewrites-prev.json')]):
            if os.path.exists(f):
                for r in json.load(open(f))['results']:
                    prevB.setdefault(r['A'][:120], r['B'])
        print(f'  reusing {len(prevB)} arm-B rewrites', flush=True)

    def work(item):
        i, s = item
        b = prevB.get(s['text'][:120]) if a.arm == 'C' else None
        return i, s, b or call(REWRITER, NAIVE + s['text']), call(REWRITER, SKILLED + s['text'])

    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, s, b, c in ex.map(work, list(enumerate(sample))):
            out.append({'i': i, 'era': s['era'], 'A': s['text'], 'B': b, 'C': c})
            print(f'  {i}  {"ok" if not b.startswith("__ERROR__") and not c.startswith("__ERROR__") else "ERROR"}',
                  flush=True)
    print(f'wrote {out.path}\nnext: python3 research/eval/judge.py')


if __name__ == '__main__':
    main()
