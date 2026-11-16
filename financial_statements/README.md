# financial_statements/

## Goal (stated by Matt, 2026-11-06; top priority)
For ANY credit in our universe (single names in the CDS indices, plus their bond / loan issuers), be able to find and retrieve ALL of its public documents:
- annual reports
- quarterly / interim reports
- bond indentures (and offering memoranda / prospectuses)
- credit agreements
- intercreditor agreements

We are not there yet. This folder is where the work will live; this note records the intent so we keep moving toward it.

## What is already here
The old `credit_analysis/` folder was merged into this one (2026-11-06), so retrieval and analysis of a name's documents live together:
- `download_filings.py`: pulls SEC EDGAR credit agreements and indentures for US filers into `companies/<ticker>/filings/` (stdlib only, self-contained). EDGAR is the easy half; the goal is to generalise this to every name, including Europe.
- `SKILL.md`: the credit-analysis skill instructions.
- `companies/<ticker>/`: per-name notes (`<ticker>_credit_terms.md`, `<ticker>_fcf.md`, tracked in git) next to the downloaded `filings/` (gitignored). Only `xrx` so far.

## Sources by region (starting list, from general knowledge, NOT yet tested; verify before relying)
**US (SEC filers):** EDGAR has everything: 10-K / 10-Q / 8-K, and credit agreements / indentures / intercreditor agreements as exhibits (EX-4, EX-10). 144A-only issuers with no SEC registration are the gap (see Private issuers).

**Europe, no single free source yet:**
- ESMA European Single Access Point (ESAP): the intended central EU location (Transparency Directive reports, prospectuses, ESEF). Rolling out in phases from 2026, so coverage is probably thin today; check what is live.
- filings.xbrl.org (XBRL International): free index and API of ESEF (iXBRL) annual reports for listed EU/UK issuers.
- National OAMs (officially appointed mechanisms) for regulated information: UK FCA National Storage Mechanism, Germany Unternehmensregister / Bundesanzeiger, France AMF (BALO / info-financiere), Netherlands AFM, Luxembourg LuxSE, Nordics via Nasdaq / national registers.
- Company registries for statutory accounts (also covers many private companies): UK Companies House (free API), France Infogreffe / data.gouv, Luxembourg RCS, German Handelsregister.
- Bond listing venues (offering memoranda, indentures' summaries, sometimes the indenture): LuxSE (Euro MTF), Euronext Dublin (Global Exchange Market), The International Stock Exchange.
- Issuer investor-relations pages: most HY issuers post quarterly reports there because the indenture requires it. Often the only source for quarterlies.

**Private issuers / 144A-Reg S (most European HY):** quarterlies are usually on the IR site or a password-protected data room (needs a login we may not have). Credit agreements and intercreditor agreements are rarely public in Europe; at best the offering memorandum describes them (the "Description of Other Indebtedness" and "Intercreditor Agreement" sections). Expect some documents to be unobtainable.

## Open questions / next steps
1. Per name: record issuer legal entity, domicile, listing venue, SEC-registered or not (a mapping table, likely `config/` driven, keyed on market_cds_ticker).
2. Test what ESAP and filings.xbrl.org really return today.
3. Decide storage layout, e.g. `financial_statements/{ticker}/{annual|quarterly|indenture|credit_agreement|intercreditor}/` with a manifest of source URL, filing date and retrieval date. Downloaded files are gitignored (like `companies/*/filings/` today); the layout should be reconciled with the existing `companies/<ticker>/` folders.
4. Build coverage reporting: which names have which document types, which are missing.
