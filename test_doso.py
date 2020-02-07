#!/usr/bin/env python
# coding: UTF-8

import sys
print(sys.version)
print(sys.path)

import pytest

import refact_doso

BOARD_HEIGHT = 5
BOARD_WIDTH = 3

S_ball = refact_doso.Piece(refact_doso.PieceID.BALL_ID)
S_oyasaru_f = refact_doso.Piece(refact_doso.PieceID.OYASARU_ID,
                                refact_doso.PlayPos.FRONTPLAYER)
S_saru_f = refact_doso.Piece(refact_doso.PieceID.SARU_ID,
                             refact_doso.PlayPos.FRONTPLAYER)
S_risu_f = refact_doso.Piece(refact_doso.PieceID.RISU_ID,
                             refact_doso.PlayPos.FRONTPLAYER)
S_usa_f = refact_doso.Piece(refact_doso.PieceID.USAGI_ID,
                            refact_doso.PlayPos.FRONTPLAYER)
S_oyasaru_s = refact_doso.Piece(refact_doso.PieceID.OYASARU_ID,
                                refact_doso.PlayPos.BACKPLAYER)
S_saru_s = refact_doso.Piece(refact_doso.PieceID.SARU_ID,
                             refact_doso.PlayPos.BACKPLAYER)
S_risu_s = refact_doso.Piece(refact_doso.PieceID.RISU_ID,
                             refact_doso.PlayPos.BACKPLAYER)
S_usa_s = refact_doso.Piece(refact_doso.PieceID.USAGI_ID,
                            refact_doso.PlayPos.BACKPLAYER)

cells = []
for i in range(refact_doso.BOARD_HEIGHT):
    cells.append([None for i in range(refact_doso.BOARD_WIDTH)])

cells[1][1] = S_saru_f
cells[0][0] = S_usa_f
cells[0][2] = S_risu_f
cells[2][1] = S_ball
cells[3][1] = S_saru_s
cells[4][0] = S_risu_s
cells[4][2] = S_usa_s

dummyboard = refact_doso.Board(None, None, refact_doso.PlayPos.FRONTPLAYER,
                               cells)


@pytest.mark.parametrize('inp, out', [(dummyboard.S_ball, (2, 1)),
                                      (dummyboard.S_saru_f, (1, 1))])
def test_piece_where_me(inp, out):
    assert dummyboard.where_you(inp) == out


@pytest.mark.parametrize('inp, out',
                         [(dummyboard.S_usa_s, ([(3, 2), (4, 1)], None)),
                          (dummyboard.S_saru_f, ([(0, 1), (1, 0), (1, 2),
                                                  (2, 0), (2, 2)], (2, 1)))])
def test_piece_where_me(inp, out):
    assert dummyboard.piece_can_move(inp) == out


if __name__ == '__main__':
    pytest.main(['-v', __file__])