#!/usr/bin/env python
# coding: UTF-8

from refact_doso import DobutuEnv
from includes import PlayPos
import playerRemix

if __name__ == "__main__":
    human = playerRemix.Human()
    rand = playerRemix.Random()
    monte = playerRemix.MonteCarlo()
    monte2 = playerRemix.MonteCarlo()

    vtable = None
    vlearn = playerRemix.Qlearning(PlayPos.FRONTPLAYER, vtable)

    env = DobutuEnv(vlearn, rand)
    env.progress()
