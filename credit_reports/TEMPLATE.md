# Credit report: <TICKER> (<reference entity name>)

Copy this file to `credit_reports/<TICKER>.md` and fill it in. Keep THIS file generic: no credit-specific content. Matt's 9 C's framework (2026-11-23). C's 2-9 bullets are first drafts, to be amended by Matt.
Rules: each bullet gets an Answer and a Source (document, page / section); write "not found" rather than guessing; mark anything inferred as inferred. Do ownership / control first: it feeds Character.

## Header
- CDS ticker / index: <market_cds_ticker> / <index>      Markit ticker: <...>      RED code: <...>
- Reference entity (the CDS names this legal entity): <...>      Ultimate parent + CIK: <...>      Public / private: <...>
- Debt of the reference entity (deliverable): <ISIN, coupon, maturity, amount>   Debt of OTHER group entities (not deliverable): <...>
- Filings folder: financial_statements/companies/<ticker>/      Report date: <...>      Sources read: <...>

## 1. Character & Control
Character only matters if you control the decisions: find who controls first, then judge their character.
1. **Control**: special voting classes (votes per share by class), 5%+ holders and stakes, insider ownership, board independence and chair, whether any person or group can decide alone, legal-entity chain down to the reference entity (10-K Exhibit 21).
   - Answer:   - Source:
2. **Financial policy, as a bondholder sees it**: how aggressive are dividends and buybacks (amounts vs net income and free cash flow, and vs what the debt documents allow), and what management SAYS it wants for leverage (high, hold, reduce; targets, rating goals, M&A appetite, use of free cash flow). Targets are usually on earnings calls / decks, not in the 10-K.
   - Answer:   - Source:
3. **Strategic intent**: GROW (organic or M&A), HOLD, RESTRUCTURE / SHRINK, HARVEST cash, or RUN OFF. Drives bullet 2 and matters for CDS (growth / M&A can add debt before a credit event; run-off changes behaviour near default). Intent is what management WANTS; whether it CAN is Competition / Capacity / Contracts, so check they agree. Classify explicitly and quote the source.
   Answer it PER BUSINESS UNIT, and watch for anything "discontinued", held for sale, "legacy" or "non-core": a business that is discontinued or in run-off is a warning that it may be run for cash to fund a growth business, or sent into run-off or separated in a good-bank / bad-bank style split (legacy assets and liabilities in one vehicle, the franchise in another). No cash need leave the group for one class of creditors to lose out. Ask which creditor classes have a claim on the old business and which on the new, and whether management can redirect cash or assets between them (see Classes and Covenants bullet 1).
   - Answer:   - Source:
4. **Track record with creditors**: history of treating creditors vs shareholders (past refinancings, liability management / uptier or drop-down deals, litigation, restatements, legacy-liability handling, guidance credibility).
   - Answer:   - Source:

## 2. Capacity (ability to service the debt from cash flow)
1. Leverage and coverage: gross and net debt / EBITDA, interest cover, FCF / debt.
   - Answer:   - Source:
2. Cash-flow quality and direction: operating cash flow, capex, restructuring and one-offs, working capital, guidance vs delivery.
   - Answer:   - Source:
3. Liquidity and the maturity wall: cash, undrawn revolver, maturities by year vs refinancing ability, springing maturities.
   - Answer:   - Source:

## 3. Capital (the equity cushion beneath the debt)
1. Book equity (and tangible equity after goodwill) vs total debt.
   - Answer:   - Source:
2. Market cushion: equity market value and enterprise value vs debt (how far EV can fall before the bond is impaired).
   - Answer:   - Source:
3. Junior capital beneath the bond: preferred, subordinated or shareholder debt, and how much value must be lost before the bond takes a loss.
   - Answer:   - Source:

## 4. Collateral (what backs the bond and where it ranks)
1. What secures it, if anything: liens, the guarantor list, and who is NOT a guarantor.
   - Answer:   - Source:
2. Structural position: which entity issues; what debt and claims sit ahead at each entity (structural subordination).
   - Answer:   - Source:
