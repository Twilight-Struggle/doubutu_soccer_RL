# coding: UTF-8

import numpy as np

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


class Piece:
    def __init__(self, powe):
        self.spiece = 100
        self.power = powe
        self.kicked = False

    def to_string(self):
        if self.spiece == BALL_ID:
            return "ボ"
        elif self.spiece == SARU_ID and self.power == FRONTPLAYER:
            return "さ"
        elif self.spiece == RISU_ID and self.power == FRONTPLAYER:
            return "り"
        elif self.spiece == USAGI_ID and self.power == FRONTPLAYER:
            return "う"
        elif self.spiece == OYASARU_ID and self.power == FRONTPLAYER:
            return "お"
        elif self.spiece == SARU_ID and self.power == BACKPLAYER:
            return "サ"
        elif self.spiece == RISU_ID and self.power == BACKPLAYER:
            return "リ"
        elif self.spiece == USAGI_ID and self.power == BACKPLAYER:
            return "ウ"
        elif self.spiece == OYASARU_ID and self.power == BACKPLAYER:
            return "オ"

    def where_me(self, board):
        arr = np.array(board.cells)
        pos = []
        for nd in np.where(arr == self):
            if len(nd) != 0:
                pos.append(nd[0])
        return tuple(pos)

    # ([合法手], ボールを蹴る合法手)を返す。
    def legal_move(self, board):
        my_place = self.where_me(board)
        if len(my_place) == 0:
            return None, None
        legal_l = []
        ball_legal = None
        for dx in range(-1, 2, 1):
            for dy in range(-1, 2, 1):
                new_x = my_place[0] + dx
                new_y = my_place[1] + dy
                if 0 <= new_x <= 4 and 0 <= new_y <= 2:
                    if board.cells[new_x][new_y] is None:
                        legal_l.append((new_x, new_y))
                    elif board.cells[new_x][new_y].spiece == BALL_ID:
                        ball_legal = (new_x, new_y)
        return legal_l, ball_legal


class BallPiece(Piece):
    def __init__(self, tn=100):
        super().__init__(tn)
        self.spiece = BALL_ID

    def legal_move(self, kicker, my_place, first_kicker, board):
        kick_to = []
        kick_l = []
        kick_pas = []
        if kicker.spiece == SARU_ID or kicker.spiece == OYASARU_ID:
            kick_to = np.array([(1, 1), (1, -1), (-1, 0), (2, 2), (2, -2),
                                (-2, 0)])
        elif kicker.spiece == RISU_ID:
            kick_to = np.array([(1, 0), (2, 0), (-1, 0), (-2, 0), (0, 1),
                                (0, 2), (0, -1), (0, -2)])
        elif kicker.spiece == USAGI_ID:
            kick_to = np.array([(1, 0), (2, 0), (0, 1), (0, 2), (0, -1),
                                (0, -2), (1, 1), (2, 2), (1, -1), (2, -2)])
        if board.turn == BACKPLAYER:
            kick_to = -1 * kick_to

        kicker.kicked = True
        for kick in kick_to:
            dist = my_place + kick
            if -1 <= dist[0] <= 5 and 0 <= dist[1] <= 2:
                if dist[0] == -1 or dist[0] == 5:
                    kick_l.append(tuple(dist))
                elif board.cells[dist[0]][dist[1]] is None or board.cells[
                        dist[0]][dist[1]] == first_kicker:
                    kick_l.append(tuple(dist))
                elif board.cells[dist[0]][
                        dist[1]].power == board.turn and board.cells[dist[0]][
                            dist[1]].kicked is False:
                    kick_pas.append(tuple(dist))
                    board.cells[dist[0]][dist[1]].kicked = True
        return kick_l, kick_pas


class SaruPiece(Piece):
    def __init__(self, powe, oyasaru):
        super().__init__(powe)
        self.spiece = SARU_ID
        self.oyasaru = oyasaru

    def nari(self, board):
        mypos = self.where_me(board)
        if len(mypos) != 0:
            if (mypos[0] == 4 and self.power == FRONTPLAYER) or (
                    mypos[0] == 0 and self.power == BACKPLAYER):
                self.board.cells[mypos[0]][mypos[1]] = self.oyasaru


class OyasaruPiece(Piece):
    def __init__(self, powe):
        super().__init__(powe)
        self.spiece = OYASARU_ID

    # ([合法手], ボールを蹴る合法手)を返す。
    def legal_move(self, board):
        my_place = self.where_me(board)
        if len(my_place) == 0:
            return None, None
        legal_l = []
        ball_legal = None
        for dx in range(-2, 3, 1):
            for dy in range(-2, 3, 1):
                new_x = my_place[0] + dx
                new_y = my_place[1] + dy
                if 0 <= new_x <= 4 and 0 <= new_y <= 2:
                    if self.board.cells[new_x][new_y] is None:
                        legal_l.append((new_x, new_y))
                    elif self.board.cells[new_x][new_y].spiece == BALL_ID:
                        ball_legal = (new_x, new_y)
        return legal_l, ball_legal


class RisuPiece(Piece):
    def __init__(self, powe):
        super().__init__(powe)
        self.spiece = RISU_ID


class UsagiPiece(Piece):
    def __init__(self, powe):
        super().__init__(powe)
        self.spiece = USAGI_ID
