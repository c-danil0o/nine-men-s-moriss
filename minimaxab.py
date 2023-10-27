import copy

from state import *


class Minimax(object):
    MIN = -100000
    MAX = 100000
    next_move = (-4, -4)
    depth = 0

    def __init__(self, depth):
        Minimax.depth = depth

    @staticmethod
    def possible_moves(maximizing, board, phase, remove):
        changes = []
        if remove:
            toremoveall = []
            toremove = []
            for i in range(24):
                if maximizing:
                    if board[i] == 2:
                        toremoveall.append(i)
                        if i not in find_triples(board, 2):
                            toremove.append(i)
                else:
                    if board[i] == 1:
                        toremoveall.append(i)
                        if i not in find_triples(board, 1):
                            toremove.append(i)
            if len(toremove) == 0:
                toremove = toremoveall
            for i in toremove:
                changes.append((i, -3))
        elif phase > 0:
            for possibility in range(24):
                if board[possibility] == 0:
                    if maximizing:
                        changes.append((possibility, -1))
                    else:
                        changes.append((possibility, -2))

        elif phase <= 0:
            for i in range(24):
                if maximizing:
                    if board[i] == 1:
                        for pos in adjacent[i]:
                            if board[pos] == 0:
                                changes.append((i, pos))
                else:
                    if board[i] == 2:
                        for pos in adjacent[i]:
                            if board[pos] == 0:
                                changes.append((i, pos))
        return changes

    @staticmethod
    def minimax(board, change, depth, maximizing, phase, rm=0):
        br = copy.deepcopy(board)
        new_state = updateboard(br, change)
        remove = new_morris(board, change)
        if rm:
            remove = 1
            maximizing = not maximizing
        if depth <= 0:
            return evaluate(new_state, board, phase, change)
        if maximizing:
            bestvalue = Minimax.MIN
            for change in Minimax.possible_moves(maximizing if not remove else (not maximizing), new_state, phase,
                                                 0 if remove == 0 else 1):
                value = Minimax.minimax(new_state, change, depth - 1, not maximizing, phase - 1)
                if bestvalue < value:
                    bestvalue = value
                    if depth == Minimax.depth:
                        Minimax.next_move = change
            return bestvalue
        else:
            bestvalue = Minimax.MAX
            for change in Minimax.possible_moves(maximizing if not remove else (not maximizing), new_state, phase,
                                                 0 if remove == 0 else 1):
                value = Minimax.minimax(new_state, change, depth - 1, not maximizing, phase - 1)
                if bestvalue > value:
                    bestvalue = value
                    if depth == Minimax.depth:
                        Minimax.next_move = change
            return bestvalue

    @staticmethod
    def alphabeta(board, change, depth, maximizing, phase, rm=0, alpha=MIN, beta=MAX):
        br = copy.deepcopy(board)
        new_state = updateboard(br, change)
        remove = new_morris(board, change)
        if rm:
            remove = 1
            maximizing = not maximizing
        if depth <= 0:
            return evaluate(new_state, board, phase, change)
        if maximizing:
            bestvalue = Minimax.MIN
            for change in Minimax.possible_moves(maximizing if not remove else (not maximizing), new_state, phase,
                                                  0 if remove == 0 else 1):
                value = Minimax.alphabeta(new_state, change, depth - 1, not maximizing, phase - 1, 0, alpha, beta)
                if bestvalue < value:
                    bestvalue = value
                    if depth == Minimax.depth:
                        Minimax.next_move = change
                alpha = max(alpha, bestvalue)
                if alpha >= beta:
                    break
            return bestvalue
        else:
            bestvalue = Minimax.MAX
            for change in Minimax.possible_moves(maximizing if not remove else (not maximizing), new_state, phase,
                                                  0 if remove == 0 else 1):
                value = Minimax.alphabeta(new_state, change, depth - 1, not maximizing, phase - 1, 0, alpha, beta)
                if bestvalue > value:
                    bestvalue = value
                    if depth == Minimax.depth:
                        Minimax.next_move = change
                beta = min(beta, bestvalue)
                if alpha >= beta:
                    break
            return bestvalue