3. Asset value behind the claim: asset base, disposal values, what a buyer would pay.
   - Answer:   - Source:
4. CDS deliverability: which bonds actually deliver into this reference entity (issuer = reference entity, or a guarantee by it of a downstream affiliate's debt). Check the ownership chain: a PARENT's or sister company's bonds do not deliver.
   - Answer:   - Source:

## 5. Covenants (protections in the documents; some authors use Conditions here: the economy / industry backdrop)
1. **LEAKAGE (biggest concern)**: can the company move value out of the creditor perimeter, chiefly through restricted payments (dividends, buybacks, affiliate / sponsor payments), investments in unrestricted subsidiaries, drop-downs of assets to non-guarantors (J.Crew-style), asset sales, or debt that primes or sits outside the perimeter? How much can leave (baskets, builder baskets, ratio tests)? Check Restricted Subsidiary, Unrestricted Subsidiary, Permitted Investments, guarantor-release terms.
   - Answer:   - Source:
2. Debt and lien limits: incurrence tests, lien covenant and exceptions, sale-leaseback limits.
   - Answer:   - Source:
3. Triggers: change-of-control put, cross-default / cross-acceleration thresholds, maintenance covenants, springing maturities, reporting requirements.
   - Answer:   - Source:
4. Who is bound: covenants at the issuer, at a parent, or at the guarantor group; what is in each debt class's own documents vs the bank facility.
   - Answer:   - Source:

## 6. Classes (creditor groups whose incentives are not fully aligned: secured / unsecured, 1L / 2L, FLFO / FLSO, holdco / opco; more classes means longer restructurings)
1. Map of every creditor class by entity and ranking, with amounts.
   - Answer:   - Source:
2. Intercreditor and voting terms: who controls decisions (majority lenders, amend-and-extend, cooperation agreements), cross-guarantees.
   - Answer:   - Source:
3. Non-debt claims competing for value: pensions, litigation / asbestos, leases, trade, tax.
   - Answer:   - Source:
4. Likely path in distress: negotiated restructuring vs a filing. For CDS: a failing company rarely lets a bond mature or pays it at par in distress (value leaving the enterprise from the senior holders' view), so a credit event is likelier to be negotiated.
   - Answer:   - Source:

## 7. Competition (competitive balance of the industry and strength of the moat; drives how durable Capacity is)
1. Industry structure: concentration, number and size of competitors, rational pricing vs price wars.
   - Answer:   - Source:
2. The company's position: market share, cost position, pricing power.
   - Answer:   - Source:
3. Threats: substitutes, new entrants, customer and supplier concentration.
   - Answer:   - Source:

## 8. Contracts (how contracted the revenue is: how much customers are legally obliged to pay)
High: REIT leases (tenants owe rent or are in default), take-or-pay, long-term power / infrastructure contracts. Low: consumer retailers and other discretionary-demand businesses. Feeds Capacity.
1. Share of revenue under contract and its remaining tenor (backlog, lease term, take-or-pay).
   - Answer:   - Source:
2. Counterparty quality, termination rights and cost pass-through (can customers walk, are input costs passed on).
   - Answer:   - Source:
3. What is NOT contracted: discretionary, consumer or spot exposure.
   - Answer:   - Source:

## 9. Correlation (how asset value moves with the company's performance and the cycle, in systemic and idiosyncratic selloffs)
Kept separate from Collateral (what the assets are and where the debt ranks) because it also carries cyclicality.
1. Business cyclicality: earnings sensitivity to the cycle (peak-to-trough EBITDA, past downturns).
   - Answer:   - Source:
2. Wrong-way risk: do the assets keep their value in the scenario where the company fails? (Healthcare REIT buildings probably do; for NVIDIA a failure would mean its products lost value; a failed theme-park operator means the parks did not do well.)
   - Answer:   - Source:
3. Recovery implication: a realistic recovery range vs the standard 40% assumption.
   - Answer:   - Source:

## Open items / next documents to read
-
