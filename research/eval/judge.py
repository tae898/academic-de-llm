#!/usr/bin/env python3
"""Stage 2: blind judging, two independent questions.

STYLE     which of two texts reads more machine-generated. Pairwise, position
          randomised, judges never told a skill exists.

FIDELITY  does the rewrite preserve the substance. This prompt separates
          SUBSTANTIVE loss from EVALUATIVE softening, and that split is the
          whole point of it.

          The first version of this eval asked judges to flag anything
          "dropped, altered or WEAKENED". They dutifully flagged the removal of
          `crucial`, `comprehensive`, `remarkable` and `outstanding`, which is
          precisely what the skill is for, and returned 22% faithful for the
          skill against 71% for the naive prompt. With the buckets separated the
          same data gives 91% against 94%. Do not merge them again.

    python3 research/eval/judge.py [--style] [--fidelity]
"""
import argparse, json, os, random, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import JUDGES, SEED, Incremental, call, load, manifest   # noqa: E402

STYLE_Q = """You are judging writing style. Below are two versions of the same scientific abstract.

Which one reads MORE as though it were generated or heavily edited by a large language model?
Consider: formulaic sentence openings, participial clauses that add vague interpretation,
generic emphasis on significance, synonym rotation for the same referent, hollow triplets,
and stock vocabulary used without doing work.

TEXT 1:
{t1}

TEXT 2:
{t2}

Answer with strict JSON only:
{{"more_machine_like": "1" or "2", "confidence": 1-5, "reason": "one sentence"}}"""

FIDELITY_Q = """Below is an ORIGINAL scientific abstract and a REWRITE of it.

You are checking FACTUAL fidelity only. Ignore style, tone and length.

Classify every difference into exactly one bucket.

SUBSTANTIVE loss or distortion (a real failure):
  a number, statistic or measurement is gone or changed
  a method, dataset, or experimental detail is gone
  a finding, result or conclusion is gone or reversed
  a stated limitation, scope condition or hedge is gone, so the rewrite now
    claims more than the original supported
  the rewrite asserts something the original does not support

EVALUATIVE change (NOT a failure, this is expected and desirable):
  a praise word or intensifier is removed or softened while the underlying
    fact survives, e.g. "remarkable 99% accuracy" -> "99% accuracy",
    "crucial for security" -> "counters spoofing",
    "comprehensive protocol" -> "defined protocol",
    "outstanding scores" -> "high scores"
  a promotional characterisation is dropped but the measurement remains

The test for SUBSTANTIVE: could a reader of the rewrite alone be misled about
what was done, what was found, or how strong the evidence is?

ORIGINAL:
{orig}

REWRITE:
{rw}

Strict JSON only:
{{"substantive_losses": ["..."], "substantive_additions": ["..."],
  "evaluative_only_changes": <integer count>,
  "substantively_faithful": true or false,
  "severity": "none"|"minor"|"major"}}"""


QUALITY_Q = """You are a careful copy editor. Below is an ORIGINAL passage and an EDITED version.

Ignore whether either sounds machine-written. Judge only whether the edit is an
improvement a professional editor would accept.

Consider: is it clearer? Does it read naturally, with varied rhythm rather than
uniform flat sentences? Was anything worth keeping thrown away, such as a useful
qualifier, a specific detail, or the author's voice? Is it now bland?

An edit that removes stock phrasing but leaves lifeless prose is NOT an
improvement. Say so if that is what happened.

ORIGINAL:
{orig}

EDITED:
{rw}

Strict JSON only:
{{"verdict": "better"|"same"|"worse", "flatter": true or false,
  "lost_something_worth_keeping": true or false, "why": "one sentence"}}"""


def parse(s):
    m = re.search(r'\{.*\}', s, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except Exception:                                # noqa: BLE001
        return None


def run_jobs(jobs, out):
    def work(job):
        job['raw'] = call(job['judge'], job.pop('prompt'), max_tokens=3000)
        job['parsed'] = parse(job['raw'])
        job['raw'] = job['raw'][:400]
        return job
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for n, f in enumerate(as_completed(futs), 1):
            out.append(f.result())
            if n % 50 == 0:
                print(f'  {n}/{len(jobs)}', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--style', action='store_true')
    ap.add_argument('--fidelity', action='store_true')
    ap.add_argument('--quality', action='store_true')
    a = ap.parse_args()
    if not (a.style or a.fidelity or a.quality):
        a.style = a.fidelity = a.quality = True

    rw = load('rewrites.json')
    rows = [r for r in rw['results']
            if not r['B'].startswith('__ERROR__') and not r['C'].startswith('__ERROR__')]
    corpus = rw['manifest']['corpus']
    random.seed(SEED)

    if a.style:
        jobs = []
        for r in rows:
            for pair, (x, y) in {'C_vs_B': (r['C'], r['B']),
                                 'C_vs_A': (r['C'], r['A']),
                                 'B_vs_A': (r['B'], r['A'])}.items():
                flip = random.random() < 0.5
                t1, t2 = (y, x) if flip else (x, y)
                for j in JUDGES:
                    jobs.append(dict(kind='style', i=r['i'], era=r['era'], pair=pair,
                                     judge=j, flip=flip, prompt=STYLE_Q.format(t1=t1, t2=t2)))
        print(f'style: {len(jobs)} calls', flush=True)
        run_jobs(jobs, Incremental('style.json', manifest(corpus, stage='judge-style')))

    if a.fidelity:
        jobs = []
        for r in rows:
            for arm in ('B', 'C'):
                for j in JUDGES:
                    jobs.append(dict(kind='fidelity', i=r['i'], era=r['era'], arm=arm,
                                     judge=j, prompt=FIDELITY_Q.format(orig=r['A'], rw=r[arm])))
        print(f'fidelity: {len(jobs)} calls', flush=True)
        run_jobs(jobs, Incremental('fidelity.json', manifest(corpus, stage='judge-fidelity')))

    if a.quality:
        # Style asks "does it read as machine-written". Fidelity asks "are the
        # facts intact". Neither asks whether the result is any GOOD, and a
        # de-slopped passage can pass both while being flat and lifeless.
        jobs = []
        for r in rows:
            for arm in ('B', 'C'):
                for j in JUDGES:
                    jobs.append(dict(kind='quality', i=r['i'], era=r['era'], arm=arm,
                                     judge=j, prompt=QUALITY_Q.format(orig=r['A'], rw=r[arm])))
        print(f'quality: {len(jobs)} calls', flush=True)
        run_jobs(jobs, Incremental('quality.json', manifest(corpus, stage='judge-quality')))

    print('next: python3 research/eval/analyse.py')


if __name__ == '__main__':
    main()
