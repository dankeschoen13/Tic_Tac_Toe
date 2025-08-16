from art import board
import numpy as np

# full_board = np.full((7,7), 5)
inner_board = np.array([
    [3, 3, 3, 3, 3],
    [4, 3, 4, 3, 4],
    [3, 3, 3, 3, 3],
    [4, 3, 4, 3, 4],
    [3, 3, 3, 3, 3]
])

class TicEngine:

    def __init__(self):
        self.full_board = np.full((7, 7), 5)
        self.inner_board = inner_board
        self.playable_area = np.zeros((3, 3), dtype=int)
        self.turns_hist = set()

        self.winner = None
        self.active_player = None
        self.turn_cycle = 1
        self.players = {
            'one': 1,
            'two': 2
        }
        self.p_reversed = {val: key for key, val in self.players.items()}

    def add_to_history(self, item):
        t = tuple(item)
        if t in self.turns_hist:
            raise ValueError(f"Duplicate entry: {item}")
        self.turns_hist.add(t)

    def game_start(self):
        while self.winner is None:
            if self.turn_cycle % 2 == 0:
                self.active_player = self.players['two']
            else:
                self.active_player = self.players['one']

            player_input = input(f"Player {self.active_player}'s turn! \n")
            active_player_turn = player_input.split(',')
            try:
                self.add_to_history(active_player_turn)
                row = int(active_player_turn[0]) - 1
                col = int(active_player_turn[1]) - 1
            except ValueError:
                print("Invalid turn. Try again.")
                continue
            self.playable_area[row, col] = self.active_player
            self.turn_cycle += 1
            # self.game_board[1:4, 1:4] = self.playable_area  # superimpose playable_area unto gameboard
            self.render()
            self.winner_check()


    def winner_check(self):
        left_diag = np.diag(self.playable_area)
        right_diag = np.diag(np.fliplr(self.playable_area))

        mask = self.playable_area != 0
        left_mask = left_diag != 0
        right_mask = right_diag != 0

        row_complete = np.any(np.all((self.playable_area == self.playable_area[:, [0]]) & mask, axis=1))
        col_complete = np.any(np.all((self.playable_area == self.playable_area[[0], :]) & mask, axis=0))

        ld_complete = np.all((left_diag == left_diag[0]) & left_mask)
        rd_complete = np.all((right_diag == right_diag[0]) & right_mask)

        if row_complete or col_complete or ld_complete or rd_complete:
            self.winner = self.p_reversed[self.active_player]
            print(f"Player {self.winner} wins!")
        elif np.all(self.playable_area != 0):
            print("Draw! No one wins")
            self.winner = 'Draw'

    def render(self):
        for r in range(3):
            for c in range(3):
                self.inner_board[r * 2, c * 2] = self.playable_area[r, c]
        self.full_board[1:6, 1:6] = self.inner_board
        tiles = {0: " ", 1: "X", 2: "O", 3: "|", 4:"—", 5:"#"}
        for row in self.full_board:
            print(" ".join(tiles[num] for num in row))

print("Let's play tic-tac-toe! Here's our board: ")
print(board)
print("You know how it goes! Your turn in this format: row no., col no. Good luck!")
TicEngine().game_start()
