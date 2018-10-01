from .leader import (Leader, OffensiveLeader, DefensiveLeader, KickerLeader)
from .player import Player

def square_matrix(X):
    '''Squares a matrix'''
    result = [[0.0 for x in range(len(X))] for y in range(len(X))]

    # iterate through rows of X
    for i in range(len(X)):

        # iterate through columns of X
        for j in range(len(X)):

            # iterate through rows of X
            for k in range(len(X)):
                result[i][j] += X[i][k] * X[k][j]

    return result


def add_matrix(X, Y):
    '''Adds two matrices'''
    result = [[0.0 for x in range(len(X))] for y in range(len(X))]

    for i in range(len(X)):

        # iterate through columns
        for j in range(len(X)):
            result[i][j] = X[i][j] + Y[i][j]

    return result


def two_step_dominance(X):
    '''Returns result of two step dominance formula'''
    matrix = add_matrix(square_matrix(X), X)
    result = [sum(x) for x in matrix]
    return result


def power_points(dominance, teams, week):
    '''Returns list of power points'''
    power_points = []
    for i, team in zip(dominance, teams):
        avg_score = sum(team.scores[:week]) / week
        avg_mov = sum(team.mov[:week]) / week

        power = '{0:.2f}'.format((int(i)*0.8) + (int(avg_score)*0.15) +
                                 (int(avg_mov)*0.05))
        power_points.append(power)
    power_tup = [(i, j) for (i, j) in zip(power_points, teams)]
    return sorted(power_tup, key=lambda tup: float(tup[0]), reverse=True)


def sum_scores(players, position):
    score = 0
    if isinstance(players[0], Player):
        for player in players:
            if player.totalPoints is not None:
                score += player.totalPoints
    elif isinstance(players[0], Leader):
        for player in players:
            if player.totalPoints is not None:
                score += player.totalPoints
    return score


def sum_scores_by_player_type(players, position):
    temp_list = filter_by_player_type(players, position)
    scores = sum_scores(temp_list, "")
    return scores


def average_player_scores(players):
    return sum_scores(players, "")/len(players)


def average_by_player_type(players, position):
    temp = filter_by_player_type(players, position)
    return average_player_scores(temp)


def filter_by_player_type(players, position):
    temp_list = []
    for player in players:
        if isinstance(player, Leader):
            if position == "Offense":
                if isinstance(player, OffensiveLeader):
                    temp_list.append(player)
            elif position == "Defense":
                if isinstance(player, DefensiveLeader):
                    temp_list.append(player)
            elif position == "Kicker":
                if isinstance(player, KickerLeader):
                    temp_list.append(player)
        elif isinstance(player, Player):
            if position.lower() == player.getPosition():
                temp_list.append(player)
    return temp_list


def find_max_score(players):
    maximum = 0
    for player in players:
        if player.totalPoints > maximum:
            maximum = player.totalPoints
    return maximum


def find_max_by_type(players, position):
    temp = filter_by_player_type(players, position)
    return find_max_score(temp)