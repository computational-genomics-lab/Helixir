"""Master pipeline – SS prediction and Excel export."""
from __future__ import annotations

from helixir.predict      import chou_fasman, gor4, consensus_ss, ss_stats
from helixir.display      import print_header, print_alignment_block
from helixir.excel_writer import write_xlsx


def analyze_all(
    sequences: list[tuple[str, str]],
    output_xlsx: str = "helixir_results.xlsx",
    input_file: str  = "",
) -> list[dict]:
    """
    Run the complete Helixir analysis pipeline.

    Parameters
    ----------
    sequences   : list of (id, sequence) tuples.
    output_xlsx : Output .xlsx file path.
    input_file  : Original input path (used in report header).

    Returns
    -------
    list of result dicts, one per sequence.
    """
    all_results: list[dict] = []

    for seq_id, sequence in sequences:
        n = len(sequence)
        print_header(f"Analysing: {seq_id}  ({n} aa)")

        cf_ss  = chou_fasman(sequence)
        gor_ss = gor4(sequence)
        con_ss = consensus_ss(cf_ss, gor_ss)

        print_alignment_block(sequence, cf_ss,  "Chou-Fasman:")
        print_alignment_block(sequence, gor_ss, "GOR IV:")
        print_alignment_block(sequence, con_ss, "Consensus:")

        con_stats = ss_stats(sequence, con_ss)
        print(f"  Consensus → Helix: {con_stats['pct']['H']}%  "
              f"Strand: {con_stats['pct']['E']}%  "
              f"Coil: {con_stats['pct']['C']}%")

        all_results.append({
            "id"      : seq_id,
            "sequence": sequence,
            "length"  : n,
            "ss"      : {"cf": cf_ss, "gor": gor_ss, "con": con_ss},
            "stats"   : {
                "cf" : ss_stats(sequence, cf_ss),
                "gor": ss_stats(sequence, gor_ss),
                "con": con_stats,
            },
        })

    print(f"\n[Helixir] Writing {output_xlsx} …")
    write_xlsx(all_results, output_xlsx, input_file)
    print(f"[✓] Saved: {output_xlsx}  (3 sheets: Summary · Structure & Composition · Residue Map)\n")

    return all_results
