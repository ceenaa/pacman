class Base:
    def __init__(self, location):
        self.location = location

    def move_up(self):
        self.location[0] -= 1

    def move_down(self):
        self.location[0] += 1

    def move_left(self):
        self.location[1] -= 1

    def move_right(self):
        self.location[1] += 1

    def is_move_up_valid(self, ground):
        if ground[self.location[0] - 1][self.location[1]] != 0:
            return True
        else:
            return False

    def is_move_down_valid(self, ground):
        if ground[self.location[0] + 1][self.location[1]] != 0:
            return True
        else:
            return False

    def is_move_left_valid(self, ground):
        if ground[self.location[0]][self.location[1] - 1] != 0:
            return True
        else:
            return False

    def is_move_right_valid(self, ground):
        if ground[self.location[0]][self.location[1] + 1] != 0:
            return True
        else:
            return False

    def valid_moves(self, ground):
        moves = []
        if self.is_move_up_valid(ground):
            moves.append("up")
        if self.is_move_down_valid(ground):
            moves.append("down")
        if self.is_move_left_valid(ground):
            moves.append("left")
        if self.is_move_right_valid(ground):
            moves.append("right")
        return moves

    def move(self, move):
        if move == "up":
            self.move_up()
        elif move == "down":
            self.move_down()
        elif move == "left":
            self.move_left()
        elif move == "right":
            self.move_right()

    def move_back(self, move):
        if move == "up":
            self.move_down()
        elif move == "down":
            self.move_up()
        elif move == "left":
            self.move_right()
        elif move == "right":
            self.move_left()
