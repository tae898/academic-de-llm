#!/usr/bin/env python3
"""Is rhythm an AI tell, and does de-slopping damage it?

    python3 research/rhythm.py

Two different questions that the folklore runs together.

  CORPUS   does published 2026 academic prose have a different rhythm from
           pre-ChatGPT prose in the same venue? If "AI writes uniform short
           sentences" is a detection signal, it shows up here.

  REWRITE  what happens to rhythm when a model is asked to de-slop a text?
           Needs research/eval/out*/rewrites.json, so it only runs after an
           eval. This is the damage measurement, not the detection one.

The answer is that the two disagree, which is why they are measured apart.
"""
import io, json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('DELLM_DATA', os.path.join(HERE, 'data'))

METRICS = ['mean sent len', 'sd of sent len', '% 15-30 words',
           'longest', 'shortest', 'commas/sent', '% same opener']


def sentences(doc):
    return [s for s in re.split(r'(?<=[.!?])\s+', doc) if len(s.split()) > 2]


def profile(texts):
    """Mean over documents of seven per-document rhythm statistics.

    Per document, not pooled, for the reason in sources.md source 4: one long
    document otherwise decides the answer.
    """
    acc = [[] for _ in METRICS]
    for d in texts:
        ss = sentences(d)
        if len(ss) < 4:
            continue
        ln = [len(s.split()) for s in ss]
        op = [s.split()[0].lower().strip('(,') for s in ss]
        vals = [statistics.mean(ln), statistics.pstdev(ln),
                sum(1 for x in ln if 15 <= x <= 30) / len(ln) * 100,
                max(ln), min(ln),
                statistics.mean(s.count(',') for s in ss),
                sum(1 for i in range(1, len(op)) if op[i] == op[i - 1]) / max(len(op) - 1, 1) * 100]
        for a, v in zip(acc, vals):
            a.append(v)
    return [statistics.mean(a) if a else 0.0 for a in acc]


def docs(path):
    if not os.path.exists(path):
        return []
    t = io.open(path, encoding='utf-8', errors='replace').read()
    return [d for d in t.split('\n\n') if len(d.split()) >= 80]


def table(title, cols, note=''):
    print(f'\n{title}')
    if note:
        print(note)
    print(f"\n{'metric':<18}" + ''.join(f'{n:>12}' for n, _ in cols))
    print('-' * (18 + 12 * len(cols)))
    profs = [profile(t) for _, t in cols]
    for i, m in enumerate(METRICS):
        print(f'{m:<18}' + ''.join(f'{p[i]:>12.1f}' for p in profs))


def main():
    table('CORPUS: same venue, before and after ChatGPT',
          [('pre-2022', docs(f'{DATA}/pubmed/ypre.txt')),
           ('2024', docs(f'{DATA}/pubmed/y2024.txt')),
           ('2026', docs(f'{DATA}/pubmed/y2026.txt'))],
          'Sensors abstracts. If uniform rhythm were a detection signal it would show here.')

    table('CORPUS: full papers',
          [('pre-2022', docs(f'{DATA}/papers/ypre.txt')),
           ('2026', docs(f'{DATA}/papers/y2026.txt'))])

    for tag, path in (('abstracts', 'out'), ('paper sections', 'out-papers')):
        p = os.path.join(HERE, 'eval', path, 'rewrites.json')
        if not os.path.exists(p):
            continue
        r = [x for x in json.load(open(p))['results'] if x['era'] == '2026']
        table(f'REWRITE: what de-slopping does to {tag} (n={len(r)})',
              [('original', [x['A'] for x in r]),
               ('naive', [x['B'] for x in r]),
               ('skill', [x['C'] for x in r])],
              'Arm B and C are raw model output, never edited by a human.')

    print('\nRead the two together. Published prose barely moved; a rewrite pass')
    print('halves the variance and the longest sentence. Flatness is what this')
    print('skill DOES, not what it should look for.')


if __name__ == '__main__':
    main()
