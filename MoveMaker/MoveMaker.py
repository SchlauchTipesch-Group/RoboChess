import chess
import chess.engine

class MoveMaker:
    """
    This class is responsible for managing the chess game, including making moves for both the player
    and the bot (powered by the Stockfish chess engine), and checking the game status.

    Attributes:
        _stockfish (chess.engine.SimpleEngine): An instance of the Stockfish chess engine.
        _board (chess.Board): A chess board object representing the current game state.
        _stockfishDepth (int): The depth level for the Stockfish engine's analysis.

    Methods:
        __init__(self, difficulty): Initializes the MoveMaker object with the specified difficulty level.
        get_board(self): Returns the current state of the chess board.
        getOutcome(self): Return the outcome of the game None if ongoing.
        makePlayerMove(self, move_uci): Makes a move for the player on the chess board.
        makeBotMove(self): Makes a move for the bot using the Stockfish engine.
        endGame(self): Ends the game and quits the Stockfish engine.
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

        # Specify the depth level for Stockfish's analysis
        self._stockfishDepth = difficulty

    def get_board(self):
        """
        Returns the current state of the chess board.

        Returns:
            chess.Board: The board.
        """
        return self._board

    def getOutcome(self):
        """
        Checks if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self._board.outcome()

    def makePlayerMove(self, move_uci):
        """
        Makes a move for the player.

        Args:
            move_uci (str): The move in UCI notation (e.g., "e2e4").

        Returns:
            int: A status code indicating the legality of the move:
                 - -1 if the move is illegal
                 - 1 if the move is legal

        If the move is legal, the move is made on the board.
        """
        move = chess.Move.from_uci(move_uci)
        if move not in self._board.legal_moves:
            status = -1
        else:
            status = 1
            self._board.push(move)

        return status

    def makeBotMove(self):
        """
        Makes a move for the bot using the Stockfish engine.

        The bot's move is determined by the Stockfish engine, considering the current board
        position and the specified depth of analysis.

        Returns:
            chess.Move: The move made by the Stockfish engine.
        """
        result = self._stockfish.play(self._board, chess.engine.Limit(depth=self._stockfishDepth))
        stockfish_move = result.move

        self._board.push(stockfish_move)

        return stockfish_move

    def endGame(self):
        """
        Ends the game and quits the Stockfish engine.
        """
        self._stockfish.quit()