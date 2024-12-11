import random
import json
import os
from datetime import datetime
from typing import List, Tuple, Set

class Game:
    def __init__(self, width: int, height: int, mines: int):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flagged = [[False for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.first_move = True
        self.mine_positions: Set[Tuple[int, int]] = set()

        # Create the Saves folder if it doesn't exist
        if not os.path.exists('Saves'):
            os.makedirs('Saves')

    def count_adjacent_flags(self, x: int, y: int) -> int:
        # Count the number of flags around a cell
        flag_count = 0
        for adj_x, adj_y in self.get_adjacent_positions(x, y):
            if self.flagged[adj_y][adj_x]:
                flag_count += 1
        return flag_count

    def reveal_adjacent_cells(self, x: int, y: int) -> bool:
        # Reveal all adjacent cells if the number matches the flag count
        if not self.revealed[y][x] or self.board[y][x] <= 0:
            return True

        flag_count = self.count_adjacent_flags(x, y)
        if flag_count == self.board[y][x]:
            for adj_x, adj_y in self.get_adjacent_positions(x, y):
                if not self.revealed[adj_y][adj_x] and not self.flagged[adj_y][adj_x]:
                    if not self.reveal(adj_x, adj_y):
                        return False
        return True

    def reveal(self, x: int, y: int) -> bool:
        # Handle first move
        if self.first_move:
            self.place_mines(x, y)
            self.first_move = False

        # If already revealed, try to reveal adjacent cells
        if self.revealed[y][x]:
            return self.reveal_adjacent_cells(x, y)

        # Skip if flagged
        if self.flagged[y][x]:
            return True

        # Reveal current cell
        self.revealed[y][x] = True

        # Check if mine was hit
        if self.board[y][x] == -1:
            self.game_over = True
            self.save_game()  # This will archive the game and clear saved_game.json
            return False

        # If empty cell, reveal adjacent cells
        if self.board[y][x] == 0:
            for adj_x, adj_y in self.get_adjacent_positions(x, y):
                if not self.revealed[adj_y][adj_x]:
                    self.reveal(adj_x, adj_y)

        # Check for win condition
        if self.check_win():
            self.save_game()  # This will archive the game and clear saved_game.json

        return True

    def save_game(self):
        # Save the current game state
        game_state = {
            'width': self.width,
            'height': self.height,
            'mines': self.mines,
            'board': self.board,
            'revealed': self.revealed,
            'flagged': self.flagged,
            'game_over': self.game_over,
            'first_move': self.first_move,
            'mine_positions': list(self.mine_positions),
            'timestamp': datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        }

        # If game is finished (won or lost), archive it and clear the saved game
        if self.game_over or self.check_win():
            # Save completed game to archive
            archive_path = f"Saves/game_{game_state['timestamp']}.json"
            with open(archive_path, 'w') as f:
                json.dump(game_state, f)

            # Remove the saved game file
            if os.path.exists('saved_game.json'):
                os.remove('saved_game.json')
        else:
            # Save ongoing game
            with open('saved_game.json', 'w') as f:
                json.dump(game_state, f)

    @classmethod
    def load_game(cls):
        # Load a previously saved game
        try:
            with open('saved_game.json', 'r') as f:
                data = json.load(f)
            game = cls(data['width'], data['height'], data['mines'])
            game.board = data['board']
            game.revealed = data['revealed']
            game.flagged = data['flagged']
            game.game_over = data['game_over']
            game.first_move = data['first_move']
            game.mine_positions = set(tuple(pos) for pos in data['mine_positions'])
            return game
        except FileNotFoundError:
            return None

    def place_mines(self, first_x: int, first_y: int):
        # Place mines ensuring the first click is safe
        safe_zone = self.get_adjacent_positions(first_x, first_y) + [(first_x, first_y)]
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)
                         if (x, y) not in safe_zone]

        # Randomly select positions for mines
        self.mine_positions = set(random.sample(all_positions, self.mines))

        # Place mines and update adjacent cell counts
        for x, y in self.mine_positions:
            self.board[y][x] = -1
            for adj_x, adj_y in self.get_adjacent_positions(x, y):
                if self.board[adj_y][adj_x] != -1:
                    self.board[adj_y][adj_x] += 1

    def get_adjacent_positions(self, x: int, y: int) -> List[Tuple[int, int]]:
        # Get all valid adjacent positions for a given cell
        adjacent = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    adjacent.append((new_x, new_y))
        return adjacent

    def toggle_flag(self, x: int, y: int):
        # Toggle flag on a cell if not revealed
        if not self.revealed[y][x]:
            self.flagged[y][x] = not self.flagged[y][x]

    def check_win(self) -> bool:
        # Check if all non-mine cells are revealed
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True