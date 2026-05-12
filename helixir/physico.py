"""
Physicochemical property analysis using Biopython ProteinAnalysis.

Properties computed
-------------------
molecular_weight      Da
isoelectric_point     pH
gravy                 GRAVY hydrophobicity index (Kyte-Doolittle)
aromaticity           fraction of F+W+Y residues
instability_index     Guruprasad 1990 (< 40 = stable)
charge_at_ph7         net charge at pH 7.0
helix_fraction        fraction predicted as helix (Chou-Fasman)
turn_fraction         fraction predicted as turn
sheet_fraction        fraction predicted as sheet
ext_coeff_reduced     molar extinction coefficient (reduced Cys)
ext_coeff_disulfide   molar extinction coefficient (all Cys in disulfide)
half_life_mammalian   estimated half-life (mammalian, h)
half_life_yeast       estimated half-life (yeast, h)
half_life_ecoli       estimated half-life (E. coli, min)
aa_count              dict of residue counts
aa_percent            dict of residue percentages
"""

from __future__ import annotations


def analyze(sequence: str) -> dict:
    """Return a comprehensive physicochemical property dict for *sequence*."""
    try:
        from Bio.SeqUtils.ProtParam import ProteinAnalysis
    except ImportError:
        return {"error": "Biopython required. pip install biopython"}

    # ProteinAnalysis requires standard 20 AA; replace X with A as placeholder
    clean = sequence.upper().replace("X", "A")
    pa    = ProteinAnalysis(clean)
    n     = len(clean)

    mw     = round(pa.molecular_weight(), 2)
    pi     = round(pa.isoelectric_point(), 2)
    gravy  = round(pa.gravy(), 3)
    aroma  = round(pa.aromaticity(), 4)
    instab = round(pa.instability_index(), 2)

    # Charge at pH 7
    try:
        charge7 = round(pa.charge_at_pH(7.0), 3)
    except Exception:
        charge7 = "N/A"

    # Secondary structure fractions (Chou-Fasman via Biopython)
    try:
        h_frac, t_frac, s_frac = pa.secondary_structure_fraction()
        h_frac = round(h_frac, 4)
        t_frac = round(t_frac, 4)
        s_frac = round(s_frac, 4)
    except Exception:
        h_frac = t_frac = s_frac = "N/A"

    # Molar extinction coefficient
    try:
        ext_r, ext_d = pa.molar_extinction_coefficient()
    except Exception:
        ext_r = ext_d = "N/A"

    # Half-life estimates based on N-terminal rule
    # Biopython returns a dict keyed by organism
    try:
        hl = pa.protein_scale(
            ProteinAnalysis._ExPASy_scales["Miyazawa1985"], window=1
        )
        hl_mammal = hl_yeast = hl_ecoli = "N/A"
    except Exception:
        hl_mammal = hl_yeast = hl_ecoli = "N/A"

    # Use N-terminal residue look-up (standard table)
    n_term = clean[0] if clean else "A"
    HL_MAMMALIAN = {
        "A":"4.4 h","R":"1 h","N":"1.4 h","D":"1.1 h","C":">20 h",
        "E":"1 h","Q":"0.8 h","G":">20 h","H":"3.5 h","I":"20 h",
        "L":"5.5 h","K":"1.3 h","M":"30 min","F":"1.1 h","P":">20 h",
        "S":"1.9 h","T":"7.2 h","W":"2.8 h","Y":"2.8 h","V":"100 h",
    }
    HL_YEAST = {
        "A":">20 h","R":"2 min","N":"3 min","D":"3 min","C":">20 h",
        "E":"30 min","Q":"10 min","G":">20 h","H":"10 min","I":"30 min",
        "L":"3 min","K":"3 min","M":">20 h","F":"3 min","P":">20 h",
        "S":">20 h","T":">20 h","W":"3 min","Y":"10 min","V":">20 h",
    }
    HL_ECOLI = {
        "A":">10 h","R":"2 min","N":"3 min","D":">10 h","C":">10 h",
        "E":"5 min","Q":"10 min","G":">10 h","H":">10 h","I":"5 min",
        "L":"2 min","K":"2 min","M":">10 h","F":"2 min","P":">10 h",
        "S":">10 h","T":">10 h","W":"2 min","Y":"2 min","V":"100 min",
    }
    hl_mammal = HL_MAMMALIAN.get(n_term, "N/A")
    hl_yeast  = HL_YEAST.get(n_term, "N/A")
    hl_ecoli  = HL_ECOLI.get(n_term, "N/A")

    # AA composition
    aa_count   = dict(pa.count_amino_acids())
    aa_percent = {k: round(v/n*100, 2) for k,v in aa_count.items() if v > 0}

    # Residue class breakdown
    from helixir.parameters import HYDROPHOBIC, POLAR, CHARGED_POS, CHARGED_NEG, AROMATIC
    def _class_pct(cls):
        return round(sum(aa_count.get(a,0) for a in cls) / n * 100, 1)

    return {
        "molecular_weight"    : mw,
        "isoelectric_point"   : pi,
        "gravy"               : gravy,
        "aromaticity"         : aroma,
        "instability_index"   : instab,
        "stability"           : "Stable" if instab < 40 else "Unstable",
        "charge_at_ph7"       : charge7,
        "charge_class"        : ("Positive" if isinstance(charge7,float) and charge7 > 0.5
                                 else "Negative" if isinstance(charge7,float) and charge7 < -0.5
                                 else "Neutral"),
        "ss_helix_fraction"   : h_frac,
        "ss_turn_fraction"    : t_frac,
        "ss_sheet_fraction"   : s_frac,
        "ext_coeff_reduced"   : ext_r,
        "ext_coeff_disulfide" : ext_d,
        "half_life_mammalian" : hl_mammal,
        "half_life_yeast"     : hl_yeast,
        "half_life_ecoli"     : hl_ecoli,
        "pct_hydrophobic"     : _class_pct(HYDROPHOBIC),
        "pct_polar"           : _class_pct(POLAR),
        "pct_charged_pos"     : _class_pct(CHARGED_POS),
        "pct_charged_neg"     : _class_pct(CHARGED_NEG),
        "pct_aromatic"        : _class_pct(AROMATIC),
        "aa_count"            : aa_count,
        "aa_percent"          : aa_percent,
        "length"              : n,
    }
