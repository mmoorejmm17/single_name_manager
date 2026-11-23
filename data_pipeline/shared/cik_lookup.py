"""CDS ticker -> SEC CIK. System Python (xlwings + running Excel with Bloomberg, same attach approach as bbg_bql.py).

For each CDS_Ticker in cds_mappings_final.csv it looks up CENTRAL_INDEX_KEY_NUMBER (BDP) on the entity's own equity ticker, the ultimate parent's and the public-equity entity's, and falls back to
the SEC's free company_tickers.json for US tickers Bloomberg leaves blank. Writes config/ticker_cik.csv (CIKs as 10-digit strings, leading zeros kept). Never edits the mappings workbook.

    python data_pipeline/shared/cik_lookup.py            # every name
    python data_pipeline/shared/cik_lookup.py OI MPW     # just these CDS tickers (test)
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from bbg_bql import MAPPINGS, _find_app          # noqa: E402

OUT = Path(__file__).resolve().parents[2] / 'config' / 'ticker_cik.csv'
SEC_URL = 'https://www.sec.gov/files/company_tickers.json'
BAD = ('', '--', 'NaN', 'nan', 'None')


def _clean(v):
    return v.strip() if isinstance(v, str) and v.strip() not in BAD else None


def _cik(v):
    """BDP cell value -> 10-digit CIK string, or None (#N/A etc.)."""
    if isinstance(v, (int, float)) and not pd.isna(v):
        return str(int(v)).zfill(10)
    if isinstance(v, str) and v.strip().isdigit():
        return v.strip().zfill(10)
    return None


def bdp_cik(tickers, timeout=180, log=print):
    """{equity ticker: CIK or None} through one scratch workbook of =BDP(ticker,"CENTRAL_INDEX_KEY_NUMBER")."""
    tickers = sorted(set(tickers))
    app = _find_app()
    log(f'attaching to Excel pid {app.pid}, {len(tickers)} tickers')
    wb = app.books.add()
    try:
        ws = wb.sheets[0]
        ws.range('A1').options(transpose=True).value = tickers
        for i in range(len(tickers)):
            ws.cells(1 + i, 2).formula = f'=BDP(A{1 + i},"CENTRAL_INDEX_KEY_NUMBER")'
        if app.api.Calculation != -4105:
            ws.api.Calculate()
        rng = ws.range((1, 2), (len(tickers), 2))
        t0 = time.time()
        while time.time() - t0 < timeout:
            time.sleep(2)
            if not any('Requesting' in (c.api.Text or '') for c in rng):
                break
        time.sleep(1)
        vals = [c.value for c in rng]
    finally:
        wb.api.Saved = True
        wb.close()
    return {t: _cik(v) for t, v in zip(tickers, vals)}


def sec_map():
    """{US ticker: CIK} from the SEC (generic User-Agent, nothing about the user)."""
    req = urllib.request.Request(SEC_URL, headers={'User-Agent': 'research-script contact-not-provided@example.com'})
    data = json.load(urllib.request.urlopen(req, timeout=30))
    return {r['ticker'].upper(): str(r['cik_str']).zfill(10) for r in data.values()}


def build(cds_tickers=None):
    m = pd.read_csv(MAPPINGS, dtype=str, encoding='cp1252').dropna(subset=['CDS_Ticker']).drop_duplicates('CDS_Ticker')
    if cds_tickers:
        m = m[m.CDS_Ticker.isin(cds_tickers)]
    rows = pd.DataFrame({
        'market_cds_ticker': m.CDS_Ticker,
        'company_name': m.Company_Name,
        'own_equity_ticker': m.BBG_Equity_Ticker.map(_clean),
        'parent_equity_ticker': m.Ultimate_Parent_Equity_Ticker.map(_clean),
        'public_equity_ticker': m.CDS_Public_Equity_Entity_Ticker.map(_clean),
    })
    eq = pd.unique(rows[['own_equity_ticker', 'parent_equity_ticker', 'public_equity_ticker']].values.ravel())
    bbg = bdp_cik([e for e in eq if isinstance(e, str) and e])
    sec = None
    for col in ('own', 'parent', 'public'):
        rows[f'{col}_cik'] = rows[f'{col}_equity_ticker'].map(bbg)
        rows[f'{col}_cik_source'] = rows[f'{col}_cik'].map(lambda v: 'bloomberg' if isinstance(v, str) else None)
        for i, r in rows[rows[f'{col}_cik'].isna() & rows[f'{col}_equity_ticker'].notna()].iterrows():
            t = r[f'{col}_equity_ticker']
            if t.endswith(' US Equity'):                      # only US tickers can be in the SEC file
                sec = sec or sec_map()
                c = sec.get(t.split()[0].upper())
                if c:
                    rows.loc[i, f'{col}_cik'], rows.loc[i, f'{col}_cik_source'] = c, 'sec_tickers'
    return rows


def keep_manual(df, path=OUT):
    """Hand-entered values survive a rerun: wherever the existing file has <col>_cik_source == 'manual' (own / parent / public), that CIK (and the 'manual' label) replaces the looked-up one.
    A manual row whose ticker is no longer in the mappings is appended unchanged. To pin a value, type the CIK (10 digits, as text) and 'manual' in its source column."""
    if not path.exists():
        return df
    old = pd.read_csv(path, dtype=str).dropna(subset=['market_cds_ticker']).set_index('market_cds_ticker')
    df = df.set_index('market_cds_ticker')
    n = 0
    for col in ('own', 'parent', 'public'):
        man = old[old[f'{col}_cik_source'] == 'manual'].index
        for t in man:
            if t in df.index:
                df.loc[t, f'{col}_cik'] = old.loc[t, f'{col}_cik']
                df.loc[t, f'{col}_cik_source'] = 'manual'
            else:
                df = pd.concat([df, old.loc[[t]]])
            n += 1
    print(f'kept {n} manual value(s) from the existing file')
    return df.reset_index().drop_duplicates('market_cds_ticker', keep='last')


if __name__ == '__main__':
    df = build(sys.argv[1:] or None)
    if len(sys.argv) > 1:
        pd.set_option('display.width', 250, 'display.max_columns', 30)
        print(df.to_string())
    else:
        OUT.parent.mkdir(exist_ok=True)
        df = keep_manual(df)
        df.to_csv(OUT, index=False)
        have = df[['own_cik', 'parent_cik', 'public_cik']].notna().any(axis=1)
        print(f'wrote {OUT}: {have.sum()} of {len(df)} names have a CIK; no CIK: {sorted(df.market_cds_ticker[~have].dropna().astype(str))[:40]} ...')
