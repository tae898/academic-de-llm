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
import argparse, hashlib, json, os, random, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import JUDGES, OUT, SEED, Incremental, call, load, manifest   # noqa: E402

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


def sig(*texts):
    """Short content hash of everything a judgement depends on.

    The resume key used to be (i, arm, judge). That is the document INDEX, so
    re-running arm C against a changed SKILL.md reused every old judgement and
    reported 0 calls remaining: the numbers would have described the previous
    skill while claiming to describe the new one. Keying on content means a
    changed arm invalidates exactly the judgements that saw it, and leaves the
    unchanged A-vs-B pairs cached, which is where the saving actually is.
    """
    h = hashlib.sha256()
    for t in texts:
        h.update(t.encode('utf-8', 'replace')); h.update(b'\x00')
    return h.hexdigest()[:12]


def resume(name, jobs, keyfn):
    """Drop jobs already answered successfully, and carry the old results over.

    judge.py had no resume, so any interruption cost the whole stage. It has now
    been interrupted by an exhausted account, a SIGTERM from an over-long wait,
    and a `| head -3` that SIGPIPEd the process after three lines of output.
    Only SUCCESSFUL calls count as done, or a transient failure becomes
    permanent.

    A carried-over result must also ANSWER one of the jobs about to run. It is
    not enough to drop the job: an old result whose key no longer matches
    anything is a judgement of text that is no longer in the run, and keeping
    it alongside the fresh one leaves the file holding two verdicts per
    (document, judge) from two different versions of the skill. analyse.py
    would average them and report a blend of both.
    """
    import os as _os
    p = _os.path.join(OUT, name)
    if not _os.path.exists(p):
        return jobs, []
    allprev = json.load(open(p))['results']
    wanted = {keyfn(j) for j in jobs}
    prev = [r for r in allprev if r.get('parsed') and keyfn(r) in wanted]
    stale = sum(1 for r in allprev if r.get('parsed') and keyfn(r) not in wanted)
    if stale:
        print(f'  dropping {stale} results that answer no current job', flush=True)
    failed = len(allprev) - len(prev) - stale
    if failed:
        print(f'  retrying {failed} failed calls', flush=True)
    done = {keyfn(r) for r in prev}
    return [j for j in jobs if keyfn(j) not in done], prev


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
                                     judge=j, flip=flip, sig=sig(t1, t2),
                                     prompt=STYLE_Q.format(t1=t1, t2=t2)))
        jobs, prev = resume('style.json', jobs,
                            lambda r: (r['i'], r['pair'], r['judge'], r.get('sig')))
        print(f'style: {len(jobs)} calls remaining ({len(prev)} done)', flush=True)
        out = Incremental('style.json', manifest(corpus, stage='judge-style'))
        out.data['results'].extend(prev); out.flush()
        run_jobs(jobs, out)

    if a.fidelity:
        jobs = []
        for r in rows:
            for arm in ('B', 'C'):
                for j in JUDGES:
                    jobs.append(dict(kind='fidelity', i=r['i'], era=r['era'], arm=arm,
                                     judge=j, sig=sig(r['A'], r[arm]),
                                     prompt=FIDELITY_Q.format(orig=r['A'], rw=r[arm])))
        jobs, prev = resume('fidelity.json', jobs,
                            lambda r: (r['i'], r['arm'], r['judge'], r.get('sig')))
        print(f'fidelity: {len(jobs)} calls remaining ({len(prev)} done)', flush=True)
        out = Incremental('fidelity.json', manifest(corpus, stage='judge-fidelity'))
        out.data['results'].extend(prev); out.flush()
        run_jobs(jobs, out)

    if a.quality:
        # Style asks "does it read as machine-written". Fidelity asks "are the
        # facts intact". Neither asks whether the result is any GOOD, and a
        # de-slopped passage can pass both while being flat and lifeless.
        jobs = []
        for r in rows:
            for arm in ('B', 'C'):
                for j in JUDGES:
                    jobs.append(dict(kind='quality', i=r['i'], era=r['era'], arm=arm,
                                     judge=j, sig=sig(r['A'], r[arm]),
                                     prompt=QUALITY_Q.format(orig=r['A'], rw=r[arm])))
        jobs, prev = resume('quality.json', jobs,
                            lambda r: (r['i'], r['arm'], r['judge'], r.get('sig')))
        print(f'quality: {len(jobs)} calls remaining ({len(prev)} done)', flush=True)
        out = Incremental('quality.json', manifest(corpus, stage='judge-quality'))
        out.data['results'].extend(prev); out.flush()
        run_jobs(jobs, out)

    print('next: python3 research/eval/analyse.py')


if __name__ == '__main__':
    main()
