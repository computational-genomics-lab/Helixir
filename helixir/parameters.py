"""
Chou-Fasman (1978) and GOR IV (1996) residue parameters.
"""

CHOU_FASMAN: dict[str, tuple[float, float, float]] = {
    "A": (1.42, 0.83, 0.66), "R": (0.98, 0.93, 0.95),
    "N": (0.67, 0.89, 1.56), "D": (1.01, 0.54, 1.46),
    "C": (0.70, 1.19, 1.19), "E": (1.51, 0.37, 0.74),
    "Q": (1.11, 1.10, 0.98), "G": (0.57, 0.75, 1.56),
    "H": (1.00, 0.87, 0.95), "I": (1.08, 1.60, 0.47),
    "L": (1.21, 1.30, 0.59), "K": (1.16, 0.74, 1.01),
    "M": (1.45, 1.05, 0.60), "F": (1.13, 1.38, 0.60),
    "P": (0.57, 0.55, 1.52), "S": (0.77, 0.75, 1.43),
    "T": (0.83, 1.19, 0.96), "W": (1.08, 1.37, 0.96),
    "Y": (0.69, 1.47, 1.14), "V": (1.06, 1.70, 0.50),
    "X": (1.00, 1.00, 1.00),
}

GOR_SINGLE: dict[str, tuple[float, float, float]] = {
    "A": ( 0.24, -0.29,  0.05), "R": ( 0.29, -0.18, -0.12),
    "N": (-0.39,  0.02,  0.37), "D": (-0.11, -0.40,  0.51),
    "C": (-0.14,  0.44, -0.30), "E": ( 0.42, -0.49,  0.07),
    "Q": ( 0.21, -0.13, -0.08), "G": (-0.52, -0.16,  0.68),
    "H": ( 0.04,  0.08, -0.12), "I": (-0.04,  0.67, -0.63),
    "L": ( 0.49,  0.27, -0.76), "K": ( 0.18, -0.38,  0.20),
    "M": ( 0.37,  0.29, -0.66), "F": ( 0.08,  0.51, -0.59),
    "P": (-1.05, -0.59,  1.64), "S": (-0.23, -0.06,  0.29),
    "T": (-0.25,  0.40, -0.15), "W": ( 0.19,  0.60, -0.79),
    "Y": (-0.31,  0.48, -0.17), "V": (-0.18,  0.76, -0.58),
    "X": ( 0.00,  0.00,  0.00),
}

AA_NAMES: dict[str, str] = {
    "A": "Alanine",      "R": "Arginine",     "N": "Asparagine",
    "D": "Aspartic Acid","C": "Cysteine",      "E": "Glutamic Acid",
    "Q": "Glutamine",    "G": "Glycine",       "H": "Histidine",
    "I": "Isoleucine",   "L": "Leucine",       "K": "Lysine",
    "M": "Methionine",   "F": "Phenylalanine", "P": "Proline",
    "S": "Serine",       "T": "Threonine",     "W": "Tryptophan",
    "Y": "Tyrosine",     "V": "Valine",        "X": "Unknown",
}

# Residue classes for annotation
HYDROPHOBIC  = set("ACFGILMVWY")
POLAR        = set("NQST")
CHARGED_POS  = set("KRH")
CHARGED_NEG  = set("DE")
AROMATIC     = set("FWY")
SPECIAL      = set("CGP")   # Cys (disulfide), Gly (flexible), Pro (helix-breaker)

VALID_AA: frozenset[str] = frozenset(CHOU_FASMAN.keys())
