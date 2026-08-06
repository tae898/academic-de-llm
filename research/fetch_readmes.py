#!/usr/bin/env python3
"""Paired README corpus: the same repositories before and after ChatGPT.

The README register is the one this skill leads with, and the only one measured
without a baseline. `SKILL.md` claims em dashes run at 122 per 10k words in
agent-written READMEs and that formatting beats everything else by ten to fifty
times. Both are prevalence figures. Neither says whether 122 is unusual.

This is a stronger design than the PubMed one. Rather than comparing different
documents from two eras, it takes the SAME repository twice: its README as it
stood at the last commit before 2022, and its README today. Project, author,
domain and house style are held constant, so what is left is drift in how the
text is written.

Repositories qualify only if the README was touched again after 2023, otherwise
the "after" sample is just the old text again.

    python3 research/fetch_readmes.py [--n 200]

Needs the `gh` CLI authenticated. No OpenRouter credits.
"""
import argparse, base64, io, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('DELLM_DATA', os.path.join(HERE, 'data'))
CUTOFF = '2022-01-01T00:00:00Z'      # ChatGPT shipped 2022-11; this is generous
# Requiring a language excludes awesome-lists and curated link collections.
# Those top the star rankings and are 90% URLs, so they would swamp a prose
# measurement with markup.
LANGS = ['python', 'go', 'rust', 'typescript', 'java', 'ruby']


def gh(path, jq=None):
    cmd = ['gh', 'api', path]
    if jq:
        cmd += ['--jq', jq]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:                                # noqa: BLE001
        return None


def readme_at(repo, sha):
    c = gh(f'repos/{repo}/contents/README.md?ref={sha}', '.content')
    if not c:
        return None
    try:
        return base64.b64decode(c).decode('utf-8', 'replace')
    except Exception:                                # noqa: BLE001
        return None


def candidates(n):
    """Repos that existed well before ChatGPT and are still maintained."""
    out, page = [], 1
    while len(out) < n * 4 and page <= 24:
        q = ('search/repositories?q=' +
             'created:2015-01-01..2020-12-31+pushed:>2026-01-01+stars:100..8000' +
             f'+language:{LANGS[page % len(LANGS)]}' +
             f'&sort=stars&order=desc&per_page=100&page={1 + page // len(LANGS)}')
        j = gh(q, '.items[].full_name')
        if not j:
            break
        out += [x for x in j.split('\n') if x]
        page += 1
        time.sleep(0.5)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=200)
    a = ap.parse_args()

    repos = candidates(a.n)
    print(f'{len(repos)} candidate repos', flush=True)
    before, after, used = [], [], []

    for r in repos:
        if len(used) >= a.n:
            break
        old_sha = gh(f'repos/{r}/commits?path=README.md&until={CUTOFF}&per_page=1', '.[0].sha')
        new = gh(f'repos/{r}/commits?path=README.md&per_page=1', '.[0].sha // ""')
        new_date = gh(f'repos/{r}/commits?path=README.md&per_page=1', '.[0].commit.committer.date // ""')
        if not old_sha or not new or old_sha == new:
            continue
        # The "after" sample must actually be post-ChatGPT text, not the old
        # file still sitting there untouched.
        if not new_date or new_date < '2023-01-01':
            continue
        b, af = readme_at(r, old_sha), readme_at(r, new)
        if not b or not af or len(b.split()) < 150 or len(af.split()) < 150:
            continue
        # Skip link collections that slipped through: a README that is mostly
        # URLs measures markup, not writing.
        if any(d.count('](http') / max(len(d.split()), 1) > 0.02 for d in (b, af)):
            continue
        before.append(b)
        after.append(af)
        used.append(r)
        if len(used) % 10 == 0:
            print(f'  {len(used)} paired', flush=True)

    os.makedirs(f'{DATA}/readmes_paired', exist_ok=True)
    for tag, docs in (('before', before), ('after', after)):
        p = f'{DATA}/readmes_paired/{tag}.txt'
        io.open(p, 'w', encoding='utf-8').write('\n\n<<<DOC>>>\n\n'.join(docs))
        print(f'  {tag}: {len(docs)} READMEs, {sum(len(d.split()) for d in docs):,} words')
    json.dump(used, open(f'{DATA}/readmes_paired/repos.json', 'w'), indent=1)
    print(f'\nwrote {DATA}/readmes_paired/  ({len(used)} repos, same repo both sides)')


if __name__ == '__main__':
    main()
