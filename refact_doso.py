#!/usr/bin/env python
# coding: UTF-8

import numpy as np
import random
import copy
from includes import Act
from includes import PlayPos
from includes import list_to_tuple
from enum import Enum, auto

BOARD_HEIGHT = 5
BOARD_WIDTH = 3


def printn(inp):
    print(inp, end="")


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
        elif self.spiece == PieceID.BALL_ID:
            self.identity = "ボ"


class Board:
    def __init__(self, tn=PlayPos.FRONTPLAYER, cell=None):
        self.turn = tn

        if cell is None:
            self.cells = []
            for i in range(BOARD_HEIGHT):
                self.cells.append([None for i in range(BOARD_WIDTH)])
                reset_flag = True
        else:
            self.cells = cell
            #self.P_now_player = self.P_front if self.turn == PlayPos.FRONTPLAYER else self.P_back
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
            for i in range(BOARD_HEIGHT):
                for j in range(BOARD_WIDTH):
                    self.cells[i][j] = None
            self.cells[1][1] = self.S_saru_f
            self.cells[0][0] = self.S_usa_f
            self.cells[0][2] = self.S_risu_f
            self.cells[2][1] = self.S_ball
            self.cells[3][1] = self.S_saru_s
            self.cells[4][0] = self.S_risu_s
            self.cells[4][2] = self.S_usa_s
            self.turn = PlayPos.FRONTPLAYER if random.random(
            ) >= 0.5 else PlayPos.BACKPLAYER
            #self.P_now_player = self.P_front if self.turn == PlayPos.FRONTPLAYER else self.P_back
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

    def clone(self):
        return Board(self.turn, copy.deepcopy(self.cells))

    def display(self):
        nums = 4
        for side in self.cells[::-1]:
            printn("{}|".format(nums))
            for cel in side:
                if cel is not None:
                    printn(cel.identity)
                else:
                    printn("　")
                printn("|")
            print()
            nums -= 1
        print(".  0  1  2")

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
                    templ = []
                    templ.append(list(dist))
                    kick_l.append(templ)
                elif tempboard[dist[0]][dist[1]] is None:
                    templ = []
                    templ.append(list(dist))
                    kick_l.append(templ)
                elif tempboard[dist[0]][dist[1]] == 1:
                    pass
                elif tempboard[dist[0]][dist[1]].power == self.turn:
                    temppiece = tempboard[dist[0]][dist[1]]
                    tempboard[dist[0]][dist[1]] = 1
                    for oup in self.piece_can_kick(temppiece, tuple(dist),
                                                   tempboard):
                        templ = []
                        templ.append(list(dist))
                        tl = templ + oup
                        kick_l.append(tl)
        return kick_l

    # return [Act, Act, Act,...]
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
            kicks = self.piece_can_kick(piece, ball_legal, tempcell)
            ball_legal = ball_legal + (piece.identity, )
            for kick in kicks:
                kickt = list_to_tuple(kick)
                act = Act(ball_legal, kickt)
                acts.append(act)
        return acts

    def legal_moves(self):
        piece_dict = self.front_piece if self.turn == PlayPos.FRONTPLAYER else self.back_piece
        acts = []
        for pie in piece_dict.values():
            acts = acts + self.piece_legal_move(pie)
        return acts

    def action_parser(self, action):
        if action is None:
            if self.turn == PlayPos.FRONTPLAYER:
                self.turn = PlayPos.BACKPLAYER
            else:
                self.turn = PlayPos.FRONTPLAYER
            return True, None
        legalmoves = self.legal_moves()
        existflag = False
        for l in legalmoves:
            if l.is_same(action):
                existflag = True
        if not existflag:
            return False, None
        piece_dict = self.front_piece if self.turn == PlayPos.FRONTPLAYER else self.back_piece
        S_move_ready = piece_dict[action.move_command[2]]
        move_to = (action.move_command[0], action.move_command[1])

        # 移動はaction_parser内で
        if action.kick_command is None:
            old_place = self.where_you(S_move_ready)
            self.cells[old_place[0]][old_place[1]] = None
            self.cells[move_to[0]][move_to[1]] = S_move_ready
        else:
            last_stop = action.kick_command[-1]
            if last_stop[0] == -1:
                return True, PlayPos.BACKPLAYER
            elif last_stop[0] == 5:
                return True, PlayPos.FRONTPLAYER
            old_place = self.where_you(S_move_ready)
            self.cells[old_place[0]][old_place[1]] = None
            self.cells[move_to[0]][move_to[1]] = S_move_ready
            self.cells[last_stop[0]][last_stop[1]] = self.S_ball

        Sarufpos = self.where_you(self.S_saru_f)
        if len(Sarufpos) != 0 and Sarufpos[0] == 4:
            self.cells[Sarufpos[0]][Sarufpos[1]] = self.S_oyasaru_f
        Saruspos = self.where_you(self.S_saru_s)
        if len(Saruspos) != 0 and Saruspos[0] == 0:
            self.cells[Saruspos[0]][Saruspos[1]] = self.S_oyasaru_s

        if self.turn == PlayPos.FRONTPLAYER:
            self.turn = PlayPos.BACKPLAYER
        else:
            self.turn = PlayPos.FRONTPLAYER

        return True, None


class DobutuEnv:
    def __init__(self, frontman, backman):
        self.Board = Board()
        self.Board.reset()
        self.front = frontman
        self.back = backman

    def progress(self):
        while True:
            self.Board.display()
            legal_moves_l = self.Board.legal_moves()
            if self.Board.turn == PlayPos.FRONTPLAYER:
                now_player = self.front
            elif self.Board.turn == PlayPos.BACKPLAYER:
                now_player = self.back
            while True:
                if len(legal_moves_l) == 0:
                    action = None
                else:
                    action = now_player.action(self.Board, legal_moves_l)
                success, winner = self.Board.action_parser(action)
                if success is True:
                    break
            if winner is not None:
                self.front.getGameResult(self.Board, winner)
                self.back.getGameResult(self.Board, winner)
                return winner
            else:
                if len(legal_moves_l) != 0:
                    now_player.getGameResult(self.Board, winner)

    def reset(self):
        self.Board.reset()
