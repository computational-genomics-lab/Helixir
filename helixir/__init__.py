"""
Helixir – Peptide secondary structure analysis.

Quick-start
-----------
>>> from helixir import analyze_all
>>> results = analyze_all(
...     sequences=[("MyPeptide", "ACDEFGHIKLMNPQRSTVWY")],
...     output_xlsx="out.xlsx",
... )

CLI
---
    helixir                    # interactive
    helixir -f sequences.fasta
    helixir --demo
"""
from importlib.metadata import version, PackageNotFoundError
try:
    __version__: str = version("helixir")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

__author__  = "Your Name"
__license__ = "MIT"

from helixir.pipeline  import analyze_all
from helixir.predict   import chou_fasman, gor4, consensus_ss, ss_stats
from helixir.io_parser import parse_input_file, validate_sequence

__all__ = [
    "analyze_all", "chou_fasman", "gor4", "consensus_ss",
    "ss_stats", "parse_input_file", "validate_sequence",
    "__version__",
]
