#!/usr/bin/env python
# coding: UTF-8

from refact_doso import DobutuEnv
from includes import PlayPos
import playerRemix
import pickle
import os

if __name__ == "__main__":
    human = playerRemix.Human()
    rand = playerRemix.Random()
    monte = playerRemix.MonteCarlo()
    monte2 = playerRemix.MonteCarlo()

    if os.path.exists("./Qlearning.pickle"):
        with open("Qlearning.pickle", "rb") as fq:
            qtable = pickle.load(fq)
    else:
        qtable = None
    qlearn = playerRemix.Qlearning(PlayPos.FRONTPLAYER, qtable)

    env = DobutuEnv(qlearn, rand)
    for i in range(10000):
        env.progress()
        env.reset()
    # print(qlearn.Qtable)
    with open("Qlearning.pickle", "wb") as fq:
        pickle.dump(qlearn.Qtable, fq)
