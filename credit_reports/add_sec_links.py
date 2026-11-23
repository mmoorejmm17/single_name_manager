"""Add SEC links next to the local-file links in a credit report.

A report cites a filing with a relative link into financial_statements/companies/<t>/filings/ (works on the shared drive). This adds ' ([SEC](url))' after each such link, using the
download manifests (annual / earnings / quarterly _manifest.csv, and filings_manifest.csv). Idempotent: links that already have an SEC link are left alone; files with no manifest entry are listed.

    python credit_reports/add_sec_links.py credit_reports/OI.md
"""
import csv
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def url_map():
    m = {}
    for p in (ROOT / 'financial_statements' / 'companies').glob('*/filings/**/*manifest.csv'):
        with open(p, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                name = r.get('file') or r.get('local_file')
                if name and r.get('url'):
                    m[name] = r['url']
    return m


def main(md):
    urls = url_map()
    text = Path(md).read_text(encoding='utf-8')
    missing = set()
    pat = re.compile(r'\[([^\]]+)\]\(((?:\.\./)+financial_statements/companies/[^)\s][^)]*?)\)(?! \(\[SEC\])')

    def sub(m):
        label, target = m.group(1), m.group(2)
        name = unquote(target.rstrip('/').split('/')[-1])
        if target.endswith('/') or name not in urls:
            if not target.endswith('/'):
                missing.add(name)
            return m.group(0)
        return f'{m.group(0)} ([SEC]({urls[name].replace(" ", "%20")}))'

    new = pat.sub(sub, text)
    Path(md).write_text(new, encoding='utf-8', newline='')
    print(f'{md}: added {new.count("([SEC](") - text.count("([SEC](")} SEC link(s)')
    if missing:
        print('no manifest entry for:', *sorted(missing), sep='\n  ')


if __name__ == '__main__':
    main(sys.argv[1])
