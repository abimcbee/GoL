class GridManager:
    """Class to manage the grid.

    Attributes:
        grid (list): 2D list to store the grid.
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        cell_size (int): Size of each cell in the grid.
        patterns (dict): Dictionary containing predefined patterns.
    """
    def __init__(self, rows, cols):
        """Initialize the grid manager.

        Args:
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
        """
        # create a 2D list to store the grid
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.cell_size = 10  # default cell size

        self.patterns = {
            "Glider": [
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ],
            "Blinker": [
                [1, 1, 1]
            ],
            "Toad": [
                [0, 1, 1, 1],
                [1, 1, 0, 0]
            ],
            "Beacon": [
                [1, 1, 0, 0],
                [1, 1, 0, 0],
                [0, 0, 1, 1],
                [0, 0, 1, 1]
            ],
            "Pulsar": [
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [1, 1, 1, 0, 1, 1, 1],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0]
            ]
        }

    def resize_grid(self, rows, cols):
        """Resize the grid based on user input.

        Args:
            rows (int): New number of rows in the grid.
            cols (int): New number of columns in the grid.
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def count_live_cells(self) -> int:
        """Counts the number of live cells in the grid.

        Returns:
            int: Number of live cells in the grid.
        """
        sum_of_alive_cells = 0
        for row in self.grid:
            for cell in row:
                if cell == 1:
                    sum_of_alive_cells += 1
        return sum_of_alive_cells

    def count_dead_cells(self) -> int:
        """Counts the number of dead cells in the grid.

        Returns:
            int: Number of dead cells in the grid.
        """
        sum_of_dead_cells = 0
        for row in self.grid:
            for cell in row:
                if cell == 0:
                    sum_of_dead_cells += 1
        return sum_of_dead_cells

    def load_pattern(self, pattern_name):
        """Load a pattern into the grid.

        Args:
            pattern_name (str): Name of the pattern to load.

        Raises:
            ValueError: If the pattern is not found.
        """
        if pattern_name in self.patterns:
            pattern = self.patterns[pattern_name]
            pattern_rows = len(pattern)
            pattern_cols = len(pattern[0])

            # calculate the starting position
            start_row = (self.rows - pattern_rows) // 2
            start_col = (self.cols - pattern_cols) // 2

            for n in range(len(pattern)):
                for m in range(len(pattern[n])):
                    if (start_row + n < self.rows) and (start_col + m < self.cols):
                        self.grid[start_row + n][start_col + m] = pattern[n][m]
        else:
            raise ValueError(f"Pattern '{pattern_name}' not found.")
