#!/usr/bin/env python
# coding: UTF-8

import pytest

import pieceRemix

BOARD_HEIGHT = 5
BOARD_WIDTH = 3


class Dummyboard:
    def __init__(self):
        self.cells = []
        for i in range(BOARD_HEIGHT):
            self.cells.append([None for i in range(BOARD_WIDTH)])


piecetester = pieceRemix.Piece(1)


@pytest.mark.parametrize('inp', [(4, 2), (2, 1)])
def test_piece_where_me(inp):
    dummy = Dummyboard()
    dummy.cells[inp[0]][inp[1]] = piecetester
    assert piecetester.where_me(dummy) == inp


if __name__ == '__main__':
    pytest.main(['-v', __file__])