"""
Remote NCBI BLASTp wrapper.
"""
from __future__ import annotations


def run_blast(
    sequence: str,
    database: str = "swissprot",
    hitlist_size: int = 10,
    e_value: float = 0.001,
) -> list[dict]:
    """
    Submit a remote BLASTp query to NCBI and return parsed hit dicts.
    Returns an empty list on failure or when Biopython is missing.
    """
    try:
        from Bio.Blast import NCBIWWW, NCBIXML
    except ImportError:
        print("[WARNING] Biopython required for BLAST. pip install biopython")
        return []

    print(f"  [BLAST] Submitting BLASTp to NCBI ({database}) …", flush=True)
    try:
        handle = NCBIWWW.qblast(
            "blastp", database, sequence,
            hitlist_size=hitlist_size,
            expect=e_value,
            format_type="XML",
        )
    except Exception as exc:
        print(f"  [ERROR] BLAST submission failed: {exc}")
        return []

    hits: list[dict] = []
    try:
        record    = next(NCBIXML.parse(handle))
        query_len = len(sequence)
        for alignment in record.alignments:
            for hsp in alignment.hsps:
                hits.append({
                    "title"      : alignment.title[:80],
                    "accession"  : alignment.accession,
                    "length"     : alignment.length,
                    "score"      : hsp.score,
                    "bits"       : round(hsp.bits, 1),
                    "evalue"     : hsp.expect,
                    "identity"   : round(hsp.identities / hsp.align_length * 100, 1),
                    "similarity" : round(hsp.positives  / hsp.align_length * 100, 1),
                    "coverage"   : round(hsp.align_length / query_len * 100, 1),
                    "gaps"       : round((hsp.gaps or 0) / hsp.align_length * 100, 1),
                    "query_seq"  : hsp.query,
                    "match_seq"  : hsp.sbjct,
                    "midline"    : hsp.match,
                })
                break
    except Exception as exc:
        print(f"  [ERROR] BLAST XML parsing: {exc}")
    return hits
