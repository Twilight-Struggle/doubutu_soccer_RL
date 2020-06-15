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

    qtable = None
    qlearn = playerRemix.Qlearning(PlayPos.FRONTPLAYER, qtable)

    env = DobutuEnv(qlearn, rand)
    env.progress()
