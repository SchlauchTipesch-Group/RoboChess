import chess
import chess.engine

class MoveMaker:
    """
    This class is responsible for managing the chess game, including making moves for both the player
    and the bot (powered by the Stockfish chess engine), and checking the game status.
    """

    def __init__(self, difficulty):
        """
        Initializes the MoveMaker object.

        Args:
            difficulty (int): The difficulty level for the Stockfish engine, which determines
                              the depth of analysis for the bot's moves.
        """
        # Start the Stockfish engine
        self._stockfish = chess.engine.SimpleEngine.popen_uci("stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe")

        # Initialize a new chess board
        self._board = chess.Board()

        # Set the initial status to 0
        self._status = 0

        # Specify the depth level for Stockfish's analysis
        self._stockfishDepth = difficulty

    def get_status(self):
        """
        Returns the current status of the game.

        Returns:
            int: The status of the game (0: ongoing, -1: illegal move, 1: legal move).
        """
        return self._status

    def isOver(self):
        """
        Checks if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self._board.is_game_over()

    def makePlayerMove(self, move_uci):
        """
        Makes a move for the player.

        Args:
            move_uci (str): The move in UCI notation (e.g., "e2e4").

        Updates the game status based on the legality of the move:
            - If the move is illegal, the status is set to -1.
            - If the move is legal, the status is set to 1, and the move is made on the board.
        """
        move = chess.Move.from_uci(move_uci)
        if move not in self._board.legal_moves:
            self._status = -1
        else:
            self._status = 1
            self._board.push(move)

    def makeBotMove(self):
        """
        Makes a move for the bot using the Stockfish engine.

        The bot's move is determined by the Stockfish engine, considering the current board
        position and the specified depth of analysis.
        """
        result = self._stockfish.play(self._board, chess.engine.Limit(depth=self._stockfishDepth))
        stockfish_move = result.move
        self._board.push(stockfish_move)

    def endGame(self):
        """
        Ends the game and quits the Stockfish engine.
        """
        self._stockfish.quit()