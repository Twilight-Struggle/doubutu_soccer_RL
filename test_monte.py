#!/usr/bin/env python
# coding: UTF-8

import pytest
import copy
import playerRemix
from includes import Act
import refact_doso

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
cells[1][0] = S_usa_f
cells[0][2] = S_risu_f
cells[2][2] = S_ball
cells[2][1] = S_saru_s
cells[3][1] = S_risu_s
cells[4][2] = S_usa_s

dummyboard = refact_doso.Board(refact_doso.PlayPos.FRONTPLAYER, cells)
monte = playerRemix.MonteCarlo()

acts = dummyboard.legal_moves()
#acts.append(Act([2, 2, "さ"], [[4, 0]]))


@pytest.mark.parametrize('Board, act', [
    (dummyboard, acts[0]),
    (dummyboard, acts[1]),
    (dummyboard, acts[2]),
    (dummyboard, acts[3]),
    (dummyboard, acts[4]),
    (dummyboard, acts[5]),
    (dummyboard, acts[6]),
    (dummyboard, acts[7]),
    (dummyboard, acts[8]),
    (dummyboard, acts[9]),
    (dummyboard, acts[10]),
    (dummyboard, acts[11]),
    (dummyboard, acts[12]),
    (dummyboard, acts[13]),
    (dummyboard, acts[14]),
])
def test_trial(Board, act):
    for i in range(1000):
        monte.trial(Board, act)


if __name__ == '__main__':
    print(len(dummyboard.legal_moves()))
    pytest.main(['-v', __file__])
