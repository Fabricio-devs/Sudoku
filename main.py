import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Optional, Tuple

Board = List[List[int]]  # alias para legibilidad


class SudokuGenerator:
    """
    Responsible for generating full valid Sudoku boards and playable puzzles.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        if seed is not None:
            random.seed(seed)

    # ------------------------------------------------ #
    # ------------------ Public API ------------------ #
    # ------------------------------------------------ #
    
    def generate_puzzle(self, clues: int = 35) -> Board:
        """
        Generate a new Sudoku puzzle.

        :param clues: number of filled cells to keep (higher = easier).
        :return: 9x9 board with 0 for empty cells.
        """
        board = [[0] * 9 for _ in range(9)]
        self._fill_board(board)
        puzzle = [row[:] for row in board]
        self._remove_cells(puzzle, 81 - clues)
        return puzzle

    # ----------------------------------------------------- #
    # ------------------ Core generation ------------------ #
    # ----------------------------------------------------- #
    
    def _fill_board(self, board: Board) -> bool:
        """Use backtracking to fill the board with a complete valid solution."""
        empty = self._find_empty(board)
        if not empty:
            return True  # board completed

        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers)

        for num in numbers:
            if self._is_valid(board, row, col, num):
                board[row][col] = num
                if self._fill_board(board):
                    return True
                board[row][col] = 0
        return False

    def _find_empty(self, board: Board) -> Optional[Tuple[int, int]]:
        """Return the next empty cell (row, col), or None if full."""
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return r, c
        return None

    def _is_valid(self, board: Board, row: int, col: int, num: int) -> bool:
        """Check if 'num' can be placed at (row, col) respecting Sudoku rules."""
        # Row
        if any(board[row][c] == num for c in range(9)):
            return False
        # Column
        if any(board[r][col] == num for r in range(9)):
            return False
        # 3x3 block
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if board[r][c] == num:
                    return False
        return True

    def _remove_cells(self, board: Board, to_remove: int) -> None:
        """
        Remove 'to_remove' cells from the board to create a puzzle.

        Note: this version does not guarantee a unique solution, but it is
        good enough for a portfolio project and casual play.
        """
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)

        removed = 0
        for row, col in positions:
            if removed >= to_remove:
                break
            if board[row][col] != 0:
                board[row][col] = 0
                removed += 1


class SudokuGUI:
    """
    Tkinter-based Sudoku game.

    - Displays a 9x9 grid of Entry widgets.
    - Allows generating new puzzles, checking solution, solving, and clearing.
    - Auto-checks a row when it is fully filled.
    - Auto-checks the whole board when there are no empty cells.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sudoku Game")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.generator = SudokuGenerator()
        self.board_vars: List[List[tk.StringVar]] = [
            [tk.StringVar() for _ in range(9)] for _ in range(9)
        ]
        self.initial_fixed: List[List[bool]] = [[False] * 9 for _ in range(9)]

        self._build_widgets()
        self.new_game()
        
    # ------------------------------------------------- #
    # ------------------ UI creation ------------------ #
    # ------------------------------------------------- #
    
    def _build_widgets(self) -> None:
        """Create the Sudoku grid and control buttons."""
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        # Grid frame
        grid_frame = tk.Frame(main_frame)
        grid_frame.pack()

        self.entries: List[List[tk.Entry]] = [[None] * 9 for _ in range(9)]

        for r in range(9):
            for c in range(9):
                var = self.board_vars[r][c]

                # Validate input: only digits 1-9, max length 1
                vcmd = (self.root.register(self._validate_input), "%P")
                entry = tk.Entry(
                    grid_frame,
                    width=2,
                    justify="center",
                    font=("Consolas", 16),
                    textvariable=var,
                    validate="key",
                    validatecommand=vcmd
                )

                # Evento: cada vez que se suelta una tecla, revisamos la fila/tablero
                entry.bind("<KeyRelease>", lambda event, rr=r, cc=c: self._on_cell_change(rr, cc))

                # Bordes un poco más gruesos entre bloques 3x3 (opcional)
                padx = (0, 4) if (c + 1) % 3 == 0 and c != 8 else 1
                pady = (0, 4) if (r + 1) % 3 == 0 and r != 8 else 1

                entry.grid(row=r, column=c, padx=padx, pady=pady, ipady=5)
                entry.config(relief="solid", bd=1)

                self.entries[r][c] = entry

        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="New Game", width=12,
                  command=self.new_game).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Check", width=12,
                  command=self.check_solution).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Solve", width=12,
                  command=self.solve_puzzle).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(btn_frame, text="Clear", width=12,
                  command=self.clear_user_cells).grid(row=0, column=3, padx=5, pady=5)

        # Info label
        self.info_label = tk.Label(
            self.root,
            text="Fill the grid and press 'Check' to validate.",
            font=("Arial", 10)
        )
        self.info_label.pack(pady=5)

    # ------------------------------------------------------ #
    # ------------------ Input validation ------------------ #
    # ------------------------------------------------------ #
    
    def _validate_input(self, new_value: str) -> bool:
        """
        Validate the content of a cell entry.

        Allows:
        - empty string
        - a single digit between 1 and 9
        """
        if new_value == "":
            return True
        if len(new_value) > 1:
            return False
        return new_value in "123456789"

    # ------------------------------------------------ #
    # ------------------ Game logic ------------------ #
    # ------------------------------------------------ #
    
    def new_game(self) -> None:
        """Generate a new Sudoku puzzle and display it."""
        puzzle = self.generator.generate_puzzle(clues=35)  # adjust clues for difficulty
        self._load_board(puzzle)
        self.info_label.config(text="New puzzle generated. Good luck!", fg="black")

    def _load_board(self, board: Board) -> None:
        """
        Load a board into the UI.

        Cells with a non-zero value are fixed (not editable).
        """
        for r in range(9):
            for c in range(9):
                value = board[r][c]
                var = self.board_vars[r][c]
                entry = self.entries[r][c]

                entry.config(bg="white")  # reset background

                if value == 0:
                    var.set("")
                    entry.config(state="normal", disabledforeground="black")
                    self.initial_fixed[r][c] = False
                else:
                    var.set(str(value))
                    entry.config(state="disabled", disabledforeground="blue")
                    self.initial_fixed[r][c] = True

    def clear_user_cells(self) -> None:
        """Clear all non-fixed cells entered by the user."""
        for r in range(9):
            for c in range(9):
                if not self.initial_fixed[r][c]:
                    self.board_vars[r][c].set("")
                    self.entries[r][c].config(bg="white")
        self.info_label.config(text="Cleared user entries.", fg="black")

    def _get_current_board(self) -> Board:
        """Return the current board as a 9x9 matrix of integers."""
        board: Board = [[0] * 9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                val = self.board_vars[r][c].get()
                board[r][c] = int(val) if val.isdigit() else 0
        return board

    # ------------------------------------------------------------------ #
    # ------------------ Auto checks (fila y tablero) ------------------ #
    # ------------------------------------------------------------------ #
    
    def _on_cell_change(self, row: int, col: int) -> None:
        """
        Called every time the user edits a cell.

        - If the whole row is filled (no zeros), automatically checks that row.
        - If the whole board is filled, automatically checks the full solution.
        """
        board = self._get_current_board()

        # ------------------------------------------------------------------ #
        # ---------- Opción 1: verificar automáticamente la FILA ----------- #
        # ------------------------------------------------------------------ #
         
        if all(board[row][c] != 0 for c in range(9)):
            # Row is full -> check if valid
            if self._is_unit_valid(board[row]):
                # Fila correcta → verde suave en celdas no fijas
                for c in range(9):
                    if not self.initial_fixed[row][c]:
                        self.entries[row][c].config(bg="#c8e6c9")  # light green
            else:
                # Fila incorrecta → rojo suave en celdas no fijas
                for c in range(9):
                    if not self.initial_fixed[row][c]:
                        self.entries[row][c].config(bg="#ffcdd2")  # light red
        else:
            # Row not full -> reset color of editable cells to white
            for c in range(9):
                if not self.initial_fixed[row][c]:
                    self.entries[row][c].config(bg="white")
                    
        # ------------------------------------------------------------------------- #
        # ---------- Opción 2: verificar automáticamente TODO el tablero ---------- #
        # ------------------------------------------------------------------------- #
        
        if all(board[r][c] != 0 for r in range(9) for c in range(9)):
            self.check_solution()

    # -------------------------------------------------------- #
    # ------------------ Checking & solving ------------------ #
    # -------------------------------------------------------- #
    
    def check_solution(self) -> None:
        """
        Validate the current grid.

        Checks:
        - All cells are filled.
        - Sudoku rules are respected (rows, columns, blocks).
        """
        board = self._get_current_board()

        # Check if any cell is empty
        if any(board[r][c] == 0 for r in range(9) for c in range(9)):
            messagebox.showwarning("Incomplete", "The grid is not completely filled.")
            return

        if self._is_board_valid(board):
            messagebox.showinfo("Success", "Congratulations! The solution is valid.")
            self.info_label.config(text="Valid solution!", fg="green")
        else:
            messagebox.showerror("Error", "The solution is not valid. Check your entries.")
            self.info_label.config(text="Invalid solution. Try again.", fg="red")

    def _is_board_valid(self, board: Board) -> bool:
        """Check if the whole board satisfies Sudoku rules."""
        # Check rows
        for r in range(9):
            if not self._is_unit_valid(board[r]):
                return False

        # Check columns
        for c in range(9):
            col = [board[r][c] for r in range(9)]
            if not self._is_unit_valid(col):
                return False

        # Check 3x3 blocks
        for br in range(3):
            for bc in range(3):
                block = []
                for r in range(br * 3, br * 3 + 3):
                    for c in range(bc * 3, bc * 3 + 3):
                        block.append(board[r][c])
                if not self._is_unit_valid(block):
                    return False

        return True

    @staticmethod
    def _is_unit_valid(unit: List[int]) -> bool:
        """
        Check if a row/column/block contains numbers 1-9 without repetition.
        """
        nums = [n for n in unit if n != 0]
        return len(nums) == len(set(nums)) and all(1 <= n <= 9 for n in nums)

    def solve_puzzle(self) -> None:
        """Attempt to solve the current puzzle and display the solution."""
        board = self._get_current_board()
        if self._solve_backtracking(board):
            # Show solved board
            for r in range(9):
                for c in range(9):
                    self.board_vars[r][c].set(str(board[r][c]))
                    self.entries[r][c].config(
                        state="disabled",
                        disabledforeground="darkgreen"
                    )
            self.info_label.config(text="Puzzle solved.", fg="green")
        else:
            messagebox.showerror("Error", "This puzzle has no solution.")
            self.info_label.config(text="No solution found.", fg="red")

    def _solve_backtracking(self, board: Board) -> bool:
        """Classic backtracking solver for Sudoku."""
        empty = self.generator._find_empty(board)
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.generator._is_valid(board, row, col, num):
                board[row][col] = num
                if self._solve_backtracking(board):
                    return True
                board[row][col] = 0
        return False


def main() -> None:
    """Entry point: create the Tk root window and run the Sudoku game."""
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
