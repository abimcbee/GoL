import tkinter as tk
from Screen import Screen
from PIL import Image, ImageTk
import sys
import os


def get_path(filename):
    if getattr(sys, 'frozen', False):  # If running from PyInstaller bundle
        base_path = sys._MEIPASS
    else:  # Running in IDE or script
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, filename)


class HomeScreen(Screen):
    """The home screen of the application.

    Attributes:
        GoL (AppManager): The main application manager.
        canvas (tk.Canvas): The canvas to display the background image.
        original_image (PIL.Image): The original image for the background.
        background_image (ImageTk.PhotoImage): The background image.
        image_on_canvas (int): The image object on the canvas.
        game_label (tk.Label): The label for the game title.
        start_button (tk.Button): The button to start the game.
    """
    def __init__(self, GoL):
        """Initialize the home screen.

        Args:
            GoL (AppManager): The main application manager.
        """
        super().__init__(GoL)

        # create a canvas to display the background image
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(expand=True, fill="both")

        # load the image for background
        self.original_image = Image.open(get_path("home-screen.jpg"))
        self.background_image = ImageTk.PhotoImage(self.original_image)

        # display the background image
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # create a label for the game title
        self.game_label = tk.Label(self.canvas, text="Conway's Game of Life", font=("Fixedsys", 50),
                                   fg="pink", bg="black", wraplength=600)
        self.game_label.place(relx=0.5, rely=0.3, anchor="center")

        # create a button to start the game
        self.start_button = tk.Button(self.canvas, text="Start Game", font=("Fixedsys", 20), command=self.start_game,
                                      bg="pink", fg="black", activebackground="black", activeforeground="white")
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")

        # bind the configure event to resize the image
        self.canvas.bind("<Configure>", self.resize_widgets)

    def resize_widgets(self, event):
        """Resize the image to fit the canvas.

        Args:
            event (tk.Event): The event object containing the new canvas size.
        """
        # Calculate new image size
        new_width = event.width
        new_height = event.height
        # Resize the image
        resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.background_image)

        # Calculate new font sizes based on canvas width
        new_font_size_label = int(self.canvas.winfo_width() / 10)
        new_font_size_button = int(self.canvas.winfo_width() / 20)

        # Update the font sizes
        self.game_label.config(font=("Fixedsys", new_font_size_label))
        self.start_button.config(font=("Fixedsys", new_font_size_button))

        # Update wrap length based on canvas width
        self.game_label.config(wraplength=new_width - 20)

        # Reposition the widgets
        self.game_label.place(relx=0.5, rely=0.3, anchor="center")
        self.start_button.place(relx=0.5, rely=0.6, anchor="center")

    def start_game(self):
        """Switch to the game screen."""
        self.GoL.show_screen("game")
