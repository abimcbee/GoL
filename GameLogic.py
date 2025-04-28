import tkinter as tk
from GridManager import GridManager


class GameLogic:
    """Handles the rules and updates for Conway’s Game of Life.

    Attributes:
        grid_manager (GridManager): Managers the grid state and logic.
        wrap (bool): Whether to wrap around the edges of the grid.
    """
    def __init__(self, grid_manager):
        """Initialize the game logic with a grid manager.

        Args:
            grid_manager (GridManager): The grid manager instance.
        """
        self.grid_manager = grid_manager  # Stores the grid of cells
        self.wrap = False  # Whether to wrap around the edges of the grid

    def count_live_neighbors(self, row, col) -> int:
        """Counts the number of live (1) neighbors around a given cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            int: The number of live neighbors around the cell.
        """

        # Possible directions to check for neighbors (row_offset, col_offset)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Top row neighbors
            (0, -1), (0, 1),  # Left and right neighbors
            (1, -1), (1, 0), (1, 1)  # Bottom row neighbors
        ]

        live_count = 0  # Counter for live neighbors

        # Check each direction
        for dr, dc in directions:
            neighbor_row = row + dr
            neighbor_col = col + dc

            # Handle wrapping around the edges if enabled
            if self.wrap:
                neighbor_row %= self.grid_manager.rows
                neighbor_col %= self.grid_manager.cols
            else:
                # Skip out-of-bounds neighbors
                if neighbor_row < 0 or neighbor_row >= self.grid_manager.rows:
                    continue
                if neighbor_col < 0 or neighbor_col >= self.grid_manager.cols:
                    continue

            # If the neighbor is alive, count it
            if self.grid_manager.grid[neighbor_row][neighbor_col] == 1:
                live_count += 1

        return live_count

    def update_grid(self):
        """Applies Conway’s Game of Life rules to update the grid."""

        # Create a new grid with all dead cells (0)
        new_grid = [[0 for _ in range(self.grid_manager.cols)] for _ in range(self.grid_manager.rows)]

        # Loop through each cell in the grid
        for row in range(self.grid_manager.rows):
            for col in range(self.grid_manager.cols):
                live_neighbors = self.count_live_neighbors(row, col)  # Count live neighbors
                is_alive = self.grid_manager.grid[row][col] == 1  # Check if the cell is currently alive

                # Apply the rules of the game
                if is_alive:
                    # A live cell stays alive if it has 2 or 3 neighbors
                    if live_neighbors == 2 or live_neighbors == 3:
                        new_grid[row][col] = 1
                    # If not, it dies
                    else:
                        new_grid[row][col] = 0
                else:
                    # A dead cell becomes alive if it has exactly 3 neighbors
                    if live_neighbors == 3:
                        new_grid[row][col] = 1

        # Replace the old grid with the new one
        self.grid_manager.grid = new_grid
