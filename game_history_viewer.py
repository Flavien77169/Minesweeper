import tkinter as tk


class GameHistoryViewer:
    def __init__(self, master, game_data, return_to_menu):
        self.master = master
        self.game_data = game_data
        self.setup_ui(return_to_menu)

    def setup_ui(self, return_to_menu):
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, padx=20, pady=20)

        # Create title with game info
        timestamp = self.game_data['timestamp'].replace('_', ' ')
        difficulty = self.get_difficulty(self.game_data['width'],
                                         self.game_data['height'],
                                         self.game_data['mines'])

        title = f"Game from {timestamp}\nDifficulty: {difficulty}"
        tk.Label(self.frame, text=title, font=("Arial", 14)).pack(pady=10)

        # Create grid of cells
        grid_frame = tk.Frame(self.frame)
        grid_frame.pack(pady=10)

        for y in range(self.game_data['height']):
            for x in range(self.game_data['width']):
                cell = tk.Label(
                    grid_frame,
                    width=2,
                    height=1,
                    relief="raised",
                    borderwidth=1
                )
                cell.grid(row=y, column=x, padx=1, pady=1)

                # Show cell state
                if self.game_data['revealed'][y][x]:
                    value = self.game_data['board'][y][x]
                    if value == -1:
                        cell.configure(text="💣", bg="red")
                    elif value == 0:
                        cell.configure(bg="lightgray")
                    else:
                        cell.configure(text=str(value), bg="lightgray")
                elif self.game_data['flagged'][y][x]:
                    cell.configure(text="🚩")

        # Add back button
        tk.Button(self.frame, text="Back to Menu",
                  command=lambda: [self.frame.destroy(), return_to_menu()]).pack(pady=20)

    def get_difficulty(self, width, height, mines):
        if width == 9 and height == 9 and mines == 10:
            return "Easy"
        elif width == 16 and height == 16 and mines == 40:
            return "Medium"
        elif width == 30 and height == 16 and mines == 99:
            return "Hard"
        return "Custom"