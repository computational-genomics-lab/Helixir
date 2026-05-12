# Helixir 🧬

[![CI][badge-ci]][link-ci]
[![PyPI][badge-pypi]][link-pypi]
[![Python][badge-python]][link-python]
[![License: MIT][badge-license]][link-license]

<!-- Badge images -->
[badge-ci]:      https://github.com/your-username/helixir/actions/workflows/ci.yml/badge.svg
[badge-pypi]:    https://img.shields.io/pypi/v/helixir.svg
[badge-python]:  https://img.shields.io/pypi/pyversions/helixir.svg
[badge-license]: https://img.shields.io/badge/License-MIT-yellow.svg

<!-- Badge links -->
[link-ci]:      https://github.com/your-username/helixir/actions
[link-pypi]:    https://pypi.org/project/helixir/
[link-python]:  https://pypi.org/project/helixir/
[link-license]: LICENSE

**Helixir** predicts secondary structure of peptides and proteins from their primary amino acid sequence using **Chou-Fasman** and **GOR IV** algorithms, and exports a richly formatted **`.xlsx`** report.

---

## Features

| | |
|---|---|
| 🧬 **Chou-Fasman** | Propensity-based α-helix / β-strand / coil prediction |
| 📊 **GOR IV** | Information-theory single-residue prediction |
| 🔀 **Consensus** | Majority-vote combination of both methods |
| 📥 **Multi-format input** | `.fasta` · `.csv` · `.tsv` · `.xlsx` |
| 📤 **Excel output** | 3 focused sheets — Summary · Structure & Composition · Residue Map |
| 💬 **Interactive mode** | Guided prompts for input path, output path, no flags needed |

---

## Installation

```bash
# From PyPI
pip install helixir

# From source
git clone https://github.com/your-username/helixir.git
cd helixir
pip install -e ".[dev]"
```

**Requirements:** Python ≥ 3.9, Biopython, openpyxl, pandas, colorama, tabulate

---

## Usage

### Interactive mode

Run with no arguments — Helixir guides you through everything:

```
$ helixir

╔══════════════════════════════════════════════════════════════╗
║          H E L I X I R  –  Structure Prediction             ║
║   Chou-Fasman · GOR IV · Excel Report                       ║
╚══════════════════════════════════════════════════════════════╝

  Supported input formats: .fasta  .fa  .csv  .tsv  .xlsx
  Tip: If the file is in the current folder, just type the filename.
       Otherwise paste the full path (e.g. /data/proteins.fasta).
  ────────────────────────────────────────────────────────────────
  Input type — (1) file  (2) paste sequence  (3) demo [1]:

  Output file name or path [helixir_results.xlsx]:
```

### Command-line flags

```bash
# From a file in the current folder
helixir -f sequences.fasta

# Full path to a file
helixir -f /data/experiments/proteins.csv --out /results/run1.xlsx

# Single sequence
helixir -s MKTAYIAKQRQISFVKSHFSRQLEERLGL --out single.xlsx

# Built-in demo (Human HSP70)
helixir --demo

# Show version
helixir --version
```

### Python API

```python
from helixir import analyze_all

results = analyze_all(
    sequences=[
        ("Insulin", "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGS..."),
        ("GLP-1",   "HAEGTFTSDVSSYLEGQAAKEFIAWLVKGR"),
    ],
    output_xlsx="my_results.xlsx",
)

# Individual prediction functions
from helixir import chou_fasman, gor4, consensus_ss, ss_stats

seq = "MKTAYIAKQRQISFVKSHFSRQLEERLGL"
ss  = consensus_ss(chou_fasman(seq), gor4(seq))
print(ss_stats(seq, ss)["pct"])   # {"H": 85.0, "E": 0.0, "C": 15.0}
```

---

## Input file format

### FASTA
```
>Insulin_Human
MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFT...
>GLP1_Human
HAEGTFTSDVSSYLEGQAAKEFIAWLVKGR
```

### CSV / TSV / XLSX

Column headers are auto-detected:

| ID column | Sequence column |
|-----------|-----------------|
| `id`, `name`, `accession`, `gene`, `protein_id` | `sequence`, `seq`, `aa_sequence`, `protein`, `peptide` |

Fallback if headers not found: column 1 = ID, column 2 = sequence.

```csv
id,sequence
Insulin_Human,MALWMRLLPLLALLALWGPDPAAAFVNQHLCGS...
GLP1_Human,HAEGTFTSDVSSYLEGQAAKEFIAWLVKGR
```

---

## Excel output — 3 sheets

| Sheet | Contents |
|-------|----------|
| **Summary** | One row per sequence — ID, full sequence, length, SS % (all 3 methods) colour-coded, longest helix/strand, residue class breakdown % |
| **Structure & Composition** | Per-sequence: primary sequence chunks · CF/GOR IV/Consensus prediction strings · SS content table · structural segments · AA composition with class colours |
| **Residue Map** | Per-residue scrollable table for all sequences — Pos · AA · Class · CF · GOR · Consensus · Pα · Pβ · Pt |

**Colour key:** 🩷 pink = α-helix · 🩵 blue = β-strand · 💚 green = coil/loop

---

## Project layout

```
helixir/
├── helixir/
│   ├── __init__.py        public API
│   ├── __main__.py        python -m helixir
│   ├── cli.py             interactive + argparse entry-point
│   ├── parameters.py      CF & GOR IV residue tables + AA class sets
│   ├── predict.py         chou_fasman / gor4 / consensus_ss / ss_stats
│   ├── io_parser.py       parse_input_file  (FASTA / CSV / TSV / XLSX)
│   ├── display.py         console colour output
│   ├── excel_writer.py    write_xlsx  (openpyxl, 3 sheets)
│   └── pipeline.py        analyze_all  (master orchestrator)
├── tests/
│   ├── test_predict.py
│   └── test_cli.py
├── .github/
│   └── workflows/
│       └── ci.yml         GitHub Actions (Python 3.9 – 3.12)
├── pyproject.toml
├── setup.cfg
├── requirements.txt
├── MANIFEST.in
├── LICENSE
├── CHANGELOG.md
└── README.md
```

---

## Development

```bash
git clone https://github.com/your-username/helixir.git
cd helixir
pip install -e ".[dev]"

pytest                                   # run all tests
pytest --cov=helixir --cov-report=html   # with coverage
```

---

## Publishing to PyPI

```bash
pip install build twine
python -m build
twine upload dist/*
```

---

## References

- Chou PY, Fasman GD (1978). *Prediction of the secondary structure of proteins from their amino acid sequence.* Adv. Enzymol. **47**, 45–148.
- Garnier J, Gibrat J-F, Robson B (1996). *GOR method for predicting protein secondary structure.* Methods Enzymol. **266**, 540–553.

---

## License

[MIT](LICENSE) © Your Name
