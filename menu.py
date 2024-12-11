import tkinter as tk
from game_window import GameWindow
from scoreboard import ScoreboardWindow
from history import HistoryWindow
import os


class MenuWindow:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        # Create main menu frame
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, padx=20, pady=20)

        # Create title
        title = tk.Label(self.frame, text="Minesweeper", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Create menu buttons
        tk.Button(self.frame, text="Start Game",
                 command=self.show_difficulty_selection).pack(pady=10)

        tk.Button(self.frame, text="Continue Game",
                 command=self.continue_game).pack(pady=10)

        tk.Button(self.frame, text="Game History",
                 command=self.show_history).pack(pady=10)

        tk.Button(self.frame, text="High Scores",
                 command=self.show_scoreboard).pack(pady=10)

    def continue_game(self):
        # Load and continue saved game
        self.frame.pack_forget()
        GameWindow(self.master, load_saved=True, return_to_menu=self.show_menu)

    def show_difficulty_selection(self):
        # Show difficulty selection screen
        self.frame.pack_forget()
        diff_frame = tk.Frame(self.master)
        diff_frame.pack(expand=True, padx=20, pady=20)

        tk.Label(diff_frame, text="Select Difficulty",
                font=("Arial", 18)).pack(pady=20)

        difficulties = {
            "Easy": (9, 9, 10),
            "Medium": (16, 16, 40),
            "Hard": (30, 16, 99)
        }

        for diff, (width, height, mines) in difficulties.items():
            tk.Button(
                diff_frame,
                text=diff,
                command=lambda w=width, h=height, m=mines: self.start_game(w, h, m, diff_frame)
            ).pack(pady=5)

    def start_game(self, width, height, mines, diff_frame):
        # Start new game with selected difficulty
        diff_frame.destroy()
        GameWindow(self.master, width, height, mines, self.show_menu)

    def show_scoreboard(self):
        # Show high scores screen
        self.frame.pack_forget()
        ScoreboardWindow(self.master, self.show_menu)

    def show_history(self):
        # Show game history screen
        self.frame.pack_forget()
        HistoryWindow(self.master, self.show_menu)

    def show_menu(self):
        # Show main menu
        self.frame.pack(expand=True, padx=20, pady=20)