#!/usr/bin/env python
# coding: UTF-8

from enum import Enum, auto
import random
import numpy as np
import copy

BOARD_HEIGHT = 5
BOARD_WIDTH = 3


class PlayPos(Enum):
    FRONTPLAYER = auto()
    BACKPLAYER = auto()


def playpos_opponent(playpos):
    if playpos == PlayPos.FRONTPLAYER:
        return PlayPos.BACKPLAYER
    elif playpos == PlayPos.BACKPLAYER:
        return PlayPos.FRONTPLAYER


# move_command = [(x, y, "さ")]
# kick_command = [[x, y], [a, b]]
class Act():
    def __init__(self, move, kick):
        self.move_command = move
        self.kick_command = kick

    def is_same(self, aite):
        if self.move_command == aite.move_command and self.kick_command == aite.kick_command:
            return True
        else:
            return False


def list_to_tuple(_list):
    t = ()
    for e in _list:
        if isinstance(e, list):
            t += (list_to_tuple(e), )
        else:
            t += (e, )
    return t


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

    def parse_board_cells(self):
        new_cells = []
        if self.turn == PlayPos.BACKPLAYER:
            piece_dict = {
                "サ": "さ",
                "リ": "り",
                "ウ": "う",
                "オ": "お",
                "さ": "サ",
                "り": "リ",
                "う": "ウ",
                "お": "オ",
                "ボ": "ボ"
            }
            for i in range(BOARD_HEIGHT):
                yokocell = self.cells[BOARD_HEIGHT - 1 - i]
                newyokocell = []
                for nakami in yokocell[::-1]:
                    if nakami is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(piece_dict[nakami.identity])
                new_cells.append(newyokocell)
        else:
            for i in range(BOARD_HEIGHT):
                newyokocell = []
                for j in range(BOARD_WIDTH):
                    if self.cells[i][j] is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(self.cells[i][j].identity)
                new_cells.append(newyokocell)
        return new_cells

    def tensor_state_parsed(self):
        parsed_cells = self.parse_board_cells()
        tensored_board = np.empty((9, 5, 3), dtype=np.float32)
        piece_list = ["さ", "り", "う", "お", "サ", "リ", "ウ", "オ", "ボ"]
        for i in range(9):
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    if parsed_cells[y][x] == piece_list[i]:
                        tensored_board[i][y][x] = 1
                    else:
                        tensored_board[i][y][x] = 0
        return tensored_board

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

    def parse_legal_moves(self):
        parsed_legalmoves = []
        if self.turn == PlayPos.BACKPLAYER:
            legal = self.legal_moves()
            for action in legal:
                piece_dict = {"サ": "さ", "リ": "り", "ウ": "う", "オ": "お"}
                new_move_command = [
                    BOARD_HEIGHT - 1 - action.move_command[0],
                    BOARD_WIDTH - 1 - action.move_command[1],
                    piece_dict[action.move_command[2]]
                ]
                new_kick_commands = None
                if action.kick_command is not None:
                    new_kick_commands = []
                    for kick_to in action.kick_command:
                        if kick_to is not None:
                            new_kick_to = [
                                BOARD_HEIGHT - 1 - kick_to[0],
                                BOARD_WIDTH - 1 - kick_to[1]
                            ]
                        else:
                            new_kick_to = None
                        new_kick_commands.append(new_kick_to)
                new_action = Act(new_move_command, new_kick_commands)
                parsed_legalmoves.append(new_action)
        else:
            parsed_legalmoves = self.legal_moves()
        return parsed_legalmoves

    # actionのnumはparsedされ、action自体はそのまま
    def legalmoves_to_num_parsed(self):
        legalmoves_num_act_dict = {}
        legalmoves = self.legal_moves()
        if not legalmoves:
            old_place_num = 15
            move_to_num = 15
            kick_to_num = 15
            action_num = old_place_num * 288 + move_to_num * 18 + kick_to_num
            legalmoves_num_act_dict[action_num] = None
            return legalmoves_num_act_dict
        piece_dict = self.front_piece if self.turn == PlayPos.FRONTPLAYER else self.back_piece
        for action in legalmoves:
            S_move_ready = piece_dict[action.move_command[2]]
            old_place = self.where_you(S_move_ready)
            old_place_num = old_place[0] * 3 + old_place[1]
            move_to = (action.move_command[0], action.move_command[1])
            move_to_num = move_to[0] * 3 + move_to[1]
            if action.kick_command is None:
                kick_to_num = 15
            else:
                kick_to = action.kick_command[-1]
                if kick_to[0] == -1:
                    kick_to_num = 16 if self.turn == PlayPos.FRONTPLAYER else 17
                elif kick_to[0] == 5:
                    kick_to_num = 17 if self.turn == PlayPos.FRONTPLAYER else 16
                else:
                    kick_to_num = kick_to[0] * 3 + kick_to[1]
            if self.turn == PlayPos.BACKPLAYER:
                old_place_num = 14 - old_place_num if 0 <= old_place_num <= 14 else old_place_num
                move_to_num = 14 - move_to_num if 0 <= move_to_num <= 14 else move_to_num
                kick_to_num = 14 - kick_to_num if 0 <= kick_to_num <= 14 else kick_to_num
            action_num = old_place_num * 288 + move_to_num * 18 + kick_to_num
            if action_num not in legalmoves_num_act_dict:
                legalmoves_num_act_dict[action_num] = action
        return legalmoves_num_act_dict

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


