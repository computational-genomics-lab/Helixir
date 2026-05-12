"""Input file parsing for FASTA / CSV / TSV / XLSX."""
from __future__ import annotations
import os
from helixir.parameters import VALID_AA


def validate_sequence(seq: str) -> str:
    seq = seq.upper().strip().replace(" ","").replace("\n","")
    invalid = set(seq) - VALID_AA
    if invalid:
        raise ValueError(f"Invalid amino acid characters: {invalid}")
    return seq


def parse_input_file(filepath: str) -> list[tuple[str, str]]:
    """
    Parse sequences from FASTA, CSV, TSV, or XLSX.
    Returns list of (id, sequence) tuples.
    """
    ext = os.path.splitext(filepath)[1].lower()
    if ext in (".fasta",".fa",".faa",".fna"):
        return _parse_fasta(filepath)
    if ext in (".csv",".tsv",".xlsx",".xlsm",".xls"):
        return _parse_tabular(filepath, ext)
    raise ValueError(
        f'Unsupported extension "{ext}". Supported: .fasta .fa .csv .tsv .xlsx'
    )


def _parse_fasta(filepath):
    try:
        from Bio import SeqIO
    except ImportError as e:
        raise ImportError("Biopython required. pip install biopython") from e
    records = [(r.id, validate_sequence(str(r.seq)))
               for r in SeqIO.parse(filepath, "fasta")]
    if not records:
        raise ValueError(f"No sequences found in {filepath!r}")
    return records


def _parse_tabular(filepath, ext):
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError("pandas required. pip install pandas") from e

    if ext == ".csv":   df = pd.read_csv(filepath, dtype=str).fillna("")
    elif ext == ".tsv": df = pd.read_csv(filepath, sep="\t", dtype=str).fillna("")
    else:               df = pd.read_excel(filepath, dtype=str).fillna("")

    if df.empty:
        raise ValueError(f"No data in {filepath!r}")

    cols    = [c.lower().strip() for c in df.columns]
    ID_K    = {"id","name","accession","gene","protein_id"}
    SEQ_K   = {"sequence","seq","aa_sequence","protein","peptide"}
    id_col  = next((i for i,c in enumerate(cols) if c in ID_K),  0)
    seq_col = next((i for i,c in enumerate(cols) if c in SEQ_K), min(1,len(df.columns)-1))

    records = []
    for _, row in df.iterrows():
        sid = str(row.iloc[id_col]).strip()
        s   = str(row.iloc[seq_col]).strip()
        if not s: continue
        try:
            records.append((sid, validate_sequence(s)))
        except ValueError as e:
            print(f"  [SKIP] {sid}: {e}")
    if not records:
        raise ValueError("No valid sequences parsed.")
    return records
