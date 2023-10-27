from hashmap import adjacent
triples = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23],
           [0, 9, 21], [3, 10, 18], [6, 11, 15], [1, 4, 7], [8, 12, 17], [5, 13, 20], [2, 14, 23], [16, 19, 22]]
# adjacent = {0: [1, 9], 1: [0, 2, 4], 2: [1, 14], 3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13], 6: [11, 7], 7: [6, 8, 4],
#             8: [7, 12], 9: [0, 10, 21], 10: [9, 11, 3, 18], 11: [10, 6, 15], 12: [8, 13, 17], 13: [5, 12, 14, 20],
#             14: [2, 13, 23], 15: [11, 16], 16: [15, 17, 19], 17: [16, 12], 18: [10, 19], 19: [18, 20, 16, 22],
#             20: [19, 13], 21: [9, 22], 22: [21, 23, 19], 23: [22, 14]}
three_piece = [[9, 0, 1, 21, 2], [1, 2, 14, 0, 23], [9, 21, 22, 0, 23], [22, 23, 14, 21, 2], [10, 3, 4, 18, 5],
               [4, 5, 13, 3, 20], [13, 20, 19, 18, 5], [10, 18, 19, 3, 20],
               [11, 6, 7, 15, 8], [7, 8, 12, 6, 17], [12, 17, 16, 15, 8], [11, 15, 16, 6, 17]]

# [21, 0, 2], [21, 23, 2], [18, 3, 5], [18, 20, 5],
#  [15, 6, 8], [15, 17, 8]]
coefficients = [0 for i in range(9)]
placed_triples = {1: [], 2: []}
white = black = 0
player_two_pieces = ai_two_pieces = []
player = 0


def updateboard(board, change):
    if change == (-4, -4):
        return board
    if change[1] == -1:
        board[change[0]] = 1
    elif change[1] == -2:
        board[change[0]] = 2
    elif change[1] == -3:
        board[change[0]] = 0
    else:
        board[change[0]], board[change[1]] = board[change[1]], board[change[0]]
    return board
    # def __init__(self, placed, old_triples, white_placed, white_left, black_placed, black_left,
    #              game_phase, placed_triples=None):
    #     if placed_triples is None:
    #         placed_triples = {1: [], 2: []}
    #     self._placed = placed
    #     self._placed_triples = placed_triples
    #     self._old_triples = old_triples
    #     self._white_placed = white_placed
    #     self._white_left = white_left
    #     self._black_placed = black_placed
    #     self._black_left = black_left
    #     self._player_triples = []
    #     self._ai_triples = []
    #     self._game_phase = game_phase


def new_morris(board, change):
    global player
    for tr in triples:
        if change[1] == -1:
            if (change[0] == tr[0] and board[tr[1]] == board[tr[2]] == 1) or (
                    change[0] == tr[1] and board[tr[0]] == board[tr[2]] == 1) or (
                    change[0] == tr[2] and board[tr[1]] == board[tr[0]] == 1):
                return 1
        elif change[1] == -2:
            if (change[0] == tr[0] and board[tr[1]] == board[tr[2]] == 2) or (
                    change[0] == tr[1] and board[tr[0]] == board[tr[2]] == 2) or (
                    change[0] == tr[2] and board[tr[1]] == board[tr[0]] == 2):
                return -1
        elif change[1] >= 0:
            player = board[change[0]]
            board[change[0]] = 0
            if (change[1] == tr[0] and board[tr[1]] == board[tr[2]] == player) or (
                    change[1] == tr[1] and board[tr[0]] == board[tr[2]] == player) or (
                    change[1] == tr[2] and board[tr[1]] == board[tr[0]] == player):
                board[change[0]] = player
                if player == 1:
                    return 1
                else:
                    return -1
            board[change[0]] = player
    return 0


def find_triples(board, player):
    global placed_triples
    placed_triples = {1: [], 2: []}
    for triple in triples:
        if board[triple[0]] == board[triple[1]] == board[triple[2]] == player:
            placed_triples[player].append(tuple(triple))
    return placed_triples[player]


def morris_difference(board):
    # print(self._player_triples, ' //// ', self._ai_triples)
    return len(find_triples(board, 1)) - len(find_triples(board, 2))


def pieces_difference(board):
    global white, black
    white = black = 0
    for i in range(24):
        if board[i] == 1:
            white += 1
        elif board[i] == 2:
            black += 1
    return white - black


def two_piece_difference(board):
    global player_two_pieces, ai_two_pieces
    player_two_pieces = ai_two_pieces = []
    for tr in triples:
        if (board[tr[0]] == board[tr[1]] == 1 and board[tr[2]] == 0) or \
                (board[tr[0]] == board[tr[2]] == 1 and board[tr[1]] == 0) or \
                (board[tr[1]] == board[tr[2]] == 1 and board[tr[0]] == 0):
            player_two_pieces.append((tr[0], tr[1], tr[2]))
        if (board[tr[0]] == board[tr[1]] == 2 and board[tr[2]] == 0) or \
                (board[tr[0]] == board[tr[2]] == 2 and board[tr[1]] == 0) or \
                (board[tr[1]] == board[tr[2]] == 2 and board[tr[0]] == 0):
            player_two_pieces.append((tr[0], tr[1], tr[2]))

    return len(player_two_pieces) - len(ai_two_pieces)


