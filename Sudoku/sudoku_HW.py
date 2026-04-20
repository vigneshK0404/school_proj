import random


# =======================
# CORE GAME CLASS
# =======================
class SudokuGame:
    """
    Main game controller class
    Handles puzzle generation, solving, and game state management
    """

    # Difficulty configuration (empty cells percentage)
    DIFFICULTY_MAP = {
        'easy': 0.3,  # 30% cells removed
        'medium': 0.5,  # 50% cells removed
        'hard': 0.7  # 70% cells removed
    }

    def __init__(self, difficulty='medium', original=None, solution=None, current=None):
        self.difficulty = difficulty
        sel.foriginal = original
        self.solution = solution
        self.current_grid = current
        """Initialize game state - new or loaded"""
        # [Implementation unchanged]

    # =======================
    # PUZZLE GENERATION
    # =======================
    def generate_sudoku(self):
        
        grid = [[0]*9]*9
        grid = self.fill_box(grid,0,0)
        grid = self.fill_box(grid,3,3)
        grid = self.fill_box(grid,6,6)

        
        self.solve_sudoku(grid)
        self.solution = grid

        ratio = self.DIFFICULTY_MAP[self.difficulty]*81
        removeList = random.sample(range(0,81),ratio)


        for i in removeList:
            r = int(i//9)
            c = int(i%9)
            grid[r][c] = 0
        
    
        self.current_grid = grid

        return
        


    def fill_box(self, grid, row, col):
        gridNums = random.shuffle([i for i in range(1,10)])
        for r in range(row,row+3):
            for c in range(col,col+3):
                grid[r][c] = gridNums[r+(c%3)]
        return grid

    # =======================
    # SOLVING ALGORITHMS
    # =======================

    def solve_sudoku(self, grid):
        empty = self.find_empty_cell(grid)
        if not empty:
            return True
        row, col = empty

        for num in random.sample(range(1, 10), 9):
            if self.is_valid_move_in_grid(grid, row, col, num):
                grid[row][col] = num
                if self.solve_sudoku(grid):
                    return True
                grid[row][col] = 0
        return False

    # =======================
    # GAME STATE MANAGEMENT
    # =======================
    def find_empty_cell(self, grid=None):
       for r in range(len(grid)):
           for c in range(len(grid[r])):
               if grid[r][c] == 0:                 
                   return r,c

        return False



    def is_valid_move_in_grid(self, grid, row, col, num):
        
        if num in grid[row]:
            return False

        for r in grid:
            if r[col] == num :
                return False

        row_start = 3*int(row//3)
        col_start = 3*int(col//3)

        row_end = row_start + 3
        col_end = col_start + 3

        for r in range(row_start,row_end):
            for c in range(col_start,col_end):
                if grid[r][c] == num:
                    return False

        return True

       
    def is_valid_move(self, row, col, num):
        return self.is_valid_move_in_grid(self.current_grid, row, col, num)

    def is_complete(self):
        return self.current_grid == self.solution

    # =======================
    # VISUALIZATION & IO
    # =======================
    def print_grid(self):
        print("+---+---+---+---+---+---+---+---+---+---+")
        for r in self.current_grid:
            print("|",end=" ")
            for c in r:
                print(c,end="   ")
            print("|",end="\n")
        print("+---+---+---+---+---+---+---+---+---+---+")


    def save_progress(self, filename):

        with open(filename,"w") as f:
            for r in self.current_grid:
                for c in r:
                    f.write('%s\n' %c)

        print(f"Game Saved Successfully at {filename}")
        

    @classmethod
    def load_progress(cls, filename):
        grid = [[0]*9]*9

        with open(filename) as f:
            rawList = [a.rstrip() for a in f.readlines()]

        for i in range(len(rawList)):
            row = int(i//9)
            col = int(i%9)
            grid[row][col] = rawList[i]

        cls.current_grid = grid

        """Load game state from file"""
        """
        may add try-except
        """



# =======================
# GAME INTERFACE
# =======================
def play_sudoku():
    print("Welcome to Sudoku!")
    print("Choose an option:")
    print("1. New Game")
    print("2. Load Game")
    choice = input("Enter 1 or 2: ").strip()

    game = None
    if choice == '1':
        difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
        if difficulty not in SudokuGame.DIFFICULTY_MAP:
            print("Invalid difficulty. Using medium.")
            difficulty = 'medium'
        game = SudokuGame(difficulty)
    elif choice == '2':
        filename = input("Enter filename to load: ").strip()
        game = SudokuGame.load_progress(filename)
        if not game:
            print("Starting new medium game instead.")
            game = SudokuGame('medium')
    else:
        print("Invalid choice. Starting new medium game.")
        game = SudokuGame('medium')

    while True:
        game.print_grid()

        if game.is_complete():

            print("\nPuzzle complete.")
            break

        user_input = input("\nEnter move (row col num), 'save', 'load', or 'quit': ").strip().lower()

        if user_input == 'quit':
            print("Thanks for playing!")
            break
        elif user_input == 'save':
            filename = input("Enter filename to save: ").strip()
            game.save_progress(filename)
        elif user_input == 'load':
            filename = input("Enter filename to load: ").strip()
            loaded_game = SudokuGame.load_progress(filename)
            if loaded_game:
                game = loaded_game
                print("Game loaded!")
            else:
                print("Loading failed. Continuing current game.")
        else:
            try:
                parts = user_input.split()
                if len(parts) != 3:
                    raise ValueError("Enter 3 values separated by spaces")
                row = int(parts[0]) - 1
                col = int(parts[1]) - 1
                num = int(parts[2])

                if not (0 <= row <= 8 and 0 <= col <= 8 and 1 <= num <= 9):
                    raise ValueError("Values must be between 1-9")

                if game.original_puzzle[row][col] != 0:
                    print("Cannot modify original puzzle numbers!")
                    continue

                if not game.is_valid_move(row, col, num):
                    print("Invalid move! Conflict detected.")
                    continue

                game.current_grid[row][col] = num
                print("Move accepted!")

            except ValueError as e:
                print(f"Invalid input: {e}")


if __name__ == "__main__":
    play_sudoku()

