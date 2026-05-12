"""Helixir CLI – interactive + flag-based, no BLAST."""
from __future__ import annotations
import argparse, os, sys, textwrap

from helixir.io_parser import parse_input_file, validate_sequence
from helixir.pipeline  import analyze_all

_DEMO_SEQ = (
    "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVK"
    "ALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWE"
    "RVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDL"
    "DAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWN"
    "PVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRL"
    "TMLLLQLPHIGQVQAGVWPAAVRESVPSLL"
)

_SUPPORTED = ".fasta  .fa  .csv  .tsv  .xlsx"
_SEP       = "─" * 64


def _banner():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          H E L I X I R  –  Structure Prediction             ║")
    print("║   Chou-Fasman · GOR IV · Excel Report                       ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()


def _prompt(msg, default=""):
    hint = f"  [{default}]" if default else ""
    raw  = input(f"  {msg}{hint}: ").strip()
    return raw if raw else default


def _resolve(raw): return os.path.abspath(raw)


def _ask_input(args):
    if args.demo:
        print("  [INFO] Using built-in demo: Human HSP70 fragment")
        return [("HSP70_demo", _DEMO_SEQ)], ""
    if args.sequence:
        return [("query", validate_sequence(args.sequence))], ""
    if args.file:
        path = _resolve(args.file)
        seqs = parse_input_file(path)
        print(f"  [INFO] Loaded {len(seqs)} sequence(s) from: {path}")
        return seqs, path

    # fully interactive
    _banner()
    print(f"  Supported input formats: {_SUPPORTED}")
    print(f"  Tip: filename only if file is in current folder;")
    print(f"       otherwise paste the full path.")
    print(_SEP)
    while True:
        choice = _prompt("Input type — (1) file  (2) paste sequence  (3) demo", "1")
        if choice == "3":
            print("  [INFO] Using built-in demo: Human HSP70 fragment")
            return [("HSP70_demo", _DEMO_SEQ)], ""
        if choice == "2":
            seq_id = _prompt("Sequence ID", "query")
            print("  Paste your amino acid sequence and press Enter:")
            raw = input("  ").strip()
            if not raw:
                print("  [ERROR] No sequence entered.\n"); continue
            try:    return [(seq_id, validate_sequence(raw))], ""
            except ValueError as e: print(f"  [ERROR] {e}\n"); continue
        raw_path = _prompt("Input file name or full path")
        if not raw_path: print("  [ERROR] No path entered.\n"); continue
        path = _resolve(raw_path)
        if not os.path.isfile(path):
            print(f"  [ERROR] File not found: {path}\n"); continue
        try:
            seqs = parse_input_file(path)
            print(f"  [INFO] Loaded {len(seqs)} sequence(s) from: {path}")
            return seqs, path
        except Exception as e:
            print(f"  [ERROR] {e}\n")


def _ask_output(args):
    if args.out:
        p = _resolve(args.out)
    else:
        print()
        print("  Output file")
        print("  Tip: filename only saves to current folder; or give a full path.")
        print(_SEP)
        raw = _prompt("Output file name or path", "helixir_results.xlsx")
        p   = _resolve(raw)
    if not p.lower().endswith(".xlsx"):
        p += ".xlsx"
    return p


def build_parser():
    p = argparse.ArgumentParser(
        prog="helixir",
        description="Helixir – Peptide secondary structure prediction and analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(f"""
            Input  : {_SUPPORTED}
            Output : .xlsx  (3 sheets)

            Examples
            --------
            helixir                              # fully interactive
            helixir -f proteins.fasta
            helixir -f data.csv  --out results.xlsx
            helixir -s ACDEFGHIKLMNPQRSTVWY
            helixir --demo
        """),
    )
    src = p.add_mutually_exclusive_group()
    src.add_argument("-f","--file",     metavar="FILE",
                     help="Input file (.fasta / .csv / .tsv / .xlsx)")
    src.add_argument("-s","--sequence", metavar="SEQ",
                     help="Single amino acid sequence string")
    src.add_argument("--demo",          action="store_true",
                     help="Run built-in Human HSP70 demo")
    p.add_argument("--out",   metavar="OUT", help="Output .xlsx path")
    p.add_argument("--version", action="store_true", help="Print version and exit")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.version:
        from helixir import __version__
        print(f"Helixir {__version__}"); sys.exit(0)

    sequences, input_file = _ask_input(args)
    output_path           = _ask_output(args)

    print()
    print("  ┌─ Run summary " + "─" * 48)
    print(f"  │  Sequences  : {len(sequences)}")
    print(f"  │  Output     : {output_path}")
    print("  └" + "─" * 61)
    print()

    analyze_all(sequences=sequences, output_xlsx=output_path, input_file=input_file)


if __name__ == "__main__":
    main()
