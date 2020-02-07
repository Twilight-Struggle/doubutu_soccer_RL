#!/usr/bin/env python
# coding: UTF-8

import numpy as np
import random
import copy
from enum import Enum, auto

BOARD_HEIGHT = 5
BOARD_WIDTH = 3


class PlayPos(Enum):
    FRONTPLAYER = auto()
    BACKPLAYER = auto()


class PieceID(Enum):
    SARU_ID = auto()
    RISU_ID = auto()
    USAGI_ID = auto()
    OYASARU_ID = auto()
    BALL_ID = auto()


class Piece():
    def __init__(self, spiece, powe=None):
        self.spiece = spiece
        self.power = powe
        if self.spiece == PieceID.SARU_ID:
            self.kick_to = np.array([(1, 1), (1, -1), (-1, 0), (2, 2), (2, -2),
                                     (-2, 0)])
            if self.power == PlayPos.FRONTPLAYER:
                self.identity = "さ"
            else:
                self.identity = "サ"
        if self.spiece == PieceID.OYASARU_ID:
            self.kick_to = np.array([(1, 1), (1, -1), (-1, 0), (2, 2), (2, -2),
                                     (-2, 0)])
            if self.power == PlayPos.FRONTPLAYER:
                self.identity = "お"
            else:
                self.identity = "オ"
        elif self.spiece == PieceID.RISU_ID:
            self.kick_to = np.array([(1, 0), (2, 0), (-1, 0), (-2, 0), (0, 1),
                                     (0, 2), (0, -1), (0, -2)])
            if self.power == PlayPos.FRONTPLAYER:
                self.identity = "り"
            else:
                self.identity = "リ"
        elif self.spiece == PieceID.USAGI_ID:
            self.kick_to = np.array([(1, 0), (2, 0), (0, 1), (0, 2), (0, -1),
                                     (0, -2), (1, 1), (2, 2), (1, -1),
                                     (2, -2)])
            if self.power == PlayPos.FRONTPLAYER:
                self.identity = "う"
            else:
                self.identity = "ウ"


class Act():
    def __init__(self, move, kick):
        self.move_command = move
        self.kick_command = kick


