# Instructions for anyone who clones this repo

This repo analyses single-name CDS moves inside the CDX / iTraxx indices (spread, upfront, all_upfront, risky_pv01 changes between two dates, dispersion, top-N expected-loss share).
You only need to **use** the data. The data is built and published by one person (Matt Moore) and lives on the shared drive; it is not in GitHub.

## What you need
- Access to the shared drive `S:\Structured Credit\Matt Stuff\single_name_manager\` (the published data is in its `data\base\` folder, about 145 MB, read only for you).
- Python 3.12+ with `pandas`, `numpy`, `pyarrow`, `ipykernel` (plus Jupyter or VS Code to open notebooks). Nothing else: no Bloomberg, Databricks, Quantifi or Excel.

## Set up
```
git clone https://github.com/mmoorejmm17/single_name_manager.git
cd single_name_manager
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy pyarrow ipykernel
```
(To only read the data, the line above is enough. `poetry install` also works and adds the Bloomberg / Databricks packages needed to update the data, see "Updating the base data" below.)

## Use it
1. Open a notebook in `index_notebooks/` (or `singles_notebooks/`) and select the `.venv` kernel:
   - `index_spread_moves.ipynb`: pick an index (e.g. `HY47`) and two dates; shows which names are missing data, then every name's spread, upfront, all_upfront and risky_pv01 at both dates and the change, plus index metrics.
   - `dispersion.ipynb`: dispersion of all_upfront across an index over time.
   - `topN.ipynb`: share of the index's expected loss in the N widest names, two dates.
2. Change the parameters in the notebook's parameter cell (INDEX, dates, N ...) and Run All.
3. The first cell prints which snapshot you are reading, in the form `data published <date time>; prices through <date>`. Check that the "prices through" date is as recent as you expect.

## Where the data is read from
The data lives in a "store": a folder with `prices\`, `reference\`, `metrics\` and a `MANIFEST.json`. Today there is one store, `base`. The code looks, in order, at: the `CDS_DATA_DIR`
environment variable (a store folder); this clone's own `data\base\` folder (if it has a `MANIFEST.json`); then the shared-drive store
`S:\Structured Credit\Matt Stuff\single_name_manager\data\base`. A fresh clone has no `data\`, so it reads the shared drive automatically. If the drive is mapped to a different letter, or you want a
local copy, copy that `data\base` folder into the clone as `data\base`, or set `CDS_DATA_DIR` to the `base` folder. Never edit files in `data\`.

## Ground rules
- `analysis/` only reads data. It never writes, so you cannot damage the data store by running notebooks.
- `data_pipeline/` builds and publishes the data (Bloomberg, Databricks, Quantifi, Excel add-in). Please check with the owner before running it, since the owner is still fixing old missing data.

## Updating the base data (only if you have the logins)
The daily update is two steps, run with the system Python (it needs Quantifi and Excel): `python data_pipeline/daily/update.py`, then `python data_pipeline/shared/publish.py`.
**It might fail if you are not logged in.** Before running, make sure you are logged in to Bloomberg (terminal open and signed in), Databricks (`databricks auth login --profile <your profile>`),
and the Markit add-in in Excel (IHS Markit ribbon > Login). Without Bloomberg the Bloomberg steps fail; without Excel / Markit the add-in step is skipped with a message (or use `--no-addin`).
Publishing overwrites `data\base` for everyone (the previous version is kept in `data\_previous`; `publish.py --restore` undoes it).
- The data can change when the owner re-publishes. If numbers shift, compare the "data published" line at the top of the notebook.
- Missing / approximated data is flagged in the notebook (red = no price, amber = wide name at a marked-down recovery, blue = re-priced from the other coupon, purple = Markit add-in).
  `CLAUDE.md` has the definitions (what "priced" means, how all_upfront, dispersion and top-N are computed).

## Folders
`analysis/` code that reads data, `index_notebooks/` and `singles_notebooks/` the notebooks, `data/base/` the published data store (not in git), `data_pipeline/` owner-only code, `config/` hand-maintained inputs, `docs/` Markit user guide.
