#!/usr/bin/env python
# coding: UTF-8

from refact_doso import DobutuEnv
from includes import PlayPos
import includes
import playerRemix
import pickle
import os

if __name__ == "__main__":
    human = playerRemix.Human()
    rand = playerRemix.Random()
    monte = playerRemix.MonteCarlo()
    monte2 = playerRemix.MonteCarlo()

    winrate = []
    env = DobutuEnv(monte, rand)
    winner = env.progress()
    if winner == PlayPos.FRONTPLAYER:
        print("Winner is monte!")
    else:
        print("Winner is rand!")