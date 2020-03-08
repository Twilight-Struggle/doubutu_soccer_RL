#!/usr/bin/env python
# coding: UTF-8

from enum import Enum, auto


class PlayPos(Enum):
    FRONTPLAYER = auto()
    BACKPLAYER = auto()


class Act():
    def __init__(self, move, kick):
        self.move_command = move
        self.kick_command = kick

    def is_same(self, aite):
        if self.move_command == aite.move_command and self.kick_command == aite.kick_command:
            return True
        else:
            return False
