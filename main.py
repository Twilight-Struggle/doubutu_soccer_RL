#!/usr/bin/env python
# coding: UTF-8

from refact_doso import DobutuEnv
from includes import PlayPos
import includes
import playerRemix
import pickle
import os

if __name__ == "__main__":
    # human = playerRemix.Human()
    rand = playerRemix.Random()
    # monte = playerRemix.MonteCarlo()
    # monte2 = playerRemix.MonteCarlo()

    if os.path.exists("./Vlearning.pickle"):
        with open("Vlearning.pickle", "rb") as fq:
            vtable = pickle.load(fq)
    else:
        vtable = None
    vlearn = playerRemix.Vlearning(PlayPos.FRONTPLAYER, vtable)

    print("init done", flush=True)
    loop_num = 0
    env = DobutuEnv(vlearn, rand)
    while True:
        count = 0
        loop_num += 1
        for j in range(100):
            winner = env.progress()
            if winner == PlayPos.FRONTPLAYER:
                count += 1
            env.reset()
        won = count
        print("winrate:{}".format(won), flush=True)
        if won > 80:
            with open("Vlearning.pickle", "wb") as fq:
                pickle.dump(vlearn.Vtable, fq)
            break
        if loop_num > 1000:
            loop_num = 0
            with open("Vlearning.pickle", "wb") as fq:
                pickle.dump(vlearn.Vtable, fq)
