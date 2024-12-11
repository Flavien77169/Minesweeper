import tkinter as tk
import json
import os

SCORES_FILE = "scores.json"


def load_scores():
    # Load high scores from file
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return {"Easy": [], "Medium": [], "Hard": []}


def save_score(player_name, difficulty):
    # Save new high score
    scores = load_scores()
    scores[difficulty].append(player_name)
    scores[difficulty] = scores[difficulty][-5:]  # Keep only top 5 scores

    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)


class ScoreboardWindow:
    def __init__(self, master, return_to_menu):
        self.master = master
        self.setup_ui(return_to_menu)

    def setup_ui(self, return_to_menu):
        # Create scoreboard frame
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, padx=20, pady=20)

        # Create title
        tk.Label(self.frame, text="High Scores",
                 font=("Arial", 18)).pack(pady=20)

        # Display scores for each difficulty
        scores = load_scores()
        for difficulty in ["Easy", "Medium", "Hard"]:
            tk.Label(self.frame, text=f"\n{difficulty} Mode:",
                     font=("Arial", 14)).pack()

            if scores[difficulty]:
                for i, name in enumerate(scores[difficulty], 1):
                    tk.Label(self.frame, text=f"{i}. {name}").pack()
            else:
                tk.Label(self.frame, text="No scores yet").pack()

        # Add back button
        tk.Button(
            self.frame,
            text="Back to Menu",
            command=lambda: [self.frame.destroy(), return_to_menu()]
        ).pack(pady=20)