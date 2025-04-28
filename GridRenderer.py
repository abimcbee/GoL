import tkinter as tk


class GridRenderer:
    """Class to render and resize the grid.

    Attributes:
        canvas (tk.Canvas): The canvas to draw on.
        grid_manager (GridManager): Manages the grid state and logic.
        x_offset (int): The x offset to center the grid.
        y_offset (int): The y offset to center the grid.
        grid_lines (bool): Flag to show or hide the grid lines.
        alive_cell_color (str): The color of the alive cells.
        dead_cell_color (str): The color of the dead cells.
    """
    def __init__(self, canvas, grid_manager):
        """Initialize the GridRenderer.

        Args:
            canvas (tk.Canvas): The canvas to draw on.
            grid_manager (GridManager): Manages the grid state and logic.
        """
        self.canvas = canvas  # the canvas to draw on
        self.grid_manager = grid_manager  # the grid manager
        self.x_offset = 0  # the x offset to center the grid
        self.y_offset = 0  # the y offset to center the grid
        self.grid_lines = True  # flag to show or hide the grid lines
        self.canvas.bind("<Configure>", self.on_resize)  # bind the resize event to the on_resize function
        self.alive_cell_color = "black"  # the default color of the alive cells
        self.dead_cell_color = "white"  # the default color of the dead cells

    def on_resize(self, event):
        """Called when the canvas is resized.

        Args:
            event (tk.Event): The event object containing the resize information.
        """
        self.update_cell_size()
        self.render_grid()

    def update_cell_size(self):
        """Update the cell size based on the canvas size"""
        canvas_width = self.canvas.winfo_width()  # get the width of the canvas
        canvas_height = self.canvas.winfo_height()  # get the height of the canvas
        # set the cell size to the minimum of the width and height divided by the number of rows and columns
        self.grid_manager.cell_size = min(canvas_width // self.grid_manager.cols, canvas_height // self.grid_manager.rows)
        self.x_offset = (canvas_width - self.grid_manager.cell_size * self.grid_manager.cols) // 2
        self.y_offset = (canvas_height - self.grid_manager.cell_size * self.grid_manager.rows) // 2

    def render_grid(self):
        """Render the grid"""
        self.canvas.delete("grid_line")  # delete the old grid lines
        for i in range(self.grid_manager.rows):  # loop through the rows
            for j in range(self.grid_manager.cols):  # loop through the columns
                x0 = j * self.grid_manager.cell_size + self.x_offset  # calculate the x coordinate of the cell
                y0 = i * self.grid_manager.cell_size + self.y_offset  # calculate the y coordinate of the cell
                x1 = x0 + self.grid_manager.cell_size  # calculate the x coordinate of the right side of the cell
                y1 = y0 + self.grid_manager.cell_size  # calculate the y coordinate of the bottom side of the cell

                # fill the cell with the appropriate color
                if self.grid_manager.grid[i][j] == 1:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.alive_cell_color, outline="", tags="grid_line")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.dead_cell_color, outline="", tags="grid_line")

                # draw the grid lines if the flag is set
                if self.grid_lines:
                    self.canvas.create_line(x0, y0, x1, y0, fill="gray", tags="grid_line")
                    self.canvas.create_line(x0, y0, x0, y1, fill="gray", tags="grid_line")
