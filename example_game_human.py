"""Example: create a game and let user play against computer through CLI."""
from random import randint

from chess.coords import coords_to_loc
from chess.game import Game

verbose = True
show = True

n_moves = 200

# init game
game = Game.create()

computer_side = "white" if randint(0, 1) == 1 else "black"
if verbose:
    print(f"Computer plays with the {computer_side}s")


# show board in init state
if show:
    game.show_board()

# run moves and show board at each move
for i in range(n_moves):

    if game.is_finished:
        break

    if verbose:
        print(f"Move #{game.move_number}: {game.turn} to play")

    # computer play
    if game.turn == computer_side:
        game.next_move(verbose=verbose)
        if show:
            game.show_board()
    # user play
    else:
        # select piece
        while True:
            piece_loc = input("Select piece:").lower()
            if piece_loc == "show":
                game.show_board()
            elif game.board.get_piece(piece_loc):
                # get piece
                piece = game.board.get_piece(piece_loc)
                if piece.color != game.turn:
                    print(f"Wrong piece selected")
                    continue
                valid_moves = [
                    coords_to_loc(move.get_new_coords(piece.coords))
                    for move in piece.get_valid_moves(game.board)
                ]
                print(valid_moves)
                if len(valid_moves) == 0:
                    print(f"This piece has no moves")
                    continue
                break
            else:
                print(f"Invalid piece location {piece_loc}")
                continue
        # show moves for selected piece
        game.show_board(loc=piece_loc, show_moves=True)
        # select move
        while True:
            move = input("Select move:").lower()
            if move == "show":
                game.show_board(loc=piece_loc, show_moves=True)
            elif move in valid_moves:
                break
            else:
                print(f'Invalid move "{move}" for piece {piece}')
        move = piece.get_move(move, game.board)
        game.next_move(move=(piece, move))
        game.show_board()

# print game history
game.show_history()

# example game: blacks win after 10 moves against white
# 1. Nh3 e5
# 2. Ng5 Qxg5
# 3. Nc3 d6
# 4. a3 Bg4
# 5. a4 e4
# 6. h4 Qxh4
# 7. e3 Qxh1
# 8. Qf3 e4xf3
# 9. b4 f3xg2
