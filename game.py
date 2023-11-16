import os
from os import system
from time import sleep

from minmax import min_max, expectimax
from ghost import Ghost
from player import Player


class Game:
    def __init__(self):
        self.ground = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.player = Player([9, 9])
        self.ghost1 = Ghost([5, 18])
        self.ghost2 = Ghost([5, 1])
        self.score = 0

    def print_ground(self):
        for i in range(0, 11):
            for j in range(0, 20):
                if self.player.location == [i, j]:
                    print("P", end=" ")
                elif self.ghost1.location == [i, j]:
                    print("G", end=" ")
                elif self.ghost2.location == [i, j]:
                    print("G", end=" ")
                elif self.ground[i][j] == 0:
                    print("#", end=" ")
                elif self.ground[i][j] == 1:
                    print(".", end=" ")
                elif self.ground[i][j] == 2:
                    print(" ", end=" ")
            print()

    def is_game_over(self):
        if self.score == 106:
            return True
        if self.player.location == self.ghost1.location or self.player.location == self.ghost2.location:
            return True
        else:
            return False

    def move_player_up(self):
        if self.player.is_move_up_valid(self.ground):
            self.player.move_up()
            if self.ground[self.player.location[0]][self.player.location[1]] == 1:
                self.score += 1
                self.ground[self.player.location[0]][self.player.location[1]] = 2

    def move_player_down(self):
        if self.player.is_move_down_valid(self.ground):
            self.player.move_down()
            if self.ground[self.player.location[0]][self.player.location[1]] == 1:
                self.score += 1
                self.ground[self.player.location[0]][self.player.location[1]] = 2

    def move_player_left(self):
        if self.player.is_move_left_valid(self.ground):
            self.player.move_left()
            if self.ground[self.player.location[0]][self.player.location[1]] == 1:
                self.score += 1
                self.ground[self.player.location[0]][self.player.location[1]] = 2

    def move_player_right(self):
        if self.player.is_move_right_valid(self.ground):
            self.player.move_right()
            if self.ground[self.player.location[0]][self.player.location[1]] == 1:
                self.score += 1
                self.ground[self.player.location[0]][self.player.location[1]] = 2

    def move_player(self, depth, mode):
        movement = ""
        if mode == "expectimax":
            movement = expectimax(self, 0, "player_turn", depth, 0)
        elif mode == "minimax":
            movement = min_max(self, 0, "player_turn", depth, 0, -1000000000, +1000000000)
        if movement == "":
            raise Exception("Invalid movement")

        if movement == "up":
            self.move_player_up()
        elif movement == "down":
            self.move_player_down()
        elif movement == "left":
            self.move_player_left()
        elif movement == "right":
            self.move_player_right()

    def run_game(self, depth, mode):
        itr = 0
        while not self.is_game_over():
            itr += 1
            print("Score: ", self.score)
            print("Iteration: ", itr)
            self.print_ground()
            sleep(0.05)
            self.move_player(depth, mode)
            if self.is_game_over():
                break
            self.ghost1.make_move(self.ground)
            if self.is_game_over():
                break
            self.ghost2.make_move(self.ground)
            sleep(0.05)
            system("clear")
        os.system("clear")
        print("Score: ", self.score)
        print("Iteration: ", itr)
        self.print_ground()

        return self.score, itr

    def test_run_game(self, depth, mode):
        itr = 0
        while not self.is_game_over():
            itr += 1
            self.move_player(depth, mode)
            if self.is_game_over():
                break
            self.ghost1.make_move(self.ground)
            if self.is_game_over():
                break
            self.ghost2.make_move(self.ground)
        return self.score, itr


def test(mode):
    for d in range(1, 4):
        count_of_lost = 0
        avg_itr = 0
        for i in range(0, 50):
            game = Game()
            score, itr = game.test_run_game(d, mode)
            if score != 106:
                count_of_lost += 1
            avg_itr += itr
        print("Mode: ", mode)
        print("Depth: ", d)
        print("Count of lost: ", count_of_lost)
        print("Average iteration: ", avg_itr / 50)
        print("Percentage of lost: ", count_of_lost / 50 * 100)
