# binnacle

**LDI duration-matching — immunize the funded ratio (match, don't beat).**

A binnacle is the housing that keeps the compass steady on a pitching ship. The liability-driven
mandate isn't return — it's keeping **assets tracking liabilities** so the funded ratio doesn't lurch.
A pension/insurer liability ≈ a long-duration bond (its present value swings with rates); immunize by
matching asset duration to the liability, and the surplus barely moves whatever rates do. The
stabilizer for the liability-driven capstone. Alpaca SIP daily; liability proxy = `TLT` (long duration).

## Verdict

**VALIDATION — it immunizes exactly as theory predicts; it is risk *elimination*, not a return edge.**
Surplus (funded-ratio) volatility falls monotonically as asset duration approaches the liability's, and
the whole job is stopping the funded ratio from lurching with rates — at the cost of giving up the rate
bet in *both* directions.

| asset book | surplus vol | surplus ret | funded-ratio maxDD |
|---|---|---|---|
| **TLT (duration-matched)** | **~0.0%** | ~0.0% | **0%** |
| EDV (over-hedged ~24y) | +5.9% | −0.9% | −26% |
| IEF (under-hedged 7-10y) | +9.2% | +1.1% | −21% |
| AGG (core bonds) | +10.8% | +1.8% | −27% |
| hybrid 40 SPY / 60 TLT | +9.8% | +6.2% | −21% |
| 60/40 (SPY/IEF) | +17.4% | +9.7% | −37% |
| 100% equity (SPY) | +24.5% | +15.4% | −48% |

- **To match a long liability you must hold long duration.** Core bonds (`AGG`, surplus vol +10.8%) and
  "under-hedged" intermediate bonds (`IEF`, +9.2%) leave large funded-ratio risk; equity leaves enormous
  risk (+24.5%, −48% funded-ratio drawdown). Only long duration tracks a long liability.
- **The hybrid is the usable compromise:** 40 SPY / 60 TLT keeps surplus vol near the under-hedged bond
  books (+9.8%) while adding +6.2%/yr of surplus return — the growth-plus-overlay shape a real plan runs.

## 2022 — the rate bet, exposed

Rates rose, so the liability (`TLT`) fell **−31%** — liabilities *shrank*, which helps a plan *if* assets
held up:

| asset book | 2022 assets | → funded ratio |
|---|---|---|
| AGG (core bonds) | −13% | **+26.5%** |
| IEF (under-hedged) | −15% | +23.4% |
| 100% equity (SPY) | −18% | +19.0% |
| **TLT (matched)** | −31% | **0.0%** |
| EDV (over-hedged) | −39% | −11.5% |

Under-hedged books *gained* funded ratio in 2022 because assets fell less than liabilities — but that is
a **rate bet that only pays when rates rise.** In a falling-rate year the same under-hedge craters the
funded ratio. The matched book is flat either way: **LDI is the decision to stop betting on rates.**

## Honest note, and `binnacle_2`

Liability and matched-asset are both `TLT`, so the 0.0%-vol match is tautological by construction — it's
the *reference point* for perfect immunization. The informative results are the **mismatch spectrum**
(core bonds/equity leave large surplus risk) and the **2022 rate-bet lesson**. A real plan's liability is
a *cashflow schedule*, not one ETF — **`binnacle_2`** = actuarial liability cashflows + **key-rate**
duration matching across the curve (not a single-point duration), which is where curve-reshaping risk
(2022 was also a steepening) actually bites.

## Reproduce

```bash
export ALPACA_KEY_ID=... ALPACA_SECRET_KEY=...
python3 research/binnacle_1.py
```

---

*Blaque Baux — a Carter Warrens research initiative. Research only; not investment advice. The verdict
falls where the data puts it — and the point of a hedge is that it's flat whether you were right or wrong.*
