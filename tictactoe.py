from random import randint
from math import inf


def dict_score(coordinate):
    if coordinate == 'X':
        return {'X wins': 10, 'O wins': -10, 'Draw': 0}
    else:
        return {'X wins': -10, 'O wins': 10, 'Draw': 0}


def find_position(pos, ind):
    if pos < 3:
        return 3 * ind + pos
    if pos < 6:
        pos -= 3
        return 3 * pos + ind
    if pos == 6:
        return 4 * ind
    if pos == 7:
        return 2 * (ind + 1)


def if_not_digit(c1, c2):
    if not c1.isdigit() or not c2.isdigit():
        print('You should enter numbers!')
        return True


# list of empty cells on the field
def empty_indexes(grid):
    return [i for i in range(9) if grid[i] == ' ']


def anti_c(c):
    return 'O' if c == 'X' else 'X'


class TicTacToe:
    scores = {}

    def __init__(self, one, two):
        self.grid = [' ' for _ in range(9)]
        self.lines = self.update_lines()
        self.player_one = ['X', one]
        self.player_two = ['O', two]

    def update_lines(self):
        # columns 0 1 2
        # rows    3 4 5
        # main diagonal  6     counter diagonal  7
        lines = [[self.grid[3 * i + j] for i in range(3)] for j in range(3)] \
                + [[self.grid[i + j * 3] for i in range(3)] for j in range(3)] \
                + [[self.grid[i * 4] for i in range(3)], [self.grid[2 * i] for i in range(1, 4)]]
        return lines

    def print_grid(self):
        print('-' * 9)
        for i in range(3):
            print('|', *[self.grid[3 * i + j] for j in range(3)], '|')
        print('-' * 9)

    def check_status(self):
        for line in self.lines:
            if ['X', 'X', 'X'] == line:
                return [True, 'X wins']
            if ['O', 'O', 'O'] == line:
                return [True, 'O wins']
        if not any([True if x == ' ' else False for line in self.lines for x in line]):
            return [True, 'Draw']
        return [False, 0]

    def check_move(self, c1, c2):
        if c1 > 3 or c2 > 3:
            print('Coordinates should be from 1 to 3!')
            return True
        if self.grid[3 * (int(c1) - 1) + int(c2) - 1] != ' ':
            print('This cell is occupied! Choose another one!')
            return True

    def make_move_user(self, coordinate):
        x_y = input('Enter the coordinates: ').split()
        if if_not_digit(x_y[0], x_y[1]):
            self.make_move_user(coordinate)
            return
        if self.check_move(int(x_y[0]), int(x_y[1])):
            self.make_move_user(coordinate)
            return
        x, y = [int(i) - 1 for i in x_y]
        self.grid[3 * x + y] = coordinate

    def move_easy(self, coordinate):
        x = randint(0, 2)
        y = randint(0, 2)
        if self.grid[3 * x + y] != ' ':
            self.move_easy(coordinate)
            return
        self.grid[3 * x + y] = coordinate

    def move_medium(self, coordinate):
        # if there is a way to win
        for i in range(8):
            if self.lines[i].count(coordinate) == 2 and ' ' in self.lines[i]:
                ind = find_position(i, self.lines[i].index(' '))
                self.grid[ind] = coordinate
                return
        # if the other player has a way to win
        for i in range(8):
            if self.lines[i].count(anti_c(coordinate)) == 2 and ' ' in self.lines[i]:
                ind = find_position(i, self.lines[i].index(' '))
                self.grid[ind] = coordinate
                return
        self.move_easy(coordinate)

    def make_move(self, player):
        if player[1] == 'user':
            self.make_move_user(player[0])
        elif player[1] == 'easy':
            print('Making move level "easy"')
            self.move_easy(player[0])
        elif player[1] == 'medium':
            print('Making move level "medium"')
            self.move_medium(player[0])
        elif player[1] == 'hard':
            print('Making move level "hard"')
            self.best_move(player[0])

    def best_move(self, coordinate):
        best_score = -inf
        avail_spots = empty_indexes(self.grid)
        move = avail_spots[0]

        for i in range(9):
            if self.grid[i] == ' ':
                self.grid[i] = coordinate
                self.lines = self.update_lines()
                score = self.mini_max(False, coordinate)
                self.grid[i] = ' '
                self.lines = self.update_lines()
                if score > best_score:
                    best_score = score
                    move = i
        self.grid[move] = coordinate
        self.lines = self.update_lines()

    def mini_max(self, is_maximising, coordinate):

        result = self.check_status()
        self.scores = dict_score(coordinate)

        if result[0]:
            return self.scores[result[1]]

        if is_maximising:
            best_score = -inf
            for i in range(9):
                if self.grid[i] == ' ':
                    self.grid[i] = coordinate
                    self.lines = self.update_lines()
                    score = self.mini_max(False, coordinate)
                    self.grid[i] = ' '
                    self.lines = self.update_lines()
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = inf
            for i in range(9):
                if self.grid[i] == ' ':
                    self.grid[i] = anti_c(coordinate)
                    self.lines = self.update_lines()
                    score = self.mini_max(True, coordinate)
                    self.grid[i] = ' '
                    self.lines = self.update_lines()
                    best_score = min(best_score, score)
            return best_score

    def game_moves(self, player):
        self.make_move(player)
        self.lines = self.update_lines()
        self.print_grid()

    def start(self):
        self.print_grid()
        while not self.check_status()[0]:
            self.game_moves(self.player_one)
            if self.check_status()[0]:
                print(self.check_status()[1])
                return
            self.game_moves(self.player_two)
        print(self.check_status()[1])


correct_input = ['user', 'easy', 'medium', 'hard']


def check_input(*args):
    if len(args) == 1 and args[0] == 'exit':
        exit()
    if len(args) == 3 and args[0] == 'start':
        if args[1] in correct_input and args[2] in correct_input:
            return True
    return False


# enter start user *difficulty level* (or start *difficulty level* user)
# enter start *difficulty level* *difficulty level*
while True:
    command = input('Input command: ').split()
    if not check_input(*command):
        print('Bad parameters!')
        continue
    game = TicTacToe(command[1], command[2])
    game.start()