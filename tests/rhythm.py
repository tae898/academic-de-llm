#!/usr/bin/env python3
"""Does the cleaned example keep the original's rhythm?

The skill's measured failure mode is flattening. Against a naive de-slop prompt
on the same texts it made the result flatter four times as often (20% against
5%) and produced edits judged outright worse 13% of the time where the naive
prompt produced none. Judges named the mechanism: splitting long sentences at
every participle until a paragraph is uniform short declaratives.

The worked example must not demonstrate the defect it warns about. It did:
before this check existed, prose-after.md had a standard deviation of 3.4
against the original's 8.4, and its longest sentence fell from 37 words to 18.

Exit 0 if the rhythm survives, 1 if it was flattened.
"""
import re, statistics, sys


def stats(path):
    text = open(path, encoding='utf-8').read()
    sents = [x for x in re.split(r'(?<=[.!?])\s+', text) if len(x.split()) > 2]
    lengths = [len(x.split()) for x in sents]
    openers = [x.split()[0].lower() for x in sents]
    repeats = sum(1 for i in range(1, len(openers)) if openers[i] == openers[i - 1])
    return statistics.pstdev(lengths), max(lengths), repeats


def main():
    b_sd, b_max, _ = stats('examples/prose-before.md')
    a_sd, a_max, a_rep = stats('examples/prose-after.md')
    problems = []
    if a_sd < b_sd * 0.7:
        problems.append(f'sentence-length variance fell to {a_sd:.1f} from {b_sd:.1f}')
    if a_max < b_max * 0.7:
        problems.append(f'longest sentence fell to {a_max} from {b_max}')
    if a_rep:
        problems.append(f'{a_rep} consecutive sentences share an opening word')
    if problems:
        print('flattened: ' + '; '.join(problems))
        return 1
    print(f'sd {a_sd:.1f}/{b_sd:.1f}, longest {a_max}/{b_max}, no repeated openers')
    return 0


if __name__ == '__main__':
    sys.exit(main())
