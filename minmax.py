def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def shortest_path(ground, p1):
    queue = [p1]
    visited = [p1]
    distance = {tuple(p1): 0}

    while len(queue) != 0:
        p = queue.pop(0)
        if ground[p[0]][p[1]] == 1:
            return distance[tuple(p)]
        if ground[p[0] - 1][p[1]] != 0 and [p[0] - 1, p[1]] not in visited:
            queue.append([p[0] - 1, p[1]])
            visited.append([p[0] - 1, p[1]])
            distance[tuple([p[0] - 1, p[1]])] = distance[tuple(p)] + 1
        if ground[p[0] + 1][p[1]] != 0 and [p[0] + 1, p[1]] not in visited:
            queue.append([p[0] + 1, p[1]])
            visited.append([p[0] + 1, p[1]])
            distance[tuple([p[0] + 1, p[1]])] = distance[tuple(p)] + 1
        if ground[p[0]][p[1] - 1] != 0 and [p[0], p[1] - 1] not in visited:
            queue.append([p[0], p[1] - 1])
            visited.append([p[0], p[1] - 1])
            distance[tuple([p[0], p[1] - 1])] = distance[tuple(p)] + 1
        if ground[p[0]][p[1] + 1] != 0 and [p[0], p[1] + 1] not in visited:
            queue.append([p[0], p[1] + 1])
            visited.append([p[0], p[1] + 1])
            distance[tuple([p[0], p[1] + 1])] = distance[tuple(p)] + 1
    return 0


def nearest_point_manhattan_distance(ground, position):
    res = 1000000000
    s = len(ground)
    for i in range(s):
        for j in range(s):
            if ground[i][j] == 1:
                res = min(res, manhattan_distance(position, [i, j]))
    return res


def e_utility(ground, player, ghost1, ghost2, eaten_points):
    ghost_distance = min(manhattan_distance(player.location, ghost1.location),
                         manhattan_distance(player.location, ghost2.location))
    point_distance = shortest_path(ground, player.location)

    point_score = 3 * (35 - point_distance)
    eaten_score = 35 * eaten_points
    ghost_score = 2 * ghost_distance

    if ghost_distance <= 1:
        return 10 * ghost_score + -1000000

    return point_score + eaten_score + ghost_score


def min_max(game, cur_depth, turn, target_depth, eaten_points, alpha, beta):
    if cur_depth == target_depth:
        return e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)

    if turn == "player_turn":
        moves = game.player.valid_moves(game.ground)
        max_eval = -1000000000
        move = ""
        for m in moves:
            flag = 0
            game.player.move(m)
            if game.ground[game.player.location[0]][game.player.location[1]] == 1:
                game.score += 1
                eaten_points += 1
                game.ground[game.player.location[0]][game.player.location[1]] = 2
                flag = 1

            if game.score == 106:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            elif game.player.location == game.ghost1.location or game.player.location == game.ghost2.location:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            else:
                new_val = min_max(game, cur_depth, "ghost1_turn", target_depth, eaten_points + flag, alpha, beta)

            if flag == 1:
                game.score -= 1
                eaten_points -= 1
                game.ground[game.player.location[0]][game.player.location[1]] = 1
            game.player.move_back(m)
            if new_val > max_eval:
                max_eval = new_val
                move = m
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        if cur_depth == 0:
            return move
        else:
            return max_eval

    elif turn == "ghost1_turn":
        min_eval = 1000000000
        moves = game.ghost1.valid_moves(game.ground)
        for m in moves:
            game.ghost1.move(m)
            if game.player.location == game.ghost1.location:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            elif game.score == 106:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            else:
                new_val = min_max(game, cur_depth, "ghost2_turn", target_depth, eaten_points, alpha, beta)
            game.ghost1.move_back(m)
            if new_val < min_eval:
                min_eval = new_val
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval

    elif turn == "ghost2_turn":
        min_eval = 1000000000
        moves = game.ghost2.valid_moves(game.ground)
        for m in moves:
            game.ghost2.move(m)
            if game.player.location == game.ghost2.location:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            elif game.score == 106:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            else:
                new_val = min_max(game, cur_depth + 1, "player_turn", target_depth, eaten_points, alpha, beta)
            game.ghost2.move_back(m)
            if new_val < min_eval:
                min_eval = new_val
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval


def expectimax(game, cur_depth, turn, target_depth, eaten_points):
    if cur_depth == target_depth:
        return e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)

    if turn == "player_turn":
        moves = game.player.valid_moves(game.ground)
        max_eval = -1000000000
        move = ""
        for m in moves:
            flag = 0
            game.player.move(m)
            if game.ground[game.player.location[0]][game.player.location[1]] == 1:
                game.score += 1
                eaten_points += 1
                game.ground[game.player.location[0]][game.player.location[1]] = 2
                flag = 1

            if game.score == 106:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            elif game.player.location == game.ghost1.location or game.player.location == game.ghost2.location:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            else:
                new_val = expectimax(game, cur_depth, "ghost1_turn", target_depth, eaten_points + flag)

            if flag == 1:
                game.score -= 1
                eaten_points -= 1
                game.ground[game.player.location[0]][game.player.location[1]] = 1
            game.player.move_back(m)
            if new_val > max_eval:
                max_eval = new_val
                move = m
        if cur_depth == 0:
            return move
        else:
            return max_eval

    elif turn == "ghost1_turn":
        moves = game.ghost1.valid_moves(game.ground)
        sum_eval = 0
        for m in moves:
            game.ghost1.move(m)
            if game.player.location == game.ghost1.location:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            elif game.score == 106:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            else:
                new_val = expectimax(game, cur_depth, "ghost2_turn", target_depth, eaten_points)
            game.ghost1.move_back(m)
            sum_eval += new_val
        return sum_eval / len(moves)

    elif turn == "ghost2_turn":
        moves = game.ghost2.valid_moves(game.ground)
        sum_eval = 0
        for m in moves:
            game.ghost2.move(m)
            if game.player.location == game.ghost2.location:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            elif game.score == 106:
                new_val = e_utility(game.ground, game.player, game.ghost1, game.ghost2, eaten_points)
            else:
                new_val = expectimax(game, cur_depth + 1, "player_turn", target_depth, eaten_points)
            game.ghost2.move_back(m)
            sum_eval += new_val
        return sum_eval / len(moves)
