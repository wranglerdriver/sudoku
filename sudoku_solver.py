#!/usr/bin/env python3
"""
Sudoku Solver (9x9)
==================

This script solves standard 9x9 Sudoku puzzles with a backtracking search.

How it works (high level)
-------------------------
1) Parse the puzzle input into a 9x9 integer grid.
2) Find an empty cell (value 0) with the fewest valid candidates.
3) Try each candidate value recursively.
4) If a branch becomes invalid, undo the move (backtrack).
5) Finish when there are no empty cells left.

Input format
------------
- 81-character string of digits where `0` or `.` means empty, OR
- 9 lines of 9 characters each (same digit rules).

Examples
--------
  python3 sudoku_solver.py "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

  python3 sudoku_solver.py << 'EOF'
  530070000
  600195000
  098000060
  800060003
  400803001
  700020006
  060000280
  000419005
  000080079
  EOF

Output
------
- Prints a solved board with 3x3 separators.
- Prints "No solution found." if puzzle is unsatisfiable.
"""

import sys
from typing import List, Optional, Tuple

Grid = List[List[int]]


def parse_input(text: str) -> Grid:
    """Parse raw input text into a 9x9 grid of ints (0 means empty)."""
    chars = [c for c in text if c in "0123456789."]
    if len(chars) != 81:
        raise ValueError("Expected 81 digits/dots for a 9x9 Sudoku.")
    vals = [0 if c in "0." else int(c) for c in chars]
    return [vals[i * 9:(i + 1) * 9] for i in range(9)]


def is_valid(grid: Grid, r: int, c: int, n: int) -> bool:
    """Return True if placing n at (r, c) obeys Sudoku rules."""
    if any(grid[r][x] == n for x in range(9)):
        return False
    if any(grid[x][c] == n for x in range(9)):
        return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if grid[i][j] == n:
                return False
    return True


def find_empty_with_fewest_candidates(grid: Grid) -> Optional[Tuple[int, int, List[int]]]:
    """
    Pick the next empty cell using MRV heuristic (fewest candidates first).
    Returns (row, col, candidates) or None if puzzle is complete.
    """
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cand = [n for n in range(1, 10) if is_valid(grid, r, c, n)]
                if not cand:
                    return (r, c, [])
                if best is None or len(cand) < len(best[2]):
                    best = (r, c, cand)
                    if len(cand) == 1:
                        return best
    return best


def solve(grid: Grid) -> bool:
    """Solve in-place via recursive backtracking. Returns True if solved."""
    pick = find_empty_with_fewest_candidates(grid)
    if pick is None:
        return True
    r, c, cand = pick
    for n in cand:
        grid[r][c] = n
        if solve(grid):
            return True
        grid[r][c] = 0
    return False


def format_grid(grid: Grid) -> str:
    lines = []
    for r in range(9):
        row = " ".join(str(n) for n in grid[r][0:3]) + " | " + \
              " ".join(str(n) for n in grid[r][3:6]) + " | " + \
              " ".join(str(n) for n in grid[r][6:9])
        lines.append(row)
        if r in (2, 5):
            lines.append("-" * 21)
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = sys.stdin.read().strip()

    if not raw:
        print("Provide a puzzle as an 81-char string (0/. for blanks) or via stdin.")
        return 2

    try:
        grid = parse_input(raw)
    except ValueError as e:
        print(f"Input error: {e}")
        return 2

    if solve(grid):
        print(format_grid(grid))
        return 0

    print("No solution found.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
