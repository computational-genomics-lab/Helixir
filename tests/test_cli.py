"""CLI tests."""
import os, pytest
from helixir.cli import main

class TestCLI:
    def test_version(self, capsys):
        with pytest.raises(SystemExit) as e: main(["--version"])
        assert e.value.code == 0
        assert "Helixir" in capsys.readouterr().out
    def test_sequence(self, tmp_path):
        out = str(tmp_path / "o.xlsx")
        main(["-s","ACDEFGHIKL","--out",out]); assert os.path.exists(out)
    def test_demo(self, tmp_path):
        out = str(tmp_path / "d.xlsx")
        main(["--demo","--out",out]); assert os.path.exists(out)
    def test_fasta(self, tmp_path):
        fa = tmp_path/"s.fasta"; fa.write_text(">P1\nACDEF\n")
        main(["-f",str(fa),"--out",str(tmp_path/"o.xlsx")])
        assert os.path.exists(str(tmp_path/"o.xlsx"))
    def test_auto_xlsx_ext(self, tmp_path):
        base = str(tmp_path/"noxlsx")
        main(["-s","ACDEF","--out",base])
        assert os.path.exists(base + ".xlsx")
