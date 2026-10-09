#!/usr/bin/python3
# =============================================================================
# binnacle_1.py — LDI duration-matching: immunize the funded ratio (match, don't beat).
#
# A binnacle is the housing that keeps the compass steady on a pitching ship. The LDI mandate isn't
# return — it's keeping ASSETS tracking LIABILITIES so the funded ratio doesn't lurch. A pension/insurer
# liability ≈ a long-duration bond (its PV rises/falls with rates). Immunize by matching asset duration
# to the liability; the surplus (assets − liabilities) then barely moves regardless of rates.
#   Q1  Which asset mix MINIMIZES funded-ratio (surplus) volatility? (the immunization result)
#   Q2  The 2022 case — rates rose, liabilities fell; what happened to each book's funded ratio?
#   Q3  The frontier — surplus return vs surplus vol (you give up the rate bet BOTH ways)
#   Q4  Funded-ratio drawdown — the real LDI risk is becoming underfunded
# Not a return edge — risk ELIMINATION for a liability mandate. Liability proxy = TLT (long duration).
# Alpaca SIP daily, total-return.
# =============================================================================
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from _binnacle_common import panel, rets

LIAB = "TLT"   # long-duration liability proxy (~17y)

def funded(asset, liab):
    fr = np.cumprod((1+asset)/(1+liab))          # funded-ratio path, start 1.0
    dd = (fr/np.maximum.accumulate(fr)-1).min()
    surplus = asset - liab
    return dict(svol=surplus.std()*math.sqrt(252), smean=surplus.mean()*252, fr_end=fr[-1],
                fr_dd=float(dd), sskew=float(((surplus-surplus.mean())/surplus.std())**3 @ np.ones(len(surplus))/len(surplus)))

def main():
    syms=["SPY","IEF","TLT","EDV","AGG","LQD","BIL"]
    P,dates=panel(syms); R={s:rets(P[s]) for s in P}
    L=min(len(R[s]) for s in R); months=[d[:7] for d in dates[1:]][-L:]; r={s:R[s][-L:] for s in R}
    liab=r[LIAB]
    print("="*90); print("BINNACLE — LDI duration-matching: immunize the funded ratio (match, don't beat)"); print("="*90)
    print(f"  window {dates[-L]}..{dates[-1]}  ({L/252:.1f}y)   liability proxy = {LIAB} (long duration)")

    books = {
        "100% equity (SPY)":      r["SPY"],
        "60/40 (SPY/IEF)":        0.6*r["SPY"]+0.4*r["IEF"],
        "AGG (core bonds)":       r["AGG"],
        "IEF (under-hedged 7-10y)":r["IEF"],
        "TLT (DURATION-MATCHED)": r["TLT"],
        "EDV (over-hedged ~24y)": r["EDV"],
        "hybrid 40 SPY / 60 TLT": 0.4*r["SPY"]+0.6*r["TLT"],
    }
    M={k:funded(v,liab) for k,v in books.items()}
    print("\n  Q1/Q3/Q4  FUNDED-RATIO behaviour by asset mix")
    print(f"  {'asset book':28}{'surplus vol':>12}{'surplus ret':>12}{'FR maxDD':>10}{'FR end':>9}")
    for k in sorted(M,key=lambda x:M[x]['svol']):
        m=M[k]; print(f"  {k:28}{m['svol']*100:>+11.1f}%{m['smean']*100:>+11.1f}%{m['fr_dd']*100:>+9.0f}%{m['fr_end']:>9.2f}")

    # Q2: 2022 — rates rose, liabilities fell
    print("\n  Q2  2022 (rates rose → liability PV fell): funded-ratio change")
    idx=[i for i,m in enumerate(months) if m.startswith("2022")]
    lia22=np.prod([1+liab[i] for i in idx])-1
    print(f"      liability (TLT) 2022 return: {lia22*100:+.0f}%  (liabilities shrank — good for the plan IF assets held)")
    for k,v in books.items():
        a22=np.prod([1+v[i] for i in idx])-1; fr=(1+a22)/(1+lia22)-1
        print(f"      {k:28} assets {a22*100:>+6.0f}%  → funded ratio {fr*100:>+6.1f}%")

    print("\n  READ: the DURATION-MATCHED book (TLT) drives surplus volatility toward zero — that is")
    print("  immunization, and it's the whole job: the funded ratio stops lurching with rates. It is NOT a")
    print("  return edge (matched = you earn the liability, give up the rate bet BOTH ways). Under-hedged")
    print("  books (equity/IEF) happened to GAIN funded ratio in 2022 because liabilities fell faster than")
    print("  assets — but that's a rate BET that pays only when rates rise. LDI = stop betting on rates.")
    print("  A liability-capstone stabilizer, paired with bedrock (carry) + a growth leg (banyan).")

if __name__ == "__main__":
    main()
