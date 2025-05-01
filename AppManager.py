import tkinter as tk
from HomeScreen import HomeScreen
from GameScreen import GameScreen
from SettingsScreen import SettingsScreen
from GridManager import GridManager
from Screen import Screen
import os
import sys


# used for packaging with pyinstaller
def get_path(filename):
    if getattr(sys, 'frozen', False):  # Check if the application is frozen (packaged)
        base_path = sys._MEIPASS  # Get the base path of the frozen application
    else:
        base_path = os.path.dirname(__file__)  # Get the directory of the script
    return os.path.join(base_path, filename)  # Join the base path with the filename


class AppManager:
    """The main application manager for Conway's Game of Life.

    Attributes:
        root (tk.Tk): The main window of the application.
        grid_manager (GridManager): Manages the grid state and logic.
        grid_renderer (GridRenderer): Renders the grid state.
        game_screen (GameScreen): The game screen instance.
        screens (dict): A dictionary to store all screens.
        current_screen (Screen): The current screen being displayed.
    """
    def __init__(self):
        """Initialize the AppManager.

        This method sets up the main window, creates the grid manager,
        initializes the grid renderer and game screen, and stores all screens
        in a dictionary.
        """
        # create the main window
        self.root = tk.Tk()
        self.root.title("Conway's Game of Life")
        self.root.iconbitmap(default=get_path("GoL.ico"))
        self.root.geometry("600x600")

        # create the grid manager
        self.grid_manager = GridManager(20, 20)

        # initialize grid renderer
        self.grid_renderer = None  # updated in GameScreen

        # initialize game screen
        self.game_screen = GameScreen(self)

        # dictionary to store all screens
        self.screens = {
            "home": HomeScreen(self),
            "game": GameScreen(self),
            "settings": SettingsScreen(self),
        }

        # current screen
        self.current_screen = None

    def show_screen(self, screen):
        """Show the specified screen.

        This method hides the current screen and shows the specified screen.

        Args:
            screen (str): The name of the screen to display.
        """
        # hide the current screen
        if self.current_screen:
            self.current_screen.hide()
        # show the new screen
        self.current_screen = self.screens[screen]
        self.current_screen.show()

    def run(self):
        """Run the application.

        This method displays the home screen and starts the main event loop.
        """
        self.show_screen("home")
        self.root.mainloop()
