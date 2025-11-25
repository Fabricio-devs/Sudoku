# 🧩 Sudoku Game (Tkinter)

A fully interactive **Sudoku game** built with Python and Tkinter.\
This project includes puzzle generation, solving, auto-checking, and a
clean GUI layout.\
It's perfect as a portfolio project to demonstrate problem-solving,
algorithms, and GUI development.

## 🚀 Features

### 🎮 Gameplay

-   Automatically generated Sudoku puzzles\
-   Adjustable difficulty\
-   Manual cell input with validation (only digits 1--9)\
-   Buttons: **Check**, **Solve**, **Clear**, **New Game**

### 💡 Smart Auto-Checking  |||

-   **Row Auto-Check:**\
    When a row is fully filled, it is automatically validated.
    -   Green = valid row\
    -   Red = invalid row
-   **Full Board Auto-Check:**\
    When all 81 cells are filled, the entire Sudoku is automatically
    validated.

### 🧠 Solver

-   Complete Sudoku backtracking algorithm\
-   "Solve" button shows a correct solution instantly

### 🖥️ GUI

-   Clean Tkinter layout\
-   3×3 grid separation\
-   Fixed puzzle cells appear in blue\
-   Editable cells highlight depending on correctness

## 🛠️ Technologies Used

-   Python 3.x\
-   Tkinter (built-in GUI library)\
-   Random\
-   Backtracking algorithm

## 📦 Installation

1.  Verify Python 3 is installed:

    ``` bash
    python --version
    ```

2.  Save the project structure:

        sudoku/
        ├── main.py
        └── README.md

3.  Run the game:

    ``` bash
    python main.py
    ```

## 🧠 How It Works

### Puzzle Generation

A valid completed Sudoku board is generated using backtracking.\
Cells are then removed randomly to create a playable puzzle.

### Auto Row Checking

When a row is complete: - Checks for duplicate numbers\
- Ensures all numbers 1--9 appear\
- Colors the row accordingly

### Auto Full-Board Check

If no empty cells remain: - Entire board is validated automatically

### Solver

Uses a recursive backtracking algorithm to compute a valid solution.

## 🎯 Purpose

Great for portfolio demonstration of: - GUI design\
- Algorithmic thinking\
- Validation logic\
- Python OOP

## 📝 License

Free to use and modify.
