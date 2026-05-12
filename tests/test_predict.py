"""Unit tests for Helixir."""
import os, tempfile, pytest
from helixir.predict   import chou_fasman, gor4, consensus_ss, ss_stats
from helixir.io_parser import validate_sequence, parse_input_file


class TestValidate:
    def test_upper(self):  assert validate_sequence("acdef") == "ACDEF"
    def test_spaces(self): assert validate_sequence("A C D") == "ACD"
    def test_invalid(self):
        with pytest.raises(ValueError): validate_sequence("ACDEFZ")

class TestChouFasman:
    def test_length(self):  assert len(chou_fasman("MKTAYIAKQR")) == 10
    def test_states(self):  assert all(c in "HEC" for c in chou_fasman("ACDEFGHIKLMNPQRSTVWY"))
    def test_helix(self):   assert chou_fasman("EEEEEEEKKKKEEEEEKKKK").count("H") > 0
    def test_strand(self):  assert chou_fasman("FYFYFYFYFYFY").count("E") > 0

class TestGor4:
    def test_length(self):  assert len(gor4("MALWMRLL")) == 8
    def test_proline(self): assert all(c == "C" for c in gor4("PPPPPPPPPP"))

class TestConsensus:
    def test_agree(self):       assert consensus_ss("HHH","HHH") == "HHH"
    def test_helix_wins(self):  assert consensus_ss("H","E") == "H"
    def test_strand_coil(self): assert consensus_ss("E","C") == "E"

class TestSsStats:
    def test_counts(self):
        s = ss_stats("MKTAYIAKQR","HHHHCCCCEE")
        assert s["counts"] == {"H":4,"E":2,"C":4}
    def test_pct_sum(self):
        s = ss_stats("MKTAYIAKQR","HHHHCCCCEE")
        assert abs(sum(s["pct"].values()) - 100.0) < 0.5

class TestParseInput:
    def _tmp(self, suf, txt):
        fd, p = tempfile.mkstemp(suffix=suf)
        with os.fdopen(fd,"w") as f: f.write(txt)
        return p
    def test_fasta(self):
        p = self._tmp(".fasta",">s1\nACDEF\n")
        r = parse_input_file(p); os.unlink(p)
        assert r[0] == ("s1","ACDEF")
    def test_csv(self):
        p = self._tmp(".csv","id,sequence\nP1,ACDEF\n")
        r = parse_input_file(p); os.unlink(p)
        assert r[0][1] == "ACDEF"
    def test_bad_ext(self):
        with pytest.raises(ValueError, match="Unsupported"):
            parse_input_file("file.txt")

class TestPipeline:
    def test_result_keys(self, tmp_path):
        from helixir.pipeline import analyze_all
        out = str(tmp_path / "out.xlsx")
        res = analyze_all([("T","ACDEFGHIKLMNPQRSTVWY")], output_xlsx=out)
        assert res[0]["id"] == "T"
        assert all(k in res[0]["ss"] for k in ("cf","gor","con"))
        assert os.path.exists(out)

    def test_three_sheets(self, tmp_path):
        import openpyxl
        from helixir.pipeline import analyze_all
        out = str(tmp_path / "out.xlsx")
        analyze_all([("P1","ACDEFGHIKL"),("P2","MNPQRSTVWY")], output_xlsx=out)
        wb = openpyxl.load_workbook(out)
        assert wb.sheetnames == ["Summary","Structure & Composition","Residue Map"]
