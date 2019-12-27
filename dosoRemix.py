# coding: UTF-8

import numpy as np
import random
import copy
from pieceRemix import *
from playerRemix import *

FRONTPLAYER = 0
BACKPLAYER = 1
FRONTPLAYER_WIN = 2
BACKPLAYER_WIN = 3
BOARD_WIDTH = 3
BOARD_HEIGHT = 5
BALL_ID = 0
SARU_ID = 1
RISU_ID = 2
USAGI_ID = 3
OYASARU_ID = 4
'''
X 4
X 3
X 2
X 1
X 0 1 2
  Y
'''


def printn(inp):
    print(inp, end="")


class Board:
    def __init__(self, front, back, tn=FRONTPLAYER, cell=None):
        self.turn = tn
        self.P_front = front
        self.P_back = back

        if cell is None:
            self.cells = []
            for i in range(BOARD_HEIGHT):
                self.cells.append([None for i in range(BOARD_WIDTH)])
                reset_flag = True
        else:
            self.cells = cell
            reset_flag = False

        self.S_ball = BallPiece()
        self.S_oyasaru_f = OyasaruPiece(FRONTPLAYER)
        self.S_saru_f = SaruPiece(FRONTPLAYER, self.S_oyasaru_f)
        self.S_risu_f = RisuPiece(FRONTPLAYER)
        self.S_usa_f = UsagiPiece(FRONTPLAYER)
        self.front_piece = {
            "さ": self.S_saru_f,
            "り": self.S_risu_f,
            "う": self.S_usa_f,
            "お": self.S_oyasaru_f
        }

        self.S_oyasaru_s = OyasaruPiece(BACKPLAYER)
        self.S_saru_s = SaruPiece(BACKPLAYER, self.S_oyasaru_s)
        self.S_risu_s = RisuPiece(BACKPLAYER)
        self.S_usa_s = UsagiPiece(BACKPLAYER)
        self.back_piece = {
            "サ": self.S_saru_s,
            "リ": self.S_risu_s,
            "ウ": self.S_usa_s,
            "オ": self.S_oyasaru_s
        }
        self.reset(reset_flag)

    def reset(self, reset_flag=True):
        if reset_flag is True:
            self.cells[1][1] = self.S_saru_f
            self.cells[0][0] = self.S_usa_f
            self.cells[0][2] = self.S_risu_f
            self.cells[2][1] = self.S_ball
            self.cells[3][1] = self.S_saru_s
            self.cells[4][0] = self.S_risu_s
            self.cells[4][2] = self.S_usa_s
        else:
            for i in range(BOARD_HEIGHT):
                for j in range(BOARD_WIDTH):
                    obj = self.cells[i][j]
                    if obj is not None:
                        if obj.spiece == SARU_ID:
                            if obj.power == FRONTPLAYER:
                                self.cells[i][j] = self.S_saru_f
                            else:
                                self.cells[i][j] = self.S_saru_s
                        elif obj.spiece == USAGI_ID:
                            if obj.power == FRONTPLAYER:
                                self.cells[i][j] = self.S_usa_f
                            else:
                                self.cells[i][j] = self.S_usa_s
                        elif obj.spiece == RISU_ID:
                            if obj.power == FRONTPLAYER:
                                self.cells[i][j] = self.S_risu_f
                            else:
                                self.cells[i][j] = self.S_risu_s
                        elif obj.spiece == BALL_ID:
                            self.cells[i][j] = self.S_ball

        self.turn = FRONTPLAYER if random.random() >= 0.5 else BACKPLAYER
        self.P_now_player = self.P_front if self.turn == FRONTPLAYER else self.P_back

    def clone(self):
        return Board(self.P_front, self.P_back, self.turn,
                     copy.deepcopy(self.cells))

    def turn_piece_dict(self):
        if self.turn == FRONTPLAYER:
            return self.front_piece
        elif self.turn == BACKPLAYER:
            return self.back_piece

    def turn_player(self):
        return self.turn

    def display(self):
        nums = 4
        for side in self.cells[::-1]:
            printn("{}|".format(nums))
            for cel in side:
                if cel is not None:
                    printn(cel.to_string())
                else:
                    printn("　")
                printn("|")
            print()
            nums -= 1
        print(".  0  1  2")

    def legal_moves_child(self,
                          S_kicker,
                          ball_place,
                          ball_legal,
                          piece_dict,
                          first_kicker,
                          kick_command=[None, None, None],
                          itenum=0):
        legal_moves_l = []
        kick_l, kick_pas = self.S_ball.legal_move(S_kicker, ball_place,
                                                  first_kicker, self)
        if len(kick_l) != 0:
            for kick_to in kick_l:
                kick_command[itenum] = kick_to
                action = [ball_legal, kick_command[:]]
                legal_moves_l.append(action)
        if len(kick_pas) != 0:
            for kick_pass_to in kick_pas:
                ball_place = kick_pass_to
                S_kicker = self.cells[ball_place[0]][ball_place[1]]
                kick_command[itenum] = kick_pass_to
                legal_moves_l += self.legal_moves_child(
                    S_kicker, ball_place, ball_legal, piece_dict, first_kicker,
                    kick_command, itenum + 1)
        for pie in piece_dict.values():
            pie.kicked = False
        return legal_moves_l

    def legal_moves(self):
        legal_moves_l = []
        piece_dict = self.turn_piece_dict()
        for pie in piece_dict.values():
            legal_m, ball_legal = pie.legal_move(self)
            if legal_m is not None:
                for i, spot in enumerate(legal_m):
                    legal_m[i] = spot + (pie.to_string(), )
                for lem in legal_m:
                    action = [lem, None]
                    legal_moves_l.append(action)
            if ball_legal is not None:
                ball_legal = ball_legal + (pie.to_string(), )
                ball_place = np.array(self.S_ball.where_me(self))
                S_kicker = pie
                legal_moves_l += self.legal_moves_child(
                    S_kicker, ball_place, ball_legal, piece_dict, S_kicker,
                    [None, None, None])
        return legal_moves_l

    def action_parser(self, actions):
        # action = [move_command,([kick_commands]|None)]
        # move_command = [1,2,"さ"]
        # kick_commands = [[kick_to],([kick_to]|None),([kick_to]|None)]
        # kick_to = [1, 2]
        # legal_moveの返り値も変更
        legal_moves_l = self.legal_moves()
        if actions not in legal_moves_l:
            return False, None
        move_command = actions[0]
        kick_commands = actions[1]

        piece_fict = self.turn_piece_dict()
        S_move_ready = piece_fict[move_command[2]]
        move_to = (move_command[0], move_command[1])

        # 移動はaction_parser内で
        if kick_commands is None:
            old_place = S_move_ready.where_me(self)
            self.cells[old_place[0]][old_place[1]] = None
            self.cells[move_to[0]][move_to[1]] = S_move_ready
        else:
            # Game set 判定ループ
            for last_stop in kick_commands[::-1]:
                if last_stop is not None:
                    ball_to = last_stop
                    if last_stop[0] == -1:
                        return True, BACKPLAYER
                    elif last_stop[0] == 5:
                        return True, FRONTPLAYER
                    break
            old_place = S_move_ready.where_me(self)
            self.cells[old_place[0]][old_place[1]] = None
            self.cells[move_to[0]][move_to[1]] = S_move_ready
            self.cells[ball_to[0]][ball_to[1]] = self.S_ball

        self.S_saru_f.nari(self)
        self.S_saru_s.nari(self)

        if self.P_now_player == self.P_front:
            self.P_now_player = self.P_back
            self.turn = BACKPLAYER
        else:
            self.P_now_player = self.P_front
            self.turn = FRONTPLAYER

        return True, None


# Player class→Board class→Piece classの継承が最良か？
class DobutuEnv:
    def __init__(self, frontman, backman):
        self.Board = Board(frontman, backman)
        self.Board.reset()
        self.front = frontman
        self.back = backman

    def progress(self):
        while True:
            self.Board.display()
            legal_moves_l = self.Board.legal_moves()
            if self.Board.turn_player() == FRONTPLAYER:
                now_player = self.front
            elif self.Board.turn_player() == BACKPLAYER:
                now_player = self.back
            while True:
                actions = now_player.action(self.Board, legal_moves_l)
                success, winner = self.Board.action_parser(actions)
                if success is True:
                    break
            if winner is not None:
                self.front.getGameResult(self.Board, winner)
                self.back.getGameResult(self.Board, winner)
                break
            else:
                now_player.getGameResult(self.Board, winner)


if __name__ == "__main__":
    human = Human()
    rand = Random()
    env = DobutuEnv(human, rand)
    env.progress()