class DQNenv:
    def __init__(self):
        self.Board = Board()
        self.Board.reset()
        self.legalmoves_num_act_dict = self.Board.legalmoves_to_num_parsed()

    def reset(self):
        self.Board.reset()
        self.legalmoves_num_act_dict = self.Board.legalmoves_to_num_parsed()

    # ボードの状態をnumpy配列で表す。
    # board.cell → np.narray
    # 下側を自陣、上側を敵陣と固定
    # 0ch:自さ, 1ch:自り, 2ch:自う, 3ch:自お,
    # 4ch:敵サ, 5ch:敵リ, 6ch:敵ウ, 7ch:敵オ, 8ch:ボ
    def tensor_state(self, board_cells):
        tensored_board = np.empty((9, 5, 3), dtype=np.float32)
        piece_list = ["さ", "り", "う", "お", "サ", "リ", "ウ", "オ", "ボ"]
        for i in range(9):
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    if board_cells[y][x] == piece_list[i]:
                        tensored_board[i][y][x] = 1
                    else:
                        tensored_board[i][y][x] = 0
        return tensored_board

    def tensor_state_parsed(self):
        cells = []
        if self.Board.turn == PlayPos.BACKPLAYER:
            piece_dict = {
                "サ": "さ",
                "リ": "り",
                "ウ": "う",
                "オ": "お",
                "さ": "サ",
                "り": "リ",
                "う": "ウ",
                "お": "オ",
                "ボ": "ボ"
            }
            for i in range(BOARD_HEIGHT):
                yokocell = self.Board.cells[BOARD_HEIGHT - 1 - i]
                newyokocell = []
                for nakami in yokocell[::-1]:
                    if nakami is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(piece_dict[nakami.identity])
                cells.append(newyokocell)
        else:
            for i in range(BOARD_HEIGHT):
                newyokocell = []
                for j in range(BOARD_WIDTH):
                    if self.Board.cells[i][j] is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(self.Board.cells[i][j].identity)
                cells.append(newyokocell)
        return self.tensor_state(cells)

    def legalmoves(self):
        return self.legalmoves_num_act_dict

    def step(self, tensored_action):
        now_turn = self.Board.turn
        if len(self.legalmoves_num_act_dict) == 0:
            action = None
        else:
            action = self.legalmoves_num_act_dict[tensored_action]
        success, winner = self.Board.action_parser(action)
        if success is False:
            print("Irritating input!")
            return None, None, None, None
        if winner is not None:
            if now_turn == winner:
                reward = 1
            else:
                reward = -1
            next_state = None
            next_action = None
            done = True
            skip_turn = False
        else:
            self.legalmoves_num_act_dict = self.Board.legalmoves_to_num_parsed(
            )
            reward = 0
            next_state = self.tensor_state_parsed()
            next_action = list(self.legalmoves_num_act_dict.keys())
            done = False
            skip_turn = False if len(
                self.legalmoves_num_act_dict) != 0 else True

        return next_state, next_action, reward, done, skip_turn


class BattleEnv:
    def __init__(self, frontman, backman):
        self.Board = Board()
        self.Board.reset()
        self.front = frontman
        self.back = backman

    def progress(self):
        while True:
            #self.Board.display()
            if self.Board.turn == PlayPos.FRONTPLAYER:
                now_player = self.front
            elif self.Board.turn == PlayPos.BACKPLAYER:
                now_player = self.back
            while True:
                if len(self.Board.legal_moves()) == 0:
                    action = None
                else:
                    action = now_player.action(self.Board)
                success, winner = self.Board.action_parser(action)
                if success is True:
                    break
            if winner is not None:
                if winner == PlayPos.FRONTPLAYER:
                    print("Front Player wins!")
                else:
                    print("Back Player wins!")
                return winner

    def reset(self):
        self.Board.reset()


if __name__ == "__main__":
    env = DQNenv()
    while True:
        env.Board.display()
        legalmove = env.legalmoves()
        legalnum = list(legalmove.keys())
        print(legalnum)
        while True:
            tmp = input()
            try:
                ret = int(tmp)
            except Exception:
                pass
            _, _, _, done = env.step(ret)
            if done is not None:
                break
        if done:
            break
