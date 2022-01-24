import copy

class Board:
    def __init__(self):
        self.board = [0 for i in range(10)]

    def __repr__(self):
        return str(repr(self.board))

    def get_board(self):
        return copy.deepcopy(self.board)


class Human:
    def __init__(self, pole):
        self.pole = pole

    def do(self):
        del self.pole[0]

    def __repr__(self):
        return str(repr(self.pole))


board = Board()
man = Human(board.get_board())
for i in range(3):
    man.do()
    print(board)
    print(man)