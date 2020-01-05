# coding: UTF-8

import random

FRONTPLAYER = 0
BACKPLAYER = 1
BOARD_WIDTH = 3
BOARD_HEIGHT = 5


def printn(inp):
    print(inp, end="")


class Player:
    def __init__(self):
        pass

    def parse_board(self, Board, turnplayer):
        cells = []
        if turnplayer == BACKPLAYER:
            for i in range(BOARD_HEIGHT):
                cells.append(
                    [i for i in Board.cells[BOARD_HEIGHT - 1 - i][::-1]])
        else:
            cells = Board.cells
        return cells

    def parse_action(self, legal, turnplayer):
        parsed_legalmoves = []
        if turnplayer == BACKPLAYER:
            for action in legal:
                move_command = action[0]
                kick_commands = action[1]
                piece_dict = {"サ": "さ", "リ": "り", "ウ": "う", "オ": "お"}
                new_move_command = [
                    BOARD_HEIGHT - 1 - move_command[0],
                    BOARD_WIDTH - 1 - move_command[1],
                    piece_dict[move_command[2]]
                ]
                new_kick_commands = None
                if kick_commands is not None:
                    new_kick_commands = []
                    for kick_to in kick_commands:
                        if kick_to is not None:
                            new_kick_to = [
                                BOARD_HEIGHT - 1 - kick_to[0],
                                BOARD_WIDTH - 1 - kick_to[1]
                            ]
                        else:
                            new_kick_to = None
                        new_kick_commands.append(new_kick_to)
                new_action = [new_move_command, new_kick_commands]
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
            for i, move in enumerate(legalmoves):
                print(str(i) + '):' + str(move))
            tmp = input()
            try:
                inp = int(tmp)
                ret = legalmoves[inp]
                break
            except Exception:
                pass
        return ret

    def getGameResult(self, Board, winner=None):
        if winner == FRONTPLAYER:
            print("front player wins!")
        elif winner == BACKPLAYER:
            print("back player wins!")


class Random(Player):
    def __init__(self):
        pass

    def action(self, Board, legalmoves):
        not_lose = []
        legalmoves_p = self.parse_action(legalmoves, Board.turn_player())
        for i, move in enumerate(legalmoves_p):
            kick_commands = move[1]
            if kick_commands is None:
                not_lose.append(i)
            else:
                lose_flag = False
                for last_stop in kick_commands[::-1]:
                    if last_stop is not None:
                        if last_stop[0] == -1:
                            lose_flag = True
                        elif last_stop[0] == 5:
                            return legalmoves[i]
                        break
                if not lose_flag:
                    not_lose.append(i)
        ret_index = not_lose[random.randrange(len(not_lose))]
        return legalmoves[ret_index]


class MonteCarlo(Player):
    def __init__(self):
        super().__init__()

    def policy(self, Board, legalmoves):
        not_lose = []
        legalmoves_p = self.parse_action(legalmoves, Board.turn_player())
        for i, move in enumerate(legalmoves_p):
            kick_commands = move[1]
            if kick_commands is None:
                not_lose.append(i)
            else:
                lose_flag = False
                for last_stop in kick_commands[::-1]:
                    if last_stop is not None:
                        if last_stop[0] == -1:
                            lose_flag = True
                        elif last_stop[0] == 5:
                            return legalmoves[i]
                        break
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
        tempboard = Board.clone()
        myturn = tempboard.turn_player()
        success, winner = tempboard.action_parser(act)
        if winner is not None:
            if winner == myturn:
                return 1
            else:
                return -1
        while True:
            legal_moves_l = tempboard.legal_moves()
            while True:
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
        n = 100
        for i, act in enumerate(legalmoves):
            scores[i] = 0
            for j in range(n):
                scores[i] += self.trial(Board, act)
            scores[i] /= n

        max_score = max(scores.values())
        for i, v in scores.items():
            if v == max_score:
                return legalmoves[i]
