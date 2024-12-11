import tkinter as tk
import time
from game import Game
from scoreboard import save_score


class GameWindow:
    def __init__(self, master, width=None, height=None, mines=None, return_to_menu=None, load_saved=False):
        self.master = master
        self.return_to_menu = return_to_menu
        self.start_time = time.time()

        if load_saved:
            self.game = Game.load_game()
            if not self.game:
                self.return_to_menu()
                return
            width, height = self.game.width, self.game.height
            mines = self.game.mines
        else:
            self.game = Game(width, height, mines)

        self.difficulty = self.get_difficulty(width, height, mines)
        self.setup_ui(width, height)

    def setup_ui(self, width, height):
        # Create main frame
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, padx=20, pady=20)

        # Create control buttons
        control_frame = tk.Frame(self.frame)
        control_frame.grid(row=height, column=0, columnspan=width, pady=10)

        save_button = tk.Button(control_frame, text="Save Game", command=self.save_game)
        save_button.pack(side=tk.LEFT, padx=5)

        quit_button = tk.Button(control_frame, text="Quit", command=self.quit_game)
        quit_button.pack(side=tk.LEFT, padx=5)

        # Create grid of buttons
        self.buttons = []
        for y in range(height):
            row = []
            for x in range(width):
                btn = tk.Button(
                    self.frame,
                    width=2,
                    height=1,
                    command=lambda x=x, y=y: self.left_click(x, y)
                )
                btn.grid(row=y, column=x)
                btn.bind('<Button-3>', lambda e, x=x, y=y: self.right_click(x, y))
                row.append(btn)
            self.buttons.append(row)

        # Update display for saved games
        if hasattr(self, 'game'):
            self.update_all_buttons()

    def get_difficulty(self, width, height, mines):
        # Determine difficulty level based on board size and mines
        if width == 9 and height == 9 and mines == 10:
            return "Easy"
        elif width == 16 and height == 16 and mines == 40:
            return "Medium"
        elif width == 30 and height == 16 and mines == 99:
            return "Hard"
        return "Custom"

    def left_click(self, x, y):
        # Handle left click (reveal cell)
        if not self.game.reveal(x, y):
            self.show_all_mines()
            self.show_message("Game Over!")
            self.schedule_return_to_menu()
        else:
            self.update_all_buttons()
            if self.game.check_win():
                self.show_message("Congratulations! You won!")
                self.get_player_name()

    def right_click(self, x, y):
        # Handle right click (toggle flag)
        self.game.toggle_flag(x, y)
        btn = self.buttons[y][x]
        btn.configure(text="🚩" if self.game.flagged[y][x] else "")

    def update_all_buttons(self):
        # Update all button displays
        for y in range(self.game.height):
            for x in range(self.game.width):
                self.update_button(x, y)

    def update_button(self, x, y):
        # Update single button display
        btn = self.buttons[y][x]
        if self.game.revealed[y][x]:
            value = self.game.board[y][x]
            if value == -1:
                btn.configure(text="💣", bg="red")
            elif value == 0:
                btn.configure(text="", bg="lightgray")
            else:
                btn.configure(text=str(value), bg="lightgray")
        elif self.game.flagged[y][x]:
            btn.configure(text="🚩")

    def show_all_mines(self):
        # Reveal all mines on game over
        for y in range(self.game.height):
            for x in range(self.game.width):
                if self.game.board[y][x] == -1:
                    self.buttons[y][x].configure(text="💣", bg="red")

    def save_game(self):
        # Save current game state
        self.game.save_game()
        self.show_message("Game saved successfully!")

    def quit_game(self):
        # Handle game quit with save option
        if not self.game.game_over and not self.game.check_win():
            self.show_quit_dialog()
        else:
            self.frame.destroy()
            self.return_to_menu()

    def show_quit_dialog(self):
        # Show quit confirmation dialog
        popup = tk.Toplevel(self.master)
        popup.title("Quit Game")

        tk.Label(popup, text="Do you want to save before quitting?", padx=20, pady=10).pack()

        tk.Button(popup, text="Save and Quit",
                  command=lambda: [self.game.save_game(), popup.destroy(),
                                   self.frame.destroy(), self.return_to_menu()]).pack(side=tk.LEFT, padx=5, pady=10)

        tk.Button(popup, text="Quit without Saving",
                  command=lambda: [popup.destroy(), self.frame.destroy(),
                                   self.return_to_menu()]).pack(side=tk.LEFT, padx=5, pady=10)

    def show_message(self, message):
        # Show popup message
        popup = tk.Toplevel(self.master)
        popup.title("Game Status")
        tk.Label(popup, text=message, padx=20, pady=20).pack()
        self.master.after(3000, popup.destroy)

    def get_player_name(self):
        # Get player name for high score
        popup = tk.Toplevel(self.master)
        popup.title("Enter Your Name")

        tk.Label(popup, text="Enter your name:").pack(pady=10)
        name_entry = tk.Entry(popup)
        name_entry.pack(pady=10)

        def save():
            name = name_entry.get()
            save_score(name, self.difficulty)
            popup.destroy()
            self.schedule_return_to_menu()

        tk.Button(popup, text="Save", command=save).pack(pady=10)

    def schedule_return_to_menu(self):
        # Schedule return to menu after delay
        self.master.after(3000, lambda: [self.frame.destroy(), self.return_to_menu()])