class Board:
    def __init__(self, front, back, tn=PlayPos.FRONTPLAYER, cell=None):
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
            self.P_now_player = self.P_front if self.turn == PlayPos.FRONTPLAYER else self.P_back
            reset_flag = False

        self.S_ball = Piece(PieceID.BALL_ID)
        self.S_oyasaru_f = Piece(PieceID.OYASARU_ID, PlayPos.FRONTPLAYER)
        self.S_saru_f = Piece(PieceID.SARU_ID, PlayPos.FRONTPLAYER)
        self.S_risu_f = Piece(PieceID.RISU_ID, PlayPos.FRONTPLAYER)
        self.S_usa_f = Piece(PieceID.USAGI_ID, PlayPos.FRONTPLAYER)
        self.front_piece = {
            "さ": self.S_saru_f,
            "り": self.S_risu_f,
            "う": self.S_usa_f,
            "お": self.S_oyasaru_f
        }

        self.S_oyasaru_s = Piece(PieceID.OYASARU_ID, PlayPos.BACKPLAYER)
        self.S_saru_s = Piece(PieceID.SARU_ID, PlayPos.BACKPLAYER)
        self.S_risu_s = Piece(PieceID.RISU_ID, PlayPos.BACKPLAYER)
        self.S_usa_s = Piece(PieceID.USAGI_ID, PlayPos.BACKPLAYER)
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
            self.turn = PlayPos.FRONTPLAYER if random.random(
            ) >= 0.5 else PlayPos.BACKPLAYER
            self.P_now_player = self.P_front if self.turn == PlayPos.FRONTPLAYER else self.P_back
        else:
            for i in range(BOARD_HEIGHT):
                for j in range(BOARD_WIDTH):
                    obj = self.cells[i][j]
                    if obj is not None:
                        if obj.spiece == PieceID.SARU_ID:
                            if obj.power == PlayPos.FRONTPLAYER:
                                self.cells[i][j] = self.S_saru_f
                            else:
                                self.cells[i][j] = self.S_saru_s
                        elif obj.spiece == PieceID.USAGI_ID:
                            if obj.power == PlayPos.FRONTPLAYER:
                                self.cells[i][j] = self.S_usa_f
                            else:
                                self.cells[i][j] = self.S_usa_s
                        elif obj.spiece == PieceID.RISU_ID:
                            if obj.power == PlayPos.FRONTPLAYER:
                                self.cells[i][j] = self.S_risu_f
                            else:
                                self.cells[i][j] = self.S_risu_s
                        elif obj.spiece == PieceID.OYASARU_ID:
                            if obj.power == PlayPos.FRONTPLAYER:
                                self.cells[i][j] = self.S_oyasaru_f
                            else:
                                self.cells[i][j] = self.S_oyasaru_s
                        elif obj.spiece == PieceID.BALL_ID:
                            self.cells[i][j] = self.S_ball

    def where_you(self, piece):
        arr = np.array(self.cells)
        pos = []
        for nd in np.where(arr == piece):
            if len(nd) != 0:
                pos.append(nd[0])
        return tuple(pos)

    def piece_can_move(self, piece):
        my_place = self.where_you(piece)
        if len(my_place) == 0:
            return None, None
        legal_l = []
        ball_legal = None
        if piece.spiece == PieceID.OYASARU_ID:
            for dx in range(-2, 3, 1):
                for dy in range(-2, 3, 1):
                    new_x = my_place[0] + dx
                    new_y = my_place[1] + dy
                    if 0 <= new_x <= 4 and 0 <= new_y <= 2:
                        if self.cells[new_x][new_y] is None:
                            legal_l.append((new_x, new_y))
                        elif self.cells[new_x][
                                new_y].spiece == PieceID.BALL_ID:
                            ball_legal = (new_x, new_y)
        else:
            for dx in range(-1, 2, 1):
                for dy in range(-1, 2, 1):
                    new_x = my_place[0] + dx
                    new_y = my_place[1] + dy
                    if 0 <= new_x <= 4 and 0 <= new_y <= 2:
                        if self.cells[new_x][new_y] is None:
                            legal_l.append((new_x, new_y))
                        elif self.cells[new_x][
                                new_y].spiece == PieceID.BALL_ID:
                            ball_legal = (new_x, new_y)
        return legal_l, ball_legal

    def piece_can_kick(self, piece, fromhere, tempboard):
        kick_to = piece.kick_to
        fromhere = np.array(fromhere)
        kick_l = []
        if self.turn == PlayPos.BACKPLAYER:
            kick_to = -1 * kick_to
        for kick in kick_to:
            dist = fromhere + kick
            if -1 <= dist[0] <= 5 and 0 <= dist[1] <= 2:
                if dist[0] == -1 or dist[0] == 5:
                    kick_l.append(list(dist))
                elif tempboard[dist[0]][dist[1]] is None:
                    kick_l.append(list(dist))
                elif tempboard[dist[0]][dist[1]] == 1:
                    pass
                elif tempboard[dist[0]][dist[1]].power == self.turn:
                    temppiece = tempboard[dist[0]][dist[1]]
                    tempboard[dist[0]][dist[1]] = 1
                    for oup in self.piece_can_kick(temppiece, tuple(dist),
                                                   tempboard):
                        tl = []
                        opve = np.array(oup)
                        if opve.ndim == 2:
                            tl = list(dist) + oup
                        else:
                            tl.append(list(dist))
                            tl.append(oup)
                        kick_l.append(tl)

    def piece_legal_move(self, piece):
        acts = []
        legal_l, ball_legal = self.piece_can_move(piece)
        if legal_l is not None:
            for i, spot in enumerate(legal_l):
                legal_l[i] = spot + (piece.identity, )
            for lem in legal_l:
                act = Act(lem, None)
                acts.append(act)

        if ball_legal is not None:
            tempcell = copy.deepcopy(self.cells)
            kicker_place = self.where_you(piece)
            tempcell[kicker_place[0]][kicker_place[1]] = None
            tempcell[ball_legal[0]][ball_legal[1]] = 1
            rets = self.piece_can_kick(piece, ball_legal, tempcell)
