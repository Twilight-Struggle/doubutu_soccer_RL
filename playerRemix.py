# coding: UTF-8

import random
from includes import Act
from includes import PlayPos

BOARD_WIDTH = 3
BOARD_HEIGHT = 5


def printn(inp):
    print(inp, end="")


class Player:
    def __init__(self):
        pass

    def parse_board(self, Board, turnplayer):
        cells = []
        if turnplayer == PlayPos.BACKPLAYER:
            for i in range(BOARD_HEIGHT):
                cells.append(
                    [i for i in Board.cells[BOARD_HEIGHT - 1 - i][::-1]])
        else:
            cells = Board.cells
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
    def __init__(self, playpos, e=0.2, alpha=0.2):
        self.last_board = None
        self.Qtable = {}
        self.last_action_parsed = None
        self.alpha = alpha
        self.gammm = 0.9
        self.e = e
        self.playpos = playpos

    def policy(self, Board):
        self.last_board = Board.clone()
        legal_move_l = self.last_board.legal_moves()
        legal_move_parse = self.parse_action(legal_move_l,
                                             self.last_board.turnplayer)
        last_board_cells = self.parse_board(self.last_board,
                                            self.last_board.turnplayer)

        if random.random() < self.e:
            return legal_move_l[random.randrange(len(legal_move_l))]
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
        if self.Qtable.get(
            (boardcells, Act.move_command, Act.kick_command)) is None:
            self.Qtable[(boardcells, Act.move_command, Act.kick_command)] = 1
        return self.Qtable.get(
            (boardcells, Act.move_command, Act.kick_command))

    def getGameResult(self, Board, winner):
        last_board_cells_parsed = self.parse_board(self.last_board,
                                                   self.last_board.turnplayer)
        if winner is None:
            self.learn(last_board_cells_parsed, self.last_action_parsed, 0,
                       Board)
        else:
            if winner == self.playpos:
                self.learn(last_board_cells_parsed, self.last_action_parsed, 1,
                           Board)
            else:
                self.learn(last_board_cells_parsed, self.last_action_parsed,
                           -1, Board)
            self.last_action_parsed = None
            self.last_board = None

    def learn(self, Qscells, Act, reward, Qs1Board, winner):
        Qs = self.getQvalue(Qscells, Act)
        if winner is not None:
            maxQs1 = 0
        else:
            Qs1cells = self.parse_board(Qs1Board, Qs1Board.turnplayer)
            maxQs1 = max([
                self.getQvalue(Qs1cells, action)
                for action in Qs1Board.legal_moves()
            ])
        self.Qtable[(Qscells, Act.move_command, Act.kick_command
                     )] = Qs + self.alpha((reward + self.gammm * maxQs1) - Qs)

    def action(self, Board, legalmoves):
        return self.policy(Board)