#!/usr/bin/env python3
"""Download the corpora behind sources 3, 4 and 5 in references/sources.md.

    python3 research/fetch.py

Writes to research/data/ (gitignored). No API keys. Public endpoints only,
with the polite delays both services ask for.
"""
import io, json, os, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('DELLM_DATA', os.path.join(HERE, 'data'))
EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
UA = {'User-Agent': 'de-llm-research/1.0 (https://github.com/tae898/de-llm)'}

# Sensors (Basel) is chosen because Kobak et al. measure it at one of the
# highest frequency gaps of any journal, so the effect is visible in a small
# sample. It is not representative of publishing, and sources.md says so.
JOURNAL = '"Sensors (Basel)"[jour]'
WINDOWS = {
    'ypre':  '(2019[dp] OR 2020[dp] OR 2021[dp])',   # pre-ChatGPT baseline
    'y2024': '2024[dp]',
    'y2025': '2025[dp]',
    'y2026': '2026[dp]',
}


def get(url, timeout=90):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def pubmed(tag, window, retmax=320):
    term = urllib.parse.quote(f'{JOURNAL} AND {window} AND hasabstract')
    ids = json.loads(get(f'{EUTILS}/esearch.fcgi?db=pubmed&retmax={retmax}'
                         f'&retmode=json&term={term}'))['esearchresult']['idlist']
    if not ids:
        print(f'  {tag}: no results'); return
    xml = get(f'{EUTILS}/efetch.fcgi?db=pubmed&id={",".join(ids)}&retmode=xml')
    root = ET.fromstring(xml)
    out = []
    for art in root.iter('PubmedArticle'):
        t = ' '.join(''.join(a.itertext()) for a in art.iter('AbstractText'))
        if len(t.split()) > 80:
            out.append(t)
    write(f'pubmed/{tag}.txt', out)
    # Prove the dash-normalisation claim rather than asserting it.
    raw = xml.decode('utf-8', 'replace')
    print(f'    U+2014 in raw XML: {raw.count(chr(0x2014))}   U+2013: {raw.count(chr(0x2013))}'
          '   <- why dashes are unmeasurable in PubMed')


def arxiv(tag, lo, hi, n=300):
    q = urllib.parse.urlencode({
        'search_query': f'cat:cs.LG AND submittedDate:[{lo} TO {hi}]',
        'max_results': n, 'sortBy': 'submittedDate'})
    root = ET.fromstring(get(f'https://export.arxiv.org/api/query?{q}'))
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    out = [e.find('a:summary', ns).text.strip() for e in root.findall('a:entry', ns)
           if e.find('a:summary', ns) is not None]
    write(f'arxiv/{tag}.txt', [x for x in out if len(x.split()) > 60])


def write(rel, items):
    p = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, 'w', encoding='utf-8').write('\n\n'.join(items))
    print(f'  {rel}: {len(items)} abstracts, {sum(len(x.split()) for x in items):,} words')


def main():
    print('PubMed, Sensors (Basel):')
    for tag, window in WINDOWS.items():
        pubmed(tag, window)
        time.sleep(1)          # NCBI asks for <=3 req/sec without a key
    print('\narXiv cs.LG:')
    arxiv('pre',   '202001010000', '202012310000')
    time.sleep(3)              # arXiv asks for one request per 3 seconds
    arxiv('y2026', '202601010000', '202607310000')
    print(f'\nwrote to {DATA}\nnow run: python3 research/measure.py')
    print('\nNote: the README corpus (source 3) is not fetched here. It is 35 repos'
          '\nfrom the Claude Code community marketplace and the set will have moved on.')


if __name__ == '__main__':
    main()
