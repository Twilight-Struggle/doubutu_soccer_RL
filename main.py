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

    if os.path.exists("./Qlearning.pickle"):
        with open("Qlearning.pickle", "rb") as fq:
            qtable = pickle.load(fq)
    else:
        qtable = None
    qlearn = playerRemix.Qlearning(PlayPos.FRONTPLAYER, qtable)

    winrate = []
    env = DobutuEnv(qlearn, rand)
    for i in range(1000):
        count = 0
        for j in range(100):
            winner = env.progress()
            if winner == PlayPos.FRONTPLAYER:
                count += 1
            env.reset()
        won = count
        winrate.append(won)
        print(i)
    # print(qlearn.Qtable)
    with open("Qlearning.pickle", "wb") as fq:
        pickle.dump(qlearn.Qtable, fq)
    for i in winrate:
        print(i)
    print("{} {}".format(includes.fuckinglobal, includes.fuckinglobal2))