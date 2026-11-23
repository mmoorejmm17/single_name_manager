#!/usr/bin/env python3
"""
download_annual_reports.py - download a company's last N annual reports (10-K, or 20-F / 40-F) from SEC EDGAR, with the subsidiary list (Exhibit 21) and guarantor list (Exhibit 22).

Usage (run it yourself; the SEC needs a contact in the User-Agent, set via --user-agent or the SEC_USER_AGENT environment variable):
    python download_annual_reports.py 812074 oi --user-agent "Your Name your.email@firm.com"
    python download_annual_reports.py 812074 oi --years 4 --forms 10-K

Takes the CIK (see config/ticker_cik.csv) and a folder name. Uses the EDGAR submissions API (data.sec.gov), so it finds every 10-K regardless of what it says about credit agreements
(download_filings.py only keeps filings that match credit-agreement phrases, which is why it returned just 8-K exhibits).
Output: companies/<name>/filings/annual/<name>_<period>_<form>_<doc>, plus annual_manifest.csv. Existing files are skipped. Waits ~0.2s between requests (SEC limit is 10/s).
"""
import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
ANNUAL_FORMS = ('10-K', '20-F', '40-F')


def get(url, ua):
    time.sleep(0.2)
    return urlopen(Request(url, headers={'User-Agent': ua}), timeout=60).read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cik')
    ap.add_argument('name', help='folder under companies/, e.g. oi')
    ap.add_argument('--years', type=int, default=3)
    ap.add_argument('--forms', default=None, help='default: 10-K,20-F,40-F; with --items the default is 8-K')
    ap.add_argument('--items', help='only filings reporting this 8-K item, e.g. 2.02 (earnings releases); also fetches their Exhibit 99 (press release / slides)')
    ap.add_argument('--subdir', default='annual', help='folder under filings/ (use "earnings" with --items 2.02)')
    ap.add_argument('--user-agent', default=os.environ.get('SEC_USER_AGENT'))
    a = ap.parse_args()
    if not a.user_agent:
        sys.exit('SEC needs a contact: pass --user-agent "Name email" or set SEC_USER_AGENT')
    cik = str(int(a.cik)).zfill(10)
    forms = tuple(f.strip() for f in (a.forms or ('8-K' if a.items else ','.join(ANNUAL_FORMS))).split(','))
    sub = json.loads(get(f'https://data.sec.gov/submissions/CIK{cik}.json', a.user_agent))
    r = sub['filings']['recent']
    rows = [dict(zip(r, v)) for v in zip(*r.values())]
    rows = [x for x in rows if x['form'] in forms]
    if a.items:
        rows = [x for x in rows if a.items in [i.strip() for i in x.get('items', '').split(',')]]
    for x in rows:                                   # proxy statements (DEF 14A) have no reportDate: fall back to the filing date
        x['reportDate'] = x['reportDate'] or x['filingDate']
    rows.sort(key=lambda x: x['reportDate'], reverse=True)
    rows = rows[:a.years]
    out = HERE / 'companies' / a.name / 'filings' / a.subdir
    ex_pat = r'(ex|exhibit)[-_]?(21|22|99)' if a.items else r'(ex|exhibit)[-_]?(21|22)'
    out.mkdir(parents=True, exist_ok=True)
    manifest = []
    print(f"{sub['name']} (CIK {cik}): {len(rows)} annual report(s)")
    for x in rows:
        acc = x['accessionNumber'].replace('-', '')
        base = f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/'
        wanted = [(x['primaryDocument'], 'main')]
        try:
            idx = json.loads(get(base + 'index.json', a.user_agent))
            for it in idx['directory']['item']:
                n = it['name']
                if re.search(ex_pat, n, re.I) and n.lower().endswith(('.htm', '.html', '.txt')):
                    wanted.append((n, 'exhibit'))
        except Exception as e:
            print(f'  index failed for {acc}: {e}')
        for fn, kind in wanted:
            dest = out / f"{a.name}_{x['reportDate']}_{x['form']}_{fn}"
            if not dest.exists():
                dest.write_bytes(get(base + fn, a.user_agent))
                print(f'  downloaded {dest.name}')
            manifest.append(dict(period=x['reportDate'], filed=x['filingDate'], form=x['form'], kind=kind, file=dest.name, url=base + fn))
    if manifest:
        with open(out / f'{a.subdir}_manifest.csv', 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(manifest[0]))
            w.writeheader()
            w.writerows(manifest)
    print(f'Done. {len(manifest)} files in {out}')


if __name__ == '__main__':
    main()
