import json
import tkinter as tk
from Screen import Screen
from GridRenderer import GridRenderer
from GameLogic import GameLogic
from tkinter import messagebox
import tkinter.simpledialog
import AppManager


class GameScreen(Screen):
    """The game screen of the application.

    Attributes:
        GoL (GameOfLife): The GameOfLife instance that manages the application.
        canvas (tk.Canvas): The canvas to draw the grid on.
        toggled_cells (set): A set to keep track of the cells that have been toggled.
        start_button (tk.Button): The button to start the simulation.
        stop_button (tk.Button): The button to stop the simulation.
        reset_button (tk.Button): The button to reset the grid.
        speed_slider (tk.Scale): The slider to control the speed of the simulation.
        generation_label (tk.Label): The label to display the generation number.
        increase_generation_button (tk.Button): The button to increase the generation.
        decrease_generation_button (tk.Button): The button to decrease the generation.
        alive_label (tk.Label): The label to display the number of alive cells.
        dead_label (tk.Label): The label to display the number of dead cells.
        wrapping_button (tk.Button): The button to toggle wrapping.
        grid_lines_button (tk.Button): The button to toggle grid lines.
        save_button (tk.Button): The button to save the grid.
        settings_button (tk.Button): The button to go to the settings screen.
        zoom_in_button (tk.Button): The button to zoom in on the grid.
        zoom_out_button (tk.Button): The button to zoom out on the grid.
        grid (list): The 2D list representing the grid.
        wrapping (bool): A flag to indicate if the grid is wrapping.
        grid_history (list): A list to store the history of the grid.
        grid_manager (GridManager): The grid manager to manage the grid.
        grid_renderer (GridRenderer): The grid renderer to render the grid.
        game_logic (GameLogic): The game logic to update the grid.
        running (bool): A flag to indicate if the simulation is running.
        update_interval (int): The interval between updates in milliseconds.
        initial_grid (list): The initial state of the grid.
    """
    def __init__(self, GoL):
        """Initialize the GameScreen.

        Args:
            GoL (GameOfLife): The GameOfLife instance that manages the application.
        """
        super().__init__(GoL)

        # set the background of the root to pink
        self.GoL.root.configure(bg="pink")
        self.frame.configure(bg="pink")

        # create a frame for the controls at the top of the screen
        top_controls_frame = tk.Frame(self.frame, bg="pink")
        top_controls_frame.pack(side="top", fill="x", pady=10)

        # create a canvas for the grid
        self.canvas = tk.Canvas(self.frame, bg="pink", highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand=True, pady=10)

        # Initialize a set to keep track of the cell states
        self.toggled_cells = set()

        # bind the mouse events to the canvas
        self.canvas.bind("<Button-1>", self.start_drag)  # start dragging
        self.canvas.bind("<B1-Motion>", self.drag_toggle_cell)  # click and drag
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)  # stop dragging

        # create a frame for the controls at the bottom of the screen
        bottom_controls_frame = tk.Frame(self.frame, bg="pink")
        bottom_controls_frame.pack(side="bottom", fill="x", pady=10)

        # configure grid columns to have equal weight
        for n in range(5):
            bottom_controls_frame.grid_columnconfigure(n, weight=1)

        # create the start button
        self.start_button = tk.Button(bottom_controls_frame, text="Start", command=self.start_simulation, bg="pink")
        self.start_button.grid(row=0, column=0, padx=10)

        # create the stop button
        self.stop_button = tk.Button(bottom_controls_frame, text="Stop", command=self.stop_simulation, bg="pink")
        self.stop_button.grid(row=1, column=0, padx=10)

        # create the reset button
        self.reset_button = tk.Button(bottom_controls_frame, text="Reset", command=self.reset_grid, bg="pink")
        self.reset_button.grid(row=3, column=0, padx=10)

        # create the speed slider
        self.speed_slider = tk.Scale(bottom_controls_frame, from_=1, to=10, orient="horizontal", label="Speed: ",
                                     command=self.update_speed, bg="pink", highlightthickness=1, highlightcolor="black",
                                     troughcolor="light pink", highlightbackground="black")
        self.speed_slider.set(5)
        self.speed_slider.grid(row=0, column=1, padx=10)

        # create a generation label
        self.generation_label = tk.Label(bottom_controls_frame, text="Generation: 0", bg="pink")
        self.generation_label.grid(row=0, column=2, padx=10)

        # create a button to increase the generation
        self.increase_generation_button = tk.Button(bottom_controls_frame, text="Next Generation",
                                           command=self.update_grid, bg="pink")
        self.increase_generation_button.grid(row=1, column=2, padx=10)

        # create a button to decrease the generation
        self.decrease_generation_button = tk.Button(bottom_controls_frame, text="Previous Generation",
                                           command=self.previous_generation, bg="pink")
        self.decrease_generation_button.grid(row=3, column=2, padx=10)

        # create a label for number of alive cells
        self.alive_label = tk.Label(bottom_controls_frame, text="Alive Cells: 0", bg="pink")
        self.alive_label.grid(row=2, column=1, padx=10)

        # create a label for number of dead cells
        self.dead_label = tk.Label(bottom_controls_frame, text="Dead Cells: 0", bg="pink")
        self.dead_label.grid(row=3, column=1, padx=10)

        # create the wrapping button
        self.wrapping_button = tk.Button(bottom_controls_frame, text="Wrapping: Off",
                                         command=self.toggle_wrapping, bg="pink")
        self.wrapping_button.grid(row=0, column=3, padx=10)

        # create the grid lines button
        self.grid_lines_button = tk.Button(bottom_controls_frame, text="Grid Lines: On",
                                           command=self.toggle_grid_lines, bg="pink")
        self.grid_lines_button.grid(row=1, column=3, padx=10)

        # create the save button
        self.save_button = tk.Button(bottom_controls_frame, text="Save", command=self.save_grid, bg="pink")
        self.save_button.grid(row=0, column=4, padx=10)

        # create the settings button
        self.settings_button = tk.Button(top_controls_frame, text="Settings",
                                         command=lambda: GoL.show_screen("settings"), bg="pink")
        self.settings_button.pack(side="right", padx=10)

        # create the zoom out button
        self.zoom_out_button = tk.Button(top_controls_frame, text="Zoom Out", command=self.zoom_out, bg="pink")
        self.zoom_out_button.pack(side="right", padx=10)

        # create the zoom in button
        self.zoom_in_button = tk.Button(top_controls_frame, text="Zoom In", command=self.zoom_in, bg="pink")
        self.zoom_in_button.pack(side="right", padx=10)

        # Grid info
        self.grid = [[]]
        self.wrapping = False
        self.grid_history = []

        # use the grid manager from the AppManager
        self.grid_manager = GoL.grid_manager

        # render the grid
        self.grid_renderer = GridRenderer(self.canvas, self.grid_manager)
        self.grid_renderer.render_grid()

        # set the grid renderer in AppManager
        GoL.grid_renderer = self.grid_renderer

        # create the game logic
        self.game_logic = GameLogic(self.grid_manager)

        # flag to check if the game is running
        self.running = False
        self.update_interval = 1000 // self.speed_slider.get()

        # update the cell counts
        self.update_cell_counts()

        # Save the initial grid state
        self.initial_grid = [row[:] for row in self.grid_manager.grid]

    def start_drag(self, event):
        """Start drag operation and toggle the first cell.

        Args:
            event (tk.Event): The event object containing information about the mouse click.
        """
        self.toggled_cells.clear()  # Clear the set of toggled cells
        self.toggle_cell(event)  # Toggle the first cell

    def drag_toggle_cell(self, event):
        """Toggle the cells while dragging the mouse.

        Args:
            event (tk.Event): The event object containing information about the mouse movement.
        """
        # get the row and column of the cell
        col = (event.x - self.grid_renderer.x_offset) // self.grid_manager.cell_size
        row = (event.y - self.grid_renderer.y_offset) // self.grid_manager.cell_size
        if (row, col) not in self.toggled_cells:  # check if the cell has already been toggled
            self.toggled_cells.add((row, col))  # add the cell to the set of toggled cells
            self.toggle_cell(event)

    def stop_drag(self, event):
        """Stop the drag operation.

        Args:
            event (tk.Event): The event object containing information about the mouse release.
        """
        # Clear the set of toggled cells when the mouse is released
        self.toggled_cells.clear()

    def toggle_cell(self, event):
        """Toggle the state of the cell when clicked

        Args:
            event (tk.Event): The event object containing information about the mouse click.
        """
        # get the row and column of the cell
        col = (event.x - self.grid_renderer.x_offset) // self.grid_manager.cell_size
        row = (event.y - self.grid_renderer.y_offset) // self.grid_manager.cell_size

        # check if the row and column are within the grid bounds
        if 0 <= row < self.grid_manager.rows and 0 <= col < self.grid_manager.cols:
            # toggle the cell state
            if self.grid_manager.grid[row][col] == 1:
                self.grid_manager.grid[row][col] = 0
            else:
                self.grid_manager.grid[row][col] = 1

        # update the initial grid to reflect changes
        self.initial_grid = [row[:] for row in self.grid_manager.grid]

        self.grid_renderer.render_grid()  # render the grid
        self.update_cell_counts()  # update the cell counts

    def start_simulation(self):
        """Start the simulation"""
        if not self.running:  # check if the simulation is already running
            self.running = True  # set the running flag to true
            self.run_simulation()  # call the run_simulation function

    def run_simulation(self):
        """Run the simulation"""
        if self.running:  # check if the simulation is still running
            self.update_grid()  # update the grid
            # call the run_simulation function again after the update interval
            self.GoL.root.after(self.update_interval, self.run_simulation)

    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False

    def reset_grid(self):
        """Reset the grid to all dead cells"""
        self.grid_manager.grid = [[0 for _ in range(self.grid_manager.cols)] for _ in range(self.grid_manager.rows)]
        self.grid_renderer.render_grid()
        self.update_cell_counts()  # update the cell counts

    def update_speed(self, value):
        """Update the speed of the simulation

        Args:
            value (str): The value of the speed slider.
        """
        self.update_interval = 1000 // int(value)  # update the update interval based on the speed slider value
        if self.running:  # check if the simulation is running
            self.stop_simulation()  # stop the simulation
            self.start_simulation()  # start the simulation again with the new speed

    def toggle_wrapping(self):
        """Toggle the wrapping of the grid"""
        self.wrapping = not self.wrapping  # toggle the wrapping flag
        self.game_logic.wrap = self.wrapping  # update the game logic wrapping flag
        if self.wrapping:
            self.wrapping_button.config(text="Wrapping: On")
        else:
            self.wrapping_button.config(text="Wrapping: Off")
        self.grid_renderer.render_grid()  # render the grid
        self.update_cell_counts()  # update the cell counts

    def toggle_grid_lines(self):
        """Toggle the visibility of grid lines."""
        self.grid_renderer.grid_lines = not self.grid_renderer.grid_lines  # Toggle the flag
        self.grid_renderer.render_grid()  # Re-render the grid

        # Update button text
        if self.grid_renderer.grid_lines:
            self.grid_lines_button.config(text="Grid Lines: On")
        else:
            self.grid_lines_button.config(text="Grid Lines: Off")

    def zoom_in(self):
        """Zoom in on the grid"""
        self.grid_manager.cell_size += 1  # increase the cell size
        self.adjust_offsets()  # adjust the offsets to keep the zoom centered
        self.grid_renderer.render_grid()  # re-render the grid

    def zoom_out(self):
        """Zoom out on the grid"""
        if self.grid_manager.cell_size > 1:  # check if the cell size is greater than 1
            self.grid_manager.cell_size -= 1  # decrease the cell size
            self.adjust_offsets()  # adjust the offsets to keep the zoom centered
            self.grid_renderer.render_grid()  # re-render the grid

    def adjust_offsets(self):
        """Adjusts the offsets to keep the zoom centered"""
        canvas_width = self.canvas.winfo_width()  # get the width of the canvas
        canvas_height = self.canvas.winfo_height()  # get the height of the canvas
        grid_width = self.grid_manager.cols * self.grid_manager.cell_size  # calculate the width of the grid
        grid_height = self.grid_manager.rows * self.grid_manager.cell_size  # calculate the height of the grid

        # calculate the x offset
        self.grid_renderer.x_offset = (canvas_width - grid_width) // 2
        # calculate the y offset
        self.grid_renderer.y_offset = (canvas_height - grid_height) // 2

    def update_grid(self):
        """Update the grid"""
        self.grid_history.append(self.grid_manager.grid)  # append the current grid to the history
        self.game_logic.update_grid()  # update the grid based on the game logic
        self.grid_renderer.render_grid()  # render the grid
        self.update_cell_counts()  # update the cell counts
        self.generation_label.config(text=f"Generation: {len(self.grid_history)}")

    def update_cell_counts(self):
        """Update the cell counts"""
        self.alive_label.config(text=f"Alive Cells: {self.grid_manager.count_live_cells()}")
        self.dead_label.config(text=f"Dead Cells: {self.grid_manager.count_dead_cells()}")

    def previous_generation(self):
        """Go back to the previous generation"""
        if len(self.grid_history) > 0:  # check if there are previous generations
            self.grid_manager.grid = self.grid_history.pop()  # set the grid to the previous generation
            self.grid_renderer.render_grid()  # render the grid
            self.update_cell_counts()  # update the cell counts
            self.generation_label.config(text=f"Generation: {len(self.grid_history)}")

    def save_grid(self, filename="saved_grids.json"):
        """Save the initial state of the grid to a JSON file.

        Args:
            filename (str): The name of the file to save the grid to. Default is "saved_grids.json".
        """
        # Load existing saved grids if the file exists
        try:
            with open(AppManager.get_path(filename)) as file:
                saved_grids = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            saved_grids = []

        # Prompt the user to select a save slot
        slot = tkinter.simpledialog.askinteger("Save Grid", "Enter a slot number (1-5):", minvalue=1, maxvalue=5)
        if slot is None:
            return  # User cancelled the dialog

        # Adjust the slot to be zero-indexed
        slot -= 1

        # Check if the selected slot is not empty
        if slot < len(saved_grids) and saved_grids[slot]:
            overwrite = messagebox.askyesno("Save Grid", f"Slot {slot + 1} "
                                                         f"already contains a grid. Do you want to overwrite it?")
            if not overwrite:
                return  # User chose not to overwrite

        # Save the grid in the selected slot
        if slot < len(saved_grids):
            saved_grids[slot] = self.initial_grid
        else:
            # Add empty slots if necessary
            while len(saved_grids) <= slot:
                saved_grids.append([])
            saved_grids[slot] = self.initial_grid

        # Save the grids to the file
        with open(AppManager.get_path(filename), "w") as file:
            json.dump(saved_grids, file, indent=4)

        # Show a message to confirm the grid has been saved
        messagebox.showinfo("Save Grid", f"Grid saved successfully in slot {slot + 1}.")
