import copy
from minimaxab import Minimax
from state import *
from hashmap import adjacent
DEPTH = 3


class Game(object):
    # adjacent = {0: [1, 9], 1: [0, 2, 4], 2: [1, 14], 3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13], 6: [11, 7], 7: [6, 8, 4],
    #             8: [7, 12], 9: [0, 10, 21], 10: [9, 11, 3, 18], 11: [10, 6, 15], 12: [8, 13, 17], 13: [5, 12, 14, 20],
    #             14: [2, 13, 23], 15: [11, 16], 16: [15, 17, 19], 17: [16, 12], 18: [10, 19], 19: [18, 20, 16, 22],
    #             20: [19, 13], 21: [9, 22], 22: [21, 23, 19], 23: [22, 14]}

    triples = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23],
               [0, 9, 21], [3, 10, 18], [6, 11, 15], [1, 4, 7], [8, 12, 17], [5, 13, 20], [2, 14, 23], [16, 19, 22]]

    def __init__(self):
        self._white_placed = 0
        self._black_placed = 0
        self._white_left = 9
        self._black_left = 9
        self._placed = [0 for _ in range(24)]
        self._highlighted = [0 for _ in range(24)]
        self._move = False
        self._remove = False
        self._delete = False
        self._player_turn = 1
        self._placed_triples = {1: [], 2: []}
        self._old_triples = {1: [], 2: []}
        self._has_triple = {1: False, 2: False}
        self._prev = 0
        self._game_phase = 1

    @property
    def highlighted(self):
        return self._highlighted

    @property
    def placed(self):
        return self._placed

    @property
    def white_left(self):
        return self._white_left

    @property
    def black_left(self):
        return self._black_left

    @property
    def player_turn(self):
        return self._player_turn

    @property
    def game_phase(self):
        return self._game_phase

    def next_player(self):
        if self._player_turn == 1:
            self._player_turn = 2
        else:
            self._player_turn = 1

    def oposite_player(self):
        if self._player_turn == 1:
            return 2
        else:
            return 1

    def highlight(self, position):
        for adj in adjacent[position]:
            if not self._placed[adj]:
                self._highlighted[adj] = True

    def reset_highlights(self):
        for i in range(24):
            self._highlighted[i] = False

    def check_move(self, position):
        if self._remove:
            if self._highlighted[position]:
                self._placed[position] = 0
                if self._player_turn == 1:
                    self._black_placed -= 1
                else:
                    self._white_placed -= 1
                self._remove = False
                self.check_triples(True)
                self.reset_highlights()
                self.next_player()
        elif self._move:
            if self._highlighted[position]:
                self._placed[self._prev], self._placed[position] = self._placed[position], self._placed[self._prev]
                self.reset_highlights()
                self.check_triples()
            self._move = False
            if not self._remove:
                self.reset_highlights()
        elif not self._placed[position]:
            if self._player_turn == 1 and self._white_left > 0:
                self._white_left -= 1
                self._white_placed += 1
                self._placed[position] = 1
                self.check_triples()

            elif self._player_turn == 2 and self._black_left > 0:
                self._black_left -= 1
                self._black_placed += 1
                self._placed[position] = 2
                self.check_triples()

        elif self._white_left == 0 and self._black_left == 0 and ((self._placed[position] == 2 and
                                                                   self._player_turn == 2) or (self._placed[
                                                                                                   position] == 1 and self._player_turn == 1)):
            self._game_phase = 2
            for adj in adjacent[position]:
                if not self._placed[adj]:
                    self._highlighted[adj] = True
                self._move = True
                self._prev = position

    def check_triples(self, check=False):
        self._old_triples = self._placed_triples
        self._placed_triples = {1: [], 2: []}
        self._has_triple = {1: False, 2: False}
        for tr in Game.triples:
            if self._placed[tr[0]] == self._placed[tr[1]] == self._placed[tr[2]] == 1:
                self._placed_triples[1].append((tr[0], tr[1], tr[2]))
                if (tr[0], tr[1], tr[2]) not in self._old_triples[1]:
                    self._has_triple[1] = True
            if self._placed[tr[0]] == self._placed[tr[1]] == self._placed[tr[2]] == 2:
                self._placed_triples[2].append((tr[0], tr[1], tr[2]))
                if (tr[0], tr[1], tr[2]) not in self._old_triples[2]:
                    self._has_triple[2] = True
        if self._has_triple[self._player_turn]:
            self.highlight_for_remove()
        else:
            if check:
                pass
            else:
                self.next_player()

    def highlight_for_remove(self):
        for i in range(24):
            gotonext = 0
            if self._placed[i] == self.oposite_player():
                for tr in self._placed_triples[self.oposite_player()]:
                    if i in tr:
                        gotonext = 1
                        break
                if gotonext == 1:
                    continue
                self._highlighted[i] = True
        exist = False
        for i in range(24):
            if self._highlighted[i]:
                exist = True
                break
        if not exist:
            for i in range(24):
                if self._placed[i] == self.oposite_player():
                    self._highlighted[i] = True
        self._remove = True

    def check_if_end(self):
        if self._white_placed == 2 and self._white_left == 0:
            print('Black has won!')
        if self._black_placed == 2 and self._black_left == 0:
            print('White has won')
        blocked = False
        for i in range(24):
            if self._placed[i] == self._player_turn:
                for adj in adjacent[i]:
                    if self._placed[adj] != self.oposite_player():
                        blocked = False
                        break
                if not blocked:
                    break
                blocked = True
            if blocked:
                print('PLAYER ', self._player_turn, ' HAS WON!')

    def ai_next_move(self):
        self.reset_highlights()
        phase = 0
        if self._game_phase == 2:
            phase = 0  # broj koraka do druge faze
        else:
            phase = self._white_left + self._black_left + 1
        st = Minimax(DEPTH)
        board = copy.deepcopy(self._placed)
        # print(st.minimax(board, (-4, -4), DEPTH, False, phase))
        st.alphabeta(board, (-4, -4), DEPTH, False, phase)
        if st.next_move[1] == -1:
            print('error')
        elif st.next_move[1] == -2:
            self._black_placed += 1
            self._black_left -= 1
        elif st.next_move[1] == -3:
            self._white_placed -= 1
        else:
            print('move')
        board2 = copy.deepcopy(self._placed)
        self._placed = updateboard(self._placed, st.next_move)
        if new_morris(board2, st.next_move) == -1:
            if self._game_phase == 2:
                phase = 0  # broj koraka do druge faze
            else:
                phase = self._white_left + self._black_left + 1
            board = copy.deepcopy(self._placed)
            st2 = Minimax(DEPTH)
            # st2.minimax(board, (-4, -4), DEPTH, False, phase, 1)
            st2.alphabeta(board, (-4, -4), DEPTH, False, phase, 1)
            self._white_placed -= 1
            self._highlighted[st2.next_move[0]] = True
            self._placed = updateboard(self._placed, st2.next_move)
        self.next_player()
