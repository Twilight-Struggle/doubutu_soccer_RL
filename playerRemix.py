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

    def parse_board(self, Board):
        cells = []
        if self.power == BACKPLAYER:
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
        ret_index = not_lose[random.randrange(len(not_lose))]
        return legalmoves[ret_index]

    def trial(self, Board, act):


    def action(self, Board, legalmoves):
        scores = {}
        n = 100
        for act in legalmoves:
            scores[act] = 0
            for i in range(n):
                scores[act] += self.trial(self, Board, act)
            scores[act] /= n

        max_score = max(scores.values())
        for act, v in scores.items():
            if v == max_score:
                return act
