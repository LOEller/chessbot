import chess
from chessbot import ChessBot
import argparse


def prompt_move_helper(bot):
    move = input()
    try:
        bot.make_move_from_san(move)
    except chess.IllegalMoveError:
        print("That is not a legal move. Please try again.")
        prompt_move_helper(bot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--depth', required=True, type=int)
    parser.add_argument('-c', '--color', required=True, choices=["black", "white"])
    args = parser.parse_args()

    bot = ChessBot(args.depth)

    player_color = args.color
    computer_color = "black" if args.color == "white" else "white"

    print(f"Welcome to ChessBot. You have chosen to play as {player_color}.")

    if computer_color == "black":
        print("Enter move for white:")
        prompt_move_helper(bot)

    while not bot.board.is_game_over():
        move = bot.compute_next_move()
        print(f"{computer_color} moves {move}")
        bot.make_move_from_san(move)

        if bot.board.is_game_over():
            break
        print(bot.board)

        print(f"Enter move for {player_color}:")
        prompt_move_helper(bot)

    outcome = bot.board.outcome()
    if not outcome:
        print("Game is drawn.")
    else:
        winner = "White" if outcome.winner == chess.WHITE else "Black"
        print(f"{winner} wins")
    exit(0)
