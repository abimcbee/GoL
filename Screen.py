import tkinter as tk


class Screen:
    """The base class for all screens.

    Attributes:
        GoL (AppManager): The main application manager.
        frame (tk.Frame): The frame of the screen.
    """
    def __init__(self, GoL):
        """Initialize the screen.

        Args:
            GoL (AppManger): The main application manager.
        """
        self.GoL = GoL
        self.frame = tk.Frame(GoL.root)

    def show(self):
        """Show the screen"""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide the screen"""
        self.frame.pack_forget()
