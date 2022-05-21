"""Example: create a game and let computer play each player at a time."""
import fire

from chess.game import Game


def run_game(max_moves: int = 10, verbose: bool = True, show: bool = True):
    """Run game.

    Parameters
    -----------
    max_moves : int
        Maximum number of moves.
    verbose : bool
        Verbosity level.
    show : bool
        If True, show board at each move.

    """
    # init game
    game = Game.create()

    # show board in init state
    if show:
        game.show_board()

    # run moves and show board at each move
    for i in range(max_moves):
        if game.is_finished:
            break
        game.next_move(verbose=verbose)
        if show:
            game.show_board()

    # show game history
    if verbose:
        print("History:")
        game.show_history()


if __name__ == "__main__":
    fire.Fire(run_game)
