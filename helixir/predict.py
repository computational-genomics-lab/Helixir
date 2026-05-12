"""Secondary structure prediction engines."""

from helixir.parameters import CHOU_FASMAN, GOR_SINGLE


def _window_avg(seq: str, start: int, end: int, idx: int) -> float:
    total, n = 0.0, 0
    for aa in seq[start:end]:
        total += CHOU_FASMAN.get(aa.upper(), CHOU_FASMAN["X"])[idx]
        n += 1
    return total / n if n else 0.0


def chou_fasman(sequence: str) -> str:
    seq = sequence.upper(); n = len(seq); ss = ["C"] * n
    for i in range(n - 3):
        seg = seq[i:i+4]
        if sum(1 for a in seg if CHOU_FASMAN.get(a,(0,))[0] >= 1.00) >= 3 and _window_avg(seq,i,i+4,0) > 1.00:
            for j in range(i, i+4): ss[j] = "h"
    for i in range(n):
        if ss[i] == "h":
            j = i-1
            while j >= 0 and _window_avg(seq,max(0,j-1),j+3,0) > 1.00: ss[j]="h"; j-=1
            j = i+1
            while j < n  and _window_avg(seq,j-2,min(n,j+2),0) > 1.00: ss[j]="h"; j+=1
    for i in range(n - 2):
        seg = seq[i:i+3]
        if sum(1 for a in seg if CHOU_FASMAN.get(a,(0,0))[1] >= 1.00) >= 2 and _window_avg(seq,i,i+3,1) > 1.05:
            for j in range(i, i+3):
                if ss[j] == "C": ss[j] = "e"
    for i in range(n):
        if ss[i] == "e":
            j = i+1
            while j < n and _window_avg(seq,max(0,j-1),min(n,j+2),1) > 1.00:
                if ss[j] == "C": ss[j] = "e"
                j += 1
    return "".join("H" if s=="h" else "E" if s=="e" else "C" for s in ss)


def gor4(sequence: str) -> str:
    result = []
    for aa in sequence.upper():
        i_h, i_e, i_c = GOR_SINGLE.get(aa, GOR_SINGLE["X"])
        result.append(max(("H",i_h),("E",i_e),("C",i_c), key=lambda x:x[1])[0])
    return "".join(result)


def consensus_ss(cf: str, gor: str) -> str:
    out = []
    for a, b in zip(cf, gor):
        if a == b:          out.append(a)
        elif "H" in (a,b):  out.append("H")
        elif "E" in (a,b):  out.append("E")
        else:               out.append("C")
    return "".join(out)


def ss_stats(sequence: str, ss: str) -> dict:
    n      = len(ss)
    counts = {"H": ss.count("H"), "E": ss.count("E"), "C": ss.count("C")}
    pct    = ({k: round(v/n*100,1) for k,v in counts.items()}
              if n else {"H":0.0,"E":0.0,"C":0.0})
    if not n:
        return {"counts":counts,"pct":pct,"segments":[],"length":n}
    segs, prev, start = [], ss[0], 0
    for i in range(1, n):
        if ss[i] != prev:
            segs.append({"type":prev,"start":start+1,"end":i,
                         "length":i-start,"seq":sequence[start:i]})
            start, prev = i, ss[i]
    segs.append({"type":prev,"start":start+1,"end":n,
                 "length":n-start,"seq":sequence[start:n]})
    return {"counts":counts,"pct":pct,"segments":segs,"length":n}
