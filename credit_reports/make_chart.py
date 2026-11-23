"""Make the CDS vs equity chart for a credit report, using Matt's timeseries_slideshow_tool (plot function unchanged, data from its daily cache).

    python credit_reports/make_chart.py OI            # 1y window -> credit_reports/charts/OI_cds_equity_1y.png
    python credit_reports/make_chart.py OI 2y

Reads (never writes) the tool's cache: cache/cds_equity_data_silver.parquet and cache/cds_equity_regression_results_gold.parquet. Those are refreshed by the tool's notebook
(`app/cds_equity_ts.ipynb`, one Databricks login a day); if the date printed below is old, run that notebook first. System Python with pandas + matplotlib.
"""
import os
import sys
from pathlib import Path

import pandas as pd

TOOL = Path('S:/Structured Credit/Matt Stuff/claude_repos/timeseries_slideshow_tool')
OUT = Path(__file__).resolve().parent / 'charts'
DPI = 150


def main(ticker, window='1y'):
    cwd = os.getcwd()
    os.chdir(TOOL)                                   # slideshow.config creates ./interesting_charts relative to the cwd: keep that inside the tool's own folder
    sys.path.insert(0, str(TOOL))
    try:
        import slideshow.plotting as plotting
        plotting.FIG_DPI = DPI                       # runtime override only: the tool's config.py (90 dpi) is untouched; higher dpi keeps a wider chart sharp
        from slideshow.plotting import plot_cds_equity_ts
        data = pd.read_parquet(TOOL / 'cache' / 'cds_equity_data_silver.parquet')
        reg = pd.read_parquet(TOOL / 'cache' / 'cds_equity_regression_results_gold.parquet')
        if ticker not in set(data['market_cds_ticker']):
            sys.exit(f'{ticker}: not in the tool cache (no CDS + equity pairing for it)')
        last = pd.to_datetime(data.loc[data['market_cds_ticker'] == ticker, 'published_date']).max().date()
        _, png = plot_cds_equity_ts(ticker, window, data, reg)
    finally:
        os.chdir(cwd)
    OUT.mkdir(exist_ok=True)
    path = OUT / f'{ticker}_cds_equity_{window}.png'
    path.write_bytes(png)
    print(f'wrote {path} (data through {last}; tool cache file dated {pd.Timestamp(os.path.getmtime(TOOL / "cache" / "cds_equity_data_silver.parquet"), unit="s").date()})')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '1y')
