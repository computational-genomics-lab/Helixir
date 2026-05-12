"""Console display helpers."""
from __future__ import annotations

try:
    from colorama import Fore, Style, init as _ci
    _ci(autoreset=True)
    _COL = True
except ImportError:
    _COL = False

LINE  = "─" * 80
_B    = Style.BRIGHT    if _COL else ""
_R    = Style.RESET_ALL if _COL else ""
_SS   = {"H": Fore.RED if _COL else "", "E": Fore.YELLOW if _COL else "", "C": Fore.CYAN if _COL else ""}


def print_header(title: str) -> None:
    print(f"\n{_B}{LINE}\n  {title}\n{LINE}{_R}")


def color_ss(ss: str) -> str:
    if not _COL: return ss
    return "".join(f"{_SS.get(c,'')}{c}{Style.RESET_ALL}" for c in ss)


def print_alignment_block(sequence: str, ss: str, label: str, width: int = 60) -> None:
    print(f"\n  {_B}{label}{_R}")
    for i in range(0, len(sequence), width):
        chunk = sequence[i:i+width]
        ruler = "".join(str((i+j+1)%10) for j in range(len(chunk)))
        print(f"  {i+1:>5}  {chunk}")
        print(f"  {i+1:>5}  {color_ss(ss[i:i+width])}   (H=helix E=strand C=coil)")
        print(f"         {ruler}\n")
