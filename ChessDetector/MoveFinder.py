import chess

class MoveFinder:
    """
    This class is responsible for finding the move made on a chessboard based on the difference between the current and next board states.

    Attributes:
        _board (chess.Board): The current state of the chessboard.
        _status (int): A status code indicating the current state of the class.

    Methods:
        __init__(self, board): Initializes the MoveFinder object with the given chessboard.
        set_status(self, new_status): Sets the status of the class.
        find_move(self, next_board): Finds the move made on the chessboard based on the difference between the current and next board states.
        push_board(self, board): Updates the current chessboard with the given board.
    """

    def __init__(self, board):
        """
        Initializes the MoveFinder object with the given chessboard.

        Args:
            board (chess.Board): The initial state of the chessboard.
        """
        self._board = board
        self._status = 0

    def set_status(self, new_status):
        """
        Sets the status of the class.

        Args:
            new_status (int): The new status code.
        """
        self._status = new_status

    def find_move(self, next_board):
        """
        Finds the move made on the chessboard based on the difference between the current and next board states.

        Args:
            next_board (numpy.ndarray): The next state of the chessboard.

        Returns:
            list or str: A list containing the UCI notation of the move made, or a string 'p1z1' if the move cannot be determined.
        """
        emptied = set()
        filled = set()

        length, height = next_board.shape

        for i in range(length):
            for j in range(height):
                square_name = chess.square_name(8 * j + i)
                piece = self._board.piece_at(chess.square(i, j))

                if piece is not None:
                    if piece.color == chess.WHITE:
                        color_id = 2
                    else:
                        color_id = 1

                    if next_board[i, j] == 0:
                        emptied.add(square_name)
                    elif color_id != next_board[i, j]:
                        filled.add(square_name)
                    else:
                        pass
                else:
                    if next_board[i, j] != 0:
                        filled.add(square_name)

        if len(filled) == 1 and len(emptied) == 1:
            code = f"{list(emptied)[0]}{list(filled)[0]}"
            return [code]

        elif len(filled) == 2 and len(emptied) == 2:
            if chess.square_name(0) in emptied and chess.square_name(4) in emptied:
                code = ["e1c1", "a1d1"]
            elif chess.square_name(7) in emptied and chess.square_name(4) in emptied:
                code = ["e1g1", "h1f1"]
            else:
                code = "p1z1"
            return code
        else:
            return "p1z1"

    def push_board(self, board):
        """
        Updates the current chessboard with the given board.

        Args:
            board (chess.Board): The new state of the chessboard.
        """
        if type(board) == type(chess.Board()):
            self._board = board
        else:
            self.set_status(-1)