def blocked_pieces(board):
    player_blocked = ai_blocked = 0
    for i in range(24):
        if board[i] == 1:
            blocked = True
            for adj in adjacent[i]:
                if board[adj] == 0:
                    blocked = False
            if blocked:
                player_blocked += 1
        if board[i] == 2:
            blocked = True
            for adj in adjacent[i]:
                if board[adj] == 0:
                    blocked = False
            if blocked:
                ai_blocked += 1
    return player_blocked - ai_blocked


def three_piece_difference(board):
    player_three_piece = ai_three_piece = 0
    for three in three_piece:
        if (board[three[0]] == board[three[1]] == board[three[2]] == 1 and board[
            three[3]] == board[three[4]] == 0) or \
                (board[three[3]] == board[three[1]] == board[three[4]] == 1 and board[
                    three[0]] == board[three[2]] == 0):
            player_three_piece += 1
        if (board[three[0]] == board[three[1]] == board[three[2]] == 2 and board[
            three[3]] == board[three[4]] == 0) or \
                (board[three[3]] == board[three[1]] == board[three[4]] == 2 and board[
                    three[0]] == board[three[2]] == 0):
            ai_three_piece += 1
    return player_three_piece - ai_three_piece


def double_morrises(board):
    player_double_morrises = ai_double_morrises = 0
    if len(placed_triples[1]) > 1:
        for morris in placed_triples[1]:
            for morris2 in placed_triples[1]:
                if morris != morris2:
                    for mor in morris2:
                        if morris[0] == mor or morris[1] == mor or morris[2] == mor:
                            player_double_morrises += 1
    if len(placed_triples[2]) > 1:
        for morris in placed_triples[2]:
            for morris2 in placed_triples[2]:
                if morris != morris2:
                    for mor in morris2:
                        if morris[0] == mor or morris[1] == mor or morris[2] == mor:
                            ai_double_morrises += 1
    return player_double_morrises - ai_double_morrises


def winning_state(board, phase):
    if white < 3 and phase == 0:
        return -1
    if black < 3 and phase == 0:
        return 1
    blocked = False
    for i in range(24):
        if board[i] == 2:
            for adj in adjacent[i]:
                if board[adj] != 1:
                    blocked = False
                    break
            if not blocked:
                break
            blocked = True
        if blocked:
            return -1
    return 0


def opened_morris(board, phase):
    if not player:
        return 0
    if phase > 0:
        return 0
    opened_morrises = {1: 0, 2: 0}
    if player == 1:
        for two in player_two_pieces:
            found = 0
            for i in two:
                if board[i] == 0:
                    found = 1
                    for adj in adjacent[i]:
                        if board[adj] == player and adj != two[0] != two[1] != two[2]:
                            opened_morrises[player] += 1
                            break
                if found:
                    break
    else:
        for two in ai_two_pieces:
            found = 0
            for i in two:
                if board[i] == 0:
                    found = 1
                    for adj in adjacent[i]:
                        if board[adj] == player and adj != two[0] != two[1] != two[2]:
                            opened_morrises[player] += 1
                            break
                if found:
                    break
    return opened_morrises[1] - opened_morrises[2]


def print_states():
    print('Closed morris check: ', coefficients[0])
    print('Morris difference: ', coefficients[1])
    print('Blocked pieces: ', coefficients[2])
    print('Pieces difference: ', coefficients[3])
    print('Two piece difference: ', coefficients[4])
    print('Three piece difference: ', coefficients[5])
    print('Double morrises: ', coefficients[6])
    print('Winning state: ', coefficients[7])
    print('Opened morrises', coefficients[8])
    print('___________________')


def evaluate(board, old, phase, change, prnt=0):
    coefficients[0] = new_morris(old, change)
    coefficients[1] = morris_difference(board)
    coefficients[2] = blocked_pieces(board)
    coefficients[3] = pieces_difference(board)
    coefficients[4] = two_piece_difference(board)
    coefficients[5] = three_piece_difference(board)
    coefficients[6] = double_morrises(board)
    coefficients[7] = winning_state(board, phase)
    coefficients[8] = opened_morris(board, phase)
    result = 0
    if phase > 0:
        # 18 * (1) + 26 * (2) + 1 * (3) + 9 * (4) + 10 * (5) + 7 * (6)
        result = 18 * coefficients[0] + 26 * coefficients[1] + coefficients[2] + 9 * coefficients[3] + 10 * \
                 coefficients[4] + 7 * coefficients[5]
    else:
        # 14 * (1) + 43 * (2) + 10 * (3) + 11 * (4) + 8 * (7) + 1086 * (8)
        result = 25 * coefficients[0] + 30 * coefficients[1] + 7 * coefficients[2] + 11 * coefficients[3] + 8 * \
                 coefficients[6] + 1086 * coefficients[7] + 18 * coefficients[8]
    if prnt:
        print_states()
    # print(result)
    return result
