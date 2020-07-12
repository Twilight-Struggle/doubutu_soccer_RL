#!/usr/bin/env python
# coding: UTF-8

from enum import Enum, auto

fuckinglobal = 0
fuckinglobal2 = 0


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
