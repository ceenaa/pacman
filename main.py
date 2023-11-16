from game import Game, test

g = Game()

# you can run the game with any depth and minimax or expectimax mode
# comment out the other one to run the game with the other mode

# run the game with depth 1 and minimax mode
g.run_game(depth=1, mode="minimax")

# run the game with depth 1 and expectimax mode
# g.run_game(depth=1, mode="expectimax")

# performance testing with depth 1, 2, 3 and minimax mode
# test("minimax")

# performance testing with depth 1, 2, 3 and expectimax mode
# test("expectimax")