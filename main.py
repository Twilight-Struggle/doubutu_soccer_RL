#!/usr/bin/env python
# coding: UTF-8

from refact_doso import DobutuEnv
import playerRemix

if __name__ == "__main__":
    human = playerRemix.Human()
    rand = playerRemix.Random()
    monte = playerRemix.MonteCarlo()
    monte2 = playerRemix.MonteCarlo()
    env = DobutuEnv(human, rand)
    env.progress()
