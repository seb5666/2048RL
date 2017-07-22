import math
import random
import numpy as np

class Game:

    def __init__(self, size = 4, allow_fours = False, end_number = 2048):
        self.size = size
        self.allow_fours = allow_fours
        self.end_number = end_number
        self.board = np.array([[0 for i in range(size)] for i in range(size)])

        #initialise board with 2 tiles
        self.next_tile()
        self.next_tile()

    def print_board(self):

        hline = (self.size * 8) * "-"
        print(hline)
        for row in self.board:
            print("|", end="")
            for x in row:
                print("{:^6}|".format(x), end=' ')
            print()
            print(hline)

    def move(self, direction):
        old_board = np.copy(self.board)
        if direction in ["LEFT", "a"]:
            for i in range(self.size):
                self.board[i] = self.colapse_row(self.board[i])
        if direction in ["RIGHT", "d"]:
            for i in range(self.size):
                self.board[i] = (self.colapse_row(self.board[i][::-1]))[::-1]
        if direction in ["DOWN", "s"]:
            for i in range(self.size):
                self.board[:,i] = self.colapse_row(self.board[:,i][::-1])[::-1]
        if direction in ["UP", "w"]:
            for i in range(self.size):
                self.board[:,i] = self.colapse_row(self.board[:,i])

        return not(np.array_equal(self.board, old_board))

    def colapse_row(self, row):
        i = 0
        j = 0
        while i < len(row):
            if row[i] != 0:
                row[j] = row[i]
                j+=1
            i+=1
        for k in range(j, len(row)):
            row[k] = 0
        for k in range(min(j, len(row)-1)):
            if row[k] == row[k+1]:
                row[k] = 2 * row[k]
                for l in range(k+1, min(j, len(row) - 1)):
                    row[l] = row[l+1]
                row[min(j, len(row)-1)] = 0
                k += 1
        return row

    def next_tile(self):
        positions = np.argwhere(self.board == 0)
        if len(positions) == 0:
            return False
        x,y = positions[np.random.randint(len(positions))] 
        tile = 2
        if self.allow_fours:
            tile = 2 if random.random() < 0.9 else 4
        self.board[x,y] = tile
        return True
    
    def is_over(self):
        return self.is_lost() or self.is_won()

    def is_lost(self):
        # check if board contains a zero
        if len(np.argwhere(self.board == 0)) > 0:
                return False

        # check if two tiles can collapse
        for row in self.board:
            for i in range(self.size - 1):
                if row[i] != 0 and row[i] == row[i+1]:
                    return False
        for i in range(self.size):
            col = self.board[:, i]
            for j in range(self.size - 1):
                if col[j] != 9 and col[j] == col[j+1]:
                    return False
        # else it is game over
        return True
   
    def is_won(self):
        return self.end_number in self.board
    
    def get_board(self):
        return np.copy(self.board)

    def play(self, direction):
        if self.is_lost():
            raise GameLostException()
        if self.is_won():
            raise GameWonException()
        moved = self.move(direction)
        if moved:
            self.next_tile()

    def play_console(self):
        while True:
            self.print_board()
            if self.is_lost():
                print("Game over")
                exit()
            if self.is_won():
                print("You win")
                exit()
            direction = input()
            while direction not in ['a','s','w','d']:
                direction = input()
            self.play(direction)

class GameWonException(Exception):
    pass

class GameLostException(Exception):
    pass

if __name__ == "__main__":
    game = Game(end_number = 64, size = 3)
    game.play_console()
