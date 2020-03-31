# coding: UTF-8

from includes import Act
from includes import PlayPos
from includes import list_to_tuple
import random
import numpy as np

from playerRemix import Player

BOARD_WIDTH = 3
BOARD_HEIGHT = 5
PIECENUM = 9


def Suironki(test):
    return 10


class DQN(Player):
    def tensored(self, cells):
        x = np.zeros((BOARD_HEIGHT, BOARD_WIDTH, PIECENUM)).astype(int)
        piece_dict = {
            "さ": 0,
            "り": 1,
            "う": 2,
            "お": 3,
            "サ": 4,
            "リ": 5,
            "ウ": 6,
            "オ": 7,
            "ボ": 8
        }
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if cells[i][j] is not None:
                    x[i][j][piece_dict[cells[i][j]]] = 1
        # if turn_playpos == PlayPos.FRONTPLAYER:
        #     x[0][1][9] = 1
        # elif turn_playpos == PlayPos.BACKPLAYER:
        #     x[4][1][9] = 1
        return x

    def action(self, Board, legalmoves):
        self.last_board = Board.clone()

        scores = {}
        for i, act in enumerate(legalmoves):
            tempboard = Board.clone()
            myturn = tempboard.turn
            success, winner = tempboard.action_parser(act)
            if not success:
                print("act is not recieved")
            if winner is not None:
                if winner == myturn:
                    scores[i] = 1
                else:
                    scores[i] = -1
            else:
                tensor_input = self.tensored(
                    self.parse_board(tempboard, tempboard.turn))
                scores[i] = Suironki(tensor_input)  ###

        max_score = max(scores.values())
        for i, v in scores.items():
            if v == max_score:
                act_index = i

        self.e = 0.2
        if random.random() < self.e:
            act_index = random.randrange(len(legalmoves))

        return legalmoves[act_index]