import random
import re

# create a board object to represent the minesweeper game
class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create the board
        self.board = self.make_new_board()      #plant the bombs
        self.assign_values_to_board()

        # initialize a set to keep track of which locations have been uncovered
        # save (row, col) tuples into this set
        self.dug = set() # if we dig at 0, 0, then self.dug = {(0,0)}
    
    def make_new_board(self):
        # construct a new board based on dimension size and number of bombs

        # generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]        #creates an array that looks like a board

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)       #return a random integer N such that a <= N <= b (assigns each space on the board a unique ID)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                # means there is already a bomb at this location; keep going
                continue
            
            board[row][col] = '*'       #plant the bomb
            bombs_planted += 1
            
        return board

    def assign_values_to_board(self):
        # assign a number 0-8 for all th empty spaces, which represents
        # how many neighboring bombs there are
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if there is already a bomb here, don't calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # iterate through each of the neighboring positions and add up number of bombs

        # make sure not to go out of bounds

        num_neighboring_bombs = 0       #this is the counter
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):         #for row, we're checking above and below; max and min prevent going out of bounds
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):     #for col, we're checking to the left and right; max and min prevent going out of bounds
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        
        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at specified location
        # return True if successful dig, False if bomb

        # possible outcomes:
        # hit a bomb --> game over
        # dig at location with neighboring bombs --> finish dig
        # dig at location with no neighboring bombs --> recursively dig neighbors

        self.dug.add((row, col))        #keep track that we dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        # self.board[row][col] == 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):         #same logic as in get_num_neighboring_bombs function
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue        #don't dig where you've already dug
                self.dig(r, c)
            
            # if the initial dig didn't hit a bomb, we *should not* hit a bomb here
            return True

    def __str__(self):
        # create a new array that represents what the user will see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep



# play the game
def play(dim_size = 10, num_bombs = 10):
    # Step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Step 2: show the user the board and ask where they want to dig
    # Step 3a: if the location is a bomb, show game over message
    # Step 3b: if location is not a bomb, dig recursively until each square is at least next to a bomb
    # Step 4: repeat steps 2 and 3a/3b until there are no more places to dig --> VICTORY!
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row, col: "))      # '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        
        # if input is not valid, ask again
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # if input is valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb
            break       #game over

    # There are 2 ways to end the loop, let's check which one
    if safe:
        print("Congratulations! You are victorious!")
    else:
        print("Sorry! Game over!")
        
        # reveal the whole board
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__':      #not necessary to run, but good practice
    play()