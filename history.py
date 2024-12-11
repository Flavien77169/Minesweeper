import tkinter as tk
import json
import os
from datetime import datetime
from game_window import GameWindow
from game_history_viewer import GameHistoryViewer


class HistoryWindow:
    def __init__(self, master, return_to_menu):
        self.master = master
        self.setup_ui(return_to_menu)

    def setup_ui(self, return_to_menu):
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, padx=20, pady=20)

        # Create title
        tk.Label(self.frame, text="Game History",
                 font=("Arial", 18)).pack(pady=20)

        # Create scrollable frame for game list
        scroll_frame = tk.Frame(self.frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.game_list = tk.Listbox(scroll_frame, yscrollcommand=scrollbar.set,
                                    width=50, height=15)
        self.game_list.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.game_list.yview)

        # Load and display saved games
        self.saved_games = self.load_game_history()
        for game in self.saved_games:
            status = "Won" if game["won"] else "Lost"
            timestamp = datetime.strptime(game["timestamp"], "%Y-%m-%d_%H-%M-%S")
            display_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            self.game_list.insert(tk.END,
                                  f"{display_date} - {game['difficulty']} - {status}")

        # Add view button
        tk.Button(self.frame, text="View Game",
                  command=lambda: self.view_game(return_to_menu)).pack(pady=10)

        # Add back button
        tk.Button(self.frame, text="Back to Menu",
                  command=lambda: [self.frame.destroy(), return_to_menu()]).pack(pady=10)

    def load_game_history(self):
        games = []
        saves_dir = "Saves"
        if os.path.exists(saves_dir):
            for filename in os.listdir(saves_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(saves_dir, filename), 'r') as f:
                        game_data = json.load(f)
                        # Determine if game was won
                        won = True
                        for y in range(len(game_data['revealed'])):
                            for x in range(len(game_data['revealed'][0])):
                                if (game_data['board'][y][x] == -1 and
                                        game_data['revealed'][y][x]):
                                    won = False
                                    break
                        # Add game info
                        games.append({
                            'filename': filename,
                            'timestamp': game_data['timestamp'],
                            'difficulty': self.get_difficulty(game_data['width'],
                                                              game_data['height'],
                                                              game_data['mines']),
                            'won': won,
                            'data': game_data
                        })
        return sorted(games, key=lambda x: x['timestamp'], reverse=True)

    def get_difficulty(self, width, height, mines):
        if width == 9 and height == 9 and mines == 10:
            return "Easy"
        elif width == 16 and height == 16 and mines == 40:
            return "Medium"
        elif width == 30 and height == 16 and mines == 99:
            return "Hard"
        return "Custom"

    def view_game(self, return_to_menu):
        selection = self.game_list.curselection()
        if not selection:
            return

        game_data = self.saved_games[selection[0]]['data']
        self.frame.destroy()
        GameHistoryViewer(self.master, game_data, return_to_menu)