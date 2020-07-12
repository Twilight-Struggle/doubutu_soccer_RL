# coding: UTF-8

import random
from includes import Act
from includes import PlayPos
from includes import list_to_tuple
from includes import playpos_opponent
import includes

import sys
from itertools import chain
from collections import deque


def compute_object_size(o, handlers={}):
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {
        tuple: iter,
        list: iter,
        deque: iter,
        dict: dict_handler,
        set: iter,
        frozenset: iter,
    }
    all_handlers.update(handlers)  # user handlers take precedence
    seen = set()  # track which object id's have already been seen
    default_size = sys.getsizeof(
        0)  # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:  # do not double count the same object
            return 0
        seen.add(id(o))
        s = sys.getsizeof(o, default_size)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)


BOARD_WIDTH = 3
BOARD_HEIGHT = 5


def printn(inp):
    print(inp, end="")


class Player:
    def __init__(self):
        pass

    def parse_board_original(self, Board, turnplayer):
        cells = []
        if turnplayer == PlayPos.BACKPLAYER:
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
                yokocell = Board.cells[BOARD_HEIGHT - 1 - i]
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
                    if Board.cells[i][j] is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(Board.cells[i][j].identity)
                cells.append(newyokocell)
        return cells

    def parse_board(self, Board, turnplayer):
        cells = []
        piece_number_dict = {
            "さ": 0,
            "り": 1,
            "う": 2,
            "お": 3,
            "サ": 4,
            "リ": 5,
            "ウ": 6,
            "オ": 7,
            "ボ": 8,
        }
        if turnplayer == PlayPos.BACKPLAYER:
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
                yokocell = Board.cells[BOARD_HEIGHT - 1 - i]
                newyokocell = []
                for nakami in yokocell[::-1]:
                    if nakami is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(
                            piece_number_dict[piece_dict[nakami.identity]])
                cells.append(newyokocell)
        else:
            for i in range(BOARD_HEIGHT):
                newyokocell = []
                for j in range(BOARD_WIDTH):
                    if Board.cells[i][j] is None:
                        newyokocell.append(None)
                    else:
                        newyokocell.append(
                            piece_number_dict[Board.cells[i][j].identity])
                cells.append(newyokocell)
        return cells

    def parse_action(self, legal, turnplayer):
        parsed_legalmoves = []
        if turnplayer == PlayPos.BACKPLAYER:
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
            parsed_legalmoves = legal
        return parsed_legalmoves

    def action(self, Board, legalmoves):
        pass

    def getGameResult(self, Board, winner=None):
        pass


class Human(Player):
    def __init__(self):
        pass

    def action(self, Board, legalmoves):
        while True:
            print("合法手")
            for i, action in enumerate(legalmoves):
                printn(str(i) + '):')
                printn(action.move_command)
                printn(" ")
                print(action.kick_command)
            tmp = input()
            try:
                inp = int(tmp)
                ret = legalmoves[inp]
                break
            except Exception:
                pass
        return ret

    def getGameResult(self, Board, winner=None):
        if winner == PlayPos.FRONTPLAYER:
            print("front player wins!")
        elif winner == PlayPos.BACKPLAYER:
            print("back player wins!")


class Random(Player):
    def __init__(self):
        pass

    def action(self, Board, legalmoves):
        not_lose = []
        legalmoves_p = self.parse_action(legalmoves, Board.turn)
        for i, action in enumerate(legalmoves_p):
            if action.kick_command is None:
                not_lose.append(i)
            else:
                lose_flag = False
                last_stop = action.kick_command[-1]
                if last_stop[0] == -1:
                    lose_flag = True
                elif last_stop[0] == 5:
                    return legalmoves[i]
                if not lose_flag:
                    not_lose.append(i)
        ret_index = not_lose[random.randrange(len(not_lose))]
        return legalmoves[ret_index]


class MonteCarlo(Player):
    def __init__(self):
        super().__init__()

    def policy(self, Board, legalmoves):
        not_lose = []
        legalmoves_p = self.parse_action(legalmoves, Board.turn)
        for i, action in enumerate(legalmoves_p):
            if action.kick_command is None:
                not_lose.append(i)
            else:
                lose_flag = False
                last_stop = action.kick_command[-1]
                if last_stop[0] == -1:
                    lose_flag = True
                elif last_stop[0] == 5:
                    return legalmoves[i]
                if not lose_flag:
                    not_lose.append(i)
        if len(not_lose) != 0:
            ret_index = not_lose[random.randrange(len(not_lose))]
        else:
            print("Error: not_lose is 0")
            print(legalmoves)
            print(legalmoves_p)
            ret_index = 0
        return legalmoves[ret_index]

    def trial(self, Board, act):
        kaisu = 0
        tempboard = Board.clone()
        myturn = tempboard.turn
        success, winner = tempboard.action_parser(act)
        if not success:
            print("act is not recieved")
        if winner is not None:
            if winner == myturn:
                return 10
            else:
                return -10
        while True:
            kaisu += 1
            legal_moves_l = tempboard.legal_moves()
            if len(legal_moves_l) == 0:
                print("trial legalmove is 0:kaisu is {}".format(kaisu))
                tempboard.display()
                print(tempboard.turn)
            while True:
                if len(legal_moves_l) == 0:
                    action = None
                else:
                    action = self.policy(tempboard, legal_moves_l)
                success, winner = tempboard.action_parser(action)
                if success is True:
                    break
                else:
                    print("fuck")
            if winner is not None:
                if winner == myturn:
                    return 1
                else:
                    return -1

    def action(self, Board, legalmoves):
        scores = {}
        n = 50
        for i, act in enumerate(legalmoves):
            scores[i] = 0
            for j in range(n):
                scores[i] += self.trial(Board, act)
            scores[i] /= n

        max_score = max(scores.values())
        for i, v in scores.items():
            if v == max_score:
                return legalmoves[i]


class Qlearning(Player):
    def __init__(self, playpos, qtable, e=0.2, alpha=0.2):
        self.last_board = None
        self.Qtable = qtable if qtable is not None else {}
        self.last_action_parsed = None
        self.alpha = alpha
        self.gammm = 0.9
        self.e = e
        self.playpos = playpos

    def policy(self, Board):
        self.last_board = Board.clone()
        legal_move_l = self.last_board.legal_moves()
        legal_move_parse = self.parse_action(legal_move_l,
                                             self.last_board.turn)
        last_board_cells = self.parse_board(self.last_board,
                                            self.last_board.turn)

        if random.random() < self.e:
            retindex = random.randrange(len(legal_move_l))
            self.last_action_parsed = legal_move_parse[retindex]
            return legal_move_l[retindex]
        Qvaluelist = [
            self.getQvalue(last_board_cells, action)
            for action in legal_move_parse
        ]
        maxQvalue = max(Qvaluelist)

        if Qvaluelist.count(maxQvalue) > 1:
            best_option = [
                i for i in range(len(legal_move_parse))
                if Qvaluelist[i] == maxQvalue
            ]
            best_index = random.choice(best_option)
        else:
            best_index = Qvaluelist.index(maxQvalue)

        self.last_action_parsed = legal_move_parse[best_index]
        return legal_move_l[best_index]

    def getQvalue(self, boardcells, Act):
        gotQvalue = self.Qtable.get(
            (list_to_tuple(boardcells), Act.move_command, Act.kick_command))
        if gotQvalue is None:
            self.Qtable[(list_to_tuple(boardcells), Act.move_command,
                         Act.kick_command)] = 1
            gotQvalue = 1
            includes.fuckinglobal += 1
        else:
            includes.fuckinglobal2 += 1
        print("Used key byte:{}".format(
            compute_object_size((list_to_tuple(boardcells), Act.move_command,
                                 Act.kick_command))))
        return gotQvalue

    def getGameResult(self, Board, winner):
        last_board_cells_parsed = self.parse_board(self.last_board,
                                                   self.last_board.turn)
        if winner is None:
            self.learn(last_board_cells_parsed, self.last_action_parsed, 0,
                       Board, winner)
        else:
            if winner == self.playpos:
                self.learn(last_board_cells_parsed, self.last_action_parsed, 1,
                           Board, winner)
                #print("yeah!")
            else:
                self.learn(last_board_cells_parsed, self.last_action_parsed,
                           -1, Board, winner)
                #print("fuck")
            self.last_action_parsed = None
            self.last_board = None

    def learn(self, Qscells, Act, reward, Qs1Board, winner):
        Qs = self.getQvalue(Qscells, Act)
        if winner is not None:
            maxQs1 = 0
        else:
            Qs1cells = self.parse_board(Qs1Board, Qs1Board.turn)
            if len(Qs1Board.legal_moves()) == 0:
                maxQs1 = 0
                reward = -0.5
            else:
                maxQs1 = max([
                    self.getQvalue(Qs1cells, action)
                    for action in Qs1Board.legal_moves()
                ])
        self.Qtable[(list_to_tuple(Qscells), Act.move_command,
                     Act.kick_command)] = Qs + self.alpha * (
                         (reward + self.gammm * maxQs1) - Qs)

    def action(self, Board, legalmoves):
        return self.policy(Board)


class Vlearning(Player):
    def __init__(self, playpos, vtable, e=0.1, alpha=0.2):
        self.last_board = None
        self.Vtable = vtable if vtable is not None else {}
        self.alpha = alpha
        self.gamma = 0.9
        self.e = e
        self.playpos = playpos

    def policy(self, Board):
        self.last_board = Board.clone()
        legal_move_l = self.last_board.legal_moves()
        # 一定の確率でランダムな手をうつ
        if random.random() < self.e:
            retindex = random.randrange(len(legal_move_l))
            return legal_move_l[retindex]

        # 現状態から遷移可能なすべての盤面を保存
        next_board_list_cells = []
        for legal_move in legal_move_l:
            temp_board = self.last_board.clone()
            temp_board.action_parser(legal_move)
            # 反転せずcell化してほしいので第2引数に自分のターンを指定
            next_board_list_cells.append(
                self.parse_board(temp_board,
                                 playpos_opponent(temp_board.turn)))

        # (遷移可能な盤面 + 相手のターン)　でテーブルを引く
        Vvaluelist = [
            self.getVvalue(next_board_cell,
                           playpos_opponent(self.last_board.turn))
            for next_board_cell in next_board_list_cells
        ]
        maxVvalue = max(Vvaluelist)

        if Vvaluelist.count(maxVvalue) > 1:
            best_option = [
                i for i in range(len(legal_move_l))
                if Vvaluelist[i] == maxVvalue
            ]
            best_index = random.choice(best_option)
        else:
            best_index = Vvaluelist.index(maxVvalue)

        return legal_move_l[best_index]

    def getVvalue(self, boardcells, turn):
        gotVvalue = self.Vtable.get((list_to_tuple(boardcells), turn))
        if gotVvalue is None:
            self.Vtable[(list_to_tuple(boardcells), turn)] = 1
            gotVvalue = 1
        print("Used key byte:{}".format(
            compute_object_size((list_to_tuple(boardcells), turn))))
        return gotVvalue

    def getGameResult(self, Board, winner):
        # 自分のターンで1手打ったときの学習
        if self.playpos != Board.turn:
            last_board_cells = self.parse_board(self.last_board, self.playpos)
            # 反転せずcell化してほしいので第2引数に自分のターンを指定
            board_cells = self.parse_board(Board, self.playpos)
            if winner is None:
                self.Vtable[(list_to_tuple(last_board_cells),
                             self.playpos)] = self.getVvalue(
                                 board_cells, Board.turn)
                self.last_board = Board
            else:
                if winner == self.playpos:
                    # 自分がゴールしたとき
                    self.Vtable[(list_to_tuple(last_board_cells),
                                 self.last_board.turn)] = 1
                else:
                    # 自分がオウンゴールしたとき
                    self.Vtable[(list_to_tuple(last_board_cells),
                                 self.last_board.turn)] = -1 * self.gamma
                self.last_board = None
        # 相手のターンで1手打たれたときの学習
        elif self.last_board is not None:
            # 反転せずcell化してほしいので第2引数に自分のターンを指定
            last_board_cells = self.parse_board(self.last_board, self.playpos)
            board_cells = self.parse_board(Board, self.playpos)
            Vs = self.getVvalue(last_board_cells, self.last_board.turn)
            if winner is None:
                self.Vtable[(
                    list_to_tuple(last_board_cells), self.last_board.turn
                )] = Vs + self.alpha * (
                    self.gamma * self.getVvalue(board_cells, Board.turn) - Vs)
                # self.last_board = Board 自分のターンのpolicyで設定するためなくて良い
            else:
                if winner == self.playpos:
                    # 相手がオウンゴールしたとき
                    self.Vtable[(
                        list_to_tuple(last_board_cells),
                        self.last_board.turn)] = Vs + self.alpha * (1 - Vs)
                else:
                    # 相手がゴールしたとき
                    self.Vtable[(
                        list_to_tuple(last_board_cells),
                        self.last_board.turn)] = Vs + self.alpha * (-1 - Vs)
                self.last_board = None

    def action(self, Board, legalmoves):
        return self.policy(Board)
