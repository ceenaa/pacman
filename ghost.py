from random import randint

from base import Base


class Ghost(Base):
    ...

    def make_move(self, ground):
        moves = self.valid_moves(ground)
        move = moves[randint(0, len(moves) - 1)]
        self.move(move)
