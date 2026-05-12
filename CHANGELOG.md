# Changelog

All notable changes to **Helixir** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.0.0] – 2025-05-12

### Changed
- Removed BLAST similarity search (no internet dependency)
- Removed external property analysis module (available as a separate package)
- Replaced 5-sheet-per-sequence output with 3 concise global sheets:
  **Summary**, **Structure & Composition**, **Residue Map**
- Added full amino acid sequence column in Summary sheet (after ID)
- Summary sheet shows SS % for all 3 methods side-by-side, colour-coded
- Structure sheet shows segment analysis and AA composition with class colours
- Residue Map covers all sequences in one scrollable table (Pα · Pβ · Pt)
- Interactive CLI prompts for input path, output path — no flags required
- Auto-appends `.xlsx` extension to output path if omitted

### Removed
- `blast.py` module
- External property analysis module
- All BLAST CLI flags (`--blast-db`, `--hits`, `--evalue`, `--no-blast`)

---

## [1.0.0] – 2025-05-12

### Added
- Chou-Fasman secondary structure prediction engine
- GOR IV secondary structure prediction engine
- Consensus (majority-vote) prediction from both methods
- NCBI remote BLASTp integration (swissprot / nr / pdb)
- Multi-format input parser: `.fasta`, `.csv`, `.tsv`, `.xlsx`
- Installable Python package with `helixir` CLI entry-point
- Interactive prompt mode
- GitHub Actions CI workflow (Python 3.9 – 3.12)
