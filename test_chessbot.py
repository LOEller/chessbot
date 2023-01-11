from chessbot import ChessBot
import pytest


@pytest.mark.parametrize("depth", [1,2,3])
def test_scholars_mate(depth):
    bot = ChessBot(depth)

    bot.make_move_from_san("e4")
    bot.make_move_from_san("e5")
    bot.make_move_from_san("Qh5")
    bot.make_move_from_san("Nc6")
    bot.make_move_from_san("Bc4")
    bot.make_move_from_san("Nf6")

    assert bot.compute_next_move() == "Qxf7#"

@pytest.mark.parametrize("depth", [3,4])
def test_fork_puzzle(depth):
    # https://www.chess.com/analysis/game/pgn/2tG7kYxdre
    bot = ChessBot(depth)

    # black is leading with 5 points of material
    fen_string = "2q3k1/8/8/5N2/6P1/7K/8/8 w - - 0 1"
    bot.load_position(fen_string, -5)
    
    # move Knight to e7 to fork queen and king
    # not sure how it's possible that this is finding the
    # move when the depth is 2?
    assert bot.compute_next_move() == "Ne7+"

def test_mate_in_two(depth=3):
    # https://www.chess.com/analysis/game/pgn/12MxwqUadt
    bot = ChessBot(depth)

    # white is leading with 6 points of material
    fen_string = "8/2K5/8/2k5/2b5/2B5/2Q2n2/8 w - - 0 1"
    bot.load_position(fen_string, 6)

    # tricky, Qa4 leads to mate in 2 or Qxf2+ leads to mate in 3
    assert bot.compute_next_move() == "Qa4"


def test_mate_in_three(depth=5):
    # https://www.chess.com/analysis/game/pgn/31nWW4QQSi
    bot = ChessBot(depth)

    fen_string = "3r4/pR2N3/2pkb3/5p2/8/2B5/qP3PPP/4R1K1 w - - 1 1"
    bot.load_position(fen_string, 0)

    assert bot.compute_next_move() == "Be5+"


def test_discovered_attack(depth=5):
    # https://www.chess.com/analysis/game/pgn/3v5hoETbi6
    # not actually the best test of complex tactics since the
    # answer can be found in 1 move...

    bot = ChessBot(depth)
    fen_string = "r1b2rk1/1pq1bppp/p2p1n2/2nNp3/4P2N/1B6/PPP2PPP/R1BQR1K1 b - - 0 1"
    
    bot.load_position(fen_string, 0)

    assert bot.compute_next_move() == "Nxd5"


def test_intermezzo(depth=5):
    # https://www.chess.com/analysis/game/pgn/4vXQiwi4va
    bot = ChessBot(depth)
    fen_string = "6k1/pp6/1r1Rp1p1/4r3/7P/2P5/PP2R3/K7 w - - 0 1"
    
    bot.load_position(fen_string, 0)

    assert bot.compute_next_move() == "Rd8+"


