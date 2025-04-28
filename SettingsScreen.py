import tkinter as tk
from Screen import Screen
import json
from tkinter import messagebox
import AppManager


class SettingsScreen(Screen):
    """The settings screen of the application.

    Attributes:
        GoL (AppManager): The AppManager object that manages the application.
        back_button (Button): The button to return to the game screen.
        alive_color_var (StringVar): The variable to store the selected alive cell color.
        alive_color_dropdown (OptionMenu): The dropdown to select the alive cell color.
        dead_color_var (StringVar): The variable to store the selected dead cell color.
        dead_color_dropdown (OptionMenu): The dropdown to select the dead cell color.
        saved_grid_buttons (list): A list of buttons to load saved grids.
        delete_grid_buttons (list): A list of buttons to delete saved grids.
        predefined_patterns (Listbox): The listbox to show predefined patterns.
        grid_size_adjuster_rows (Entry): The entry widget to adjust the number of rows.
        grid_size_adjuster_cols (Entry): The entry widget to adjust the number of columns.
        apply_button (Button): The button to apply the grid size.
        MAX_ROWS (int): The maximum number of rows allowed.
        MAX_COLS (int): The maximum number of columns allowed.
    """
    def __init__(self, GoL):
        """Initialize the settings screen.

        Args:
            GoL (AppManager): The AppManager object that manages the application.
        """
        super().__init__(GoL)

        # Set the background of the root to pink
        self.GoL.root.configure(bg="pink")
        self.frame.configure(bg="pink")

        # Create a frame for the back button and settings title label
        top_frame = tk.Frame(self.frame, bg="pink")
        top_frame.pack(side="top", fill="x", pady=10, anchor="center")

        # Configure the grid columns to have appropriate weights
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=3)
        top_frame.grid_columnconfigure(2, weight=2)

        # Back button aligned to the left
        self.back_button = tk.Button(top_frame, text="Back to Game", command=self.back_to_game, bg="pink")
        self.back_button.grid(row=0, column=0, padx=10, sticky="w")

        # Settings label centered
        settings_label = tk.Label(top_frame, text="Settings", bg="pink", font=("Arial", 14, "bold"))
        settings_label.grid(row=0, column=1, sticky="ew")

        # Create a frame for the rules section with frame
        rules_frame = tk.Frame(self.frame, bg="pink", bd=2, relief="groove", padx=10, pady=10)
        rules_frame.pack(side="top", fill="x", pady=10, anchor="center")

        # Create a label to explain the rules of the game
        rules_label = tk.Label(rules_frame, text="Rules:\n"
                                                 "1. Underpopulation: "
                                                 "Any live cell with fewer than two live neighbors dies.\n"
                                                 "2. Survival: "
                                                 "Any live cell with two or three live neighbors "
                                                 "survives to the next generation.\n"
                                                 "3. Overpopulation: "
                                                 "Any live cell with more than three live neighbors dies.\n"
                                                 "4. Reproduction: "
                                                 "Any dead cell with exactly three live neighbors becomes a live cell.",
                               bg="pink")
        rules_label.pack(side="top", pady=10)

        # Create a frame for the color scheme section
        color_scheme_frame = tk.Frame(self.frame, bg="pink")
        color_scheme_frame.pack(side="top", fill="x", pady=10, anchor="center")

        # Create a dropdown for alive cell color
        alive_color_label = tk.Label(color_scheme_frame, text="Alive Cell Color:", bg="pink")
        alive_color_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.alive_color_var = tk.StringVar(value="Black")  # Default alive cell color
        self.alive_color_dropdown = tk.OptionMenu(color_scheme_frame, self.alive_color_var,
                                                  "Black", "Red", "Orange", "Green", "Blue", "Purple",
                                                  command=self.apply_color_scheme)
        self.alive_color_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Create a dropdown for dead cell color
        dead_color_label = tk.Label(color_scheme_frame, text="Dead Cell Color:", bg="pink")
        dead_color_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.dead_color_var = tk.StringVar(value="White")  # Default dead cell color
        self.dead_color_dropdown = tk.OptionMenu(color_scheme_frame, self.dead_color_var,
                                                 "White", "Black", "Yellow", "Cyan", "Magenta",
                                                 command=self.apply_color_scheme)
        self.dead_color_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Create a frame for the load previous grid section
        load_frame = tk.Frame(self.frame, bg="pink")
        load_frame.pack(side="top", fill="x", pady=10, anchor="center")

        # Create a load previous grid section
        load_label = tk.Label(load_frame, text="Load Previous Grid:", bg="pink")
        load_label.grid(row=0, column=0, columnspan=5, padx=10, pady=5)
        # Create buttons for saved grids
        self.saved_grid_buttons = []
        for n in range(5):
            button = tk.Button(load_frame, text=f"Grid {n + 1}",
                               command=lambda n=n: self.load_grid(n), bg="pink")
            button.grid(row=1, column=n, padx=10, pady=5)
            self.saved_grid_buttons.append(button)

        # Create a delete button for each saved grid
        self.delete_grid_buttons = []
        for n in range(5):
            button = tk.Button(load_frame, text=f"Delete {n + 1}",
                               command=lambda n=n: self.delete_grid(n), bg="pink")
            button.grid(row=2, column=n, padx=10, pady=5)
            self.delete_grid_buttons.append(button)

        # Create a frame for the predefined patterns section
        patterns_frame = tk.Frame(self.frame, bg="pink")
        patterns_frame.pack(side="top", fill="x", pady=10, anchor="center")

        # Create a predefined patterns section
        patterns_label = tk.Label(patterns_frame, text="Predefined Patterns:", bg="pink")
        patterns_label.pack(side="left", padx=10)
        self.predefined_patterns = tk.Listbox(patterns_frame, height=5, width=20)
        self.predefined_patterns.pack(side="left", padx=10)

        # Add predefined patterns to the listbox
        predefined_patterns = ["Glider", "Blinker", "Toad", "Beacon", "Pulsar"]
        for pattern in predefined_patterns:
            self.predefined_patterns.insert(tk.END, pattern)

        # Create a button to load the selected pattern
        load_pattern_button = tk.Button(patterns_frame, text="Load Pattern",
                                        command=self.load_selected_pattern, bg="pink")
        load_pattern_button.pack(side="left", padx=10)

        # Create a frame for the grid size adjuster
        grid_size_frame = tk.Frame(self.frame, bg="pink")
        grid_size_frame.pack(side="top", fill="x", pady=10, anchor="center")

        # Create a grid size adjuster
        grid_size_label = tk.Label(grid_size_frame, text="Grid Size:", bg="pink")
        grid_size_label.pack(side="left", padx=10)
        # Create two entry widgets for the user to input the number of rows and columns
        self.grid_size_adjuster_rows = tk.Entry(grid_size_frame)
        self.grid_size_adjuster_rows.pack(side="left", padx=10)
        tk.Label(grid_size_frame, text="x", bg="pink").pack(side="left")  # Label to separate the rows and columns (x)
        self.grid_size_adjuster_cols = tk.Entry(grid_size_frame)
        self.grid_size_adjuster_cols.pack(side="left", padx=10)

        # Create a button to apply the grid size
        self.apply_button = tk.Button(grid_size_frame, text="Apply", command=self.adjust_grid_size, bg="pink")
        self.apply_button.pack(side="left", padx=10)

        # Max num of rows and cols
        self.MAX_ROWS = 50
        self.MAX_COLS = 50

    def load_grid(self, index):
        """Load a saved grid.

        Args:
            index (int): The index of the saved grid to load.
        """
        try:
            with open(AppManager.get_path("saved_grids.json")) as file:
                saved_grids = json.load(file)
            if index < len(saved_grids):
                saved_grid = saved_grids[index]
                rows = len(saved_grid)
                cols = len(saved_grid[0])
                self.GoL.grid_manager.resize_grid(rows, cols)
                self.GoL.grid_manager.grid = saved_grid
                self.GoL.grid_renderer.update_cell_size()
                self.GoL.grid_renderer.render_grid()
                self.GoL.game_screen.adjust_offsets()  # Adjust the offsets to center the grid
                messagebox.showinfo("Load Grid", f"Grid {index + 1} has been loaded successfully.")
            else:
                messagebox.showerror("Load Grid", "Grid index out of range.")
        except (FileNotFoundError, json.JSONDecodeError, IndexError):
            messagebox.showerror("Load Grid", "Failed to load the grid.")

    def delete_grid(self, index):
        """Delete a saved grid.

        Args:
            index (int): The index of the saved grid to delete.
        """
        try:
            with open(AppManager.get_path("saved_grids.json"), "r") as file:
                saved_grids = json.load(file)
            if index < len(saved_grids):
                if not saved_grids[index]:
                    messagebox.showerror("Delete Grid", f"Grid {index + 1} is already empty.")
                    return
                del saved_grids[index]
                with open("saved_grids.json", "w") as file:
                    json.dump(saved_grids, file, indent=4)
                messagebox.showinfo("Delete Grid", f"Grid {index + 1} has been deleted.")
            else:
                messagebox.showerror("Delete Grid", f"Grid {index + 1} does not exist.")
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Delete Grid", "Failed to delete the grid.")

    def back_to_game(self):
        """Return to the game screen."""
        self.GoL.show_screen("game")

    def adjust_grid_size(self):
        """Adjust the grid size based on user input."""
        try:
            # Get the rows and columns from the grid size adjuster
            rows = int(self.grid_size_adjuster_rows.get())
            cols = int(self.grid_size_adjuster_cols.get())

            # Check if the input exceeds the maximum values
            if rows > self.MAX_ROWS or cols > self.MAX_COLS:
                messagebox.showerror("Adjust Grid Size",
                                     f"Grid size cannot exceed {self.MAX_ROWS}x{self.MAX_COLS}.")
                return

            # Resize the grid based on the user input
            self.GoL.grid_manager.resize_grid(rows, cols)
            # Update the cell size and render the grid
            self.GoL.grid_renderer.update_cell_size()
            self.GoL.grid_renderer.render_grid()
            # Add message to confirm the grid size has been adjusted
            messagebox.showinfo("Adjust Grid Size", f"Grid size has been adjusted to {rows}x{cols}.")
        except ValueError:
            messagebox.showerror("Adjust Grid Size", "Please enter valid integer values for rows and columns.")

    def apply_color_scheme(self, event):
        """Apply the selected color scheme.

        Args:
            event (tk.Event): The event object containing the selected color scheme.
        """
        # Get the selected color scheme from the dropdown
        alive_color = self.alive_color_var.get()
        dead_color = self.dead_color_var.get()
        # Apply the selected color scheme to the grid renderer
        self.GoL.grid_renderer.alive_cell_color = alive_color
        self.GoL.grid_renderer.dead_cell_color = dead_color
        # Update the grid renderer to reflect the new color scheme
        self.GoL.grid_renderer.render_grid()

    def load_selected_pattern(self):
        """Load the selected predefined pattern."""
        selected_pattern = self.predefined_patterns.get(tk.ACTIVE)
        if selected_pattern:
            # Get the current grid dimensions
            current_rows = self.GoL.grid_manager.rows
            current_cols = self.GoL.grid_manager.cols

            # Get the pattern dimensions from GridManager
            pattern = self.GoL.grid_manager.patterns[selected_pattern]
            pattern_rows = len(pattern)
            pattern_cols = len(pattern[0])

            # Check if the pattern fits in the current grid
            if pattern_rows > current_rows or pattern_cols > current_cols:
                messagebox.showerror("Load Pattern", f"{selected_pattern} pattern is too large for the current grid.")
                return

            # Load the selected pattern into the grid manager
            self.GoL.grid_manager.load_pattern(selected_pattern)
            # Render the grid with the new pattern
            self.GoL.grid_renderer.render_grid()
            # Show a message to confirm the pattern has been loaded
            messagebox.showinfo("Load Pattern", f"{selected_pattern} pattern has been loaded.")
        else:
            messagebox.showwarning("Load Pattern", "Please select a pattern to load.")
