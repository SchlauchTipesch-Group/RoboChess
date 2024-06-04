from Utilities.UDP_Socket import udpSocket
from Utilities.log import Log
from Utilities.Take_Picture import pictureTaker
from ChessDetector.ChessboardDetector import ChessboardDetector
from ChessDetector.MoveFinder import MoveFinder
from MoveMaker.MoveMaker import MoveMaker

def getStatus(game):
    """
    Check the game status and determine the winner based on the outcome.

    Args:
        game (MoveMaker): The chess game object.

    Returns:
        int: 2 if white wins, 1 if black wins, 0 for a draw, -1 if the game is ongoing.
    """
    # Check if the game is over
    outcome = game.getOutcome()

    # Determine the winner based on the outcome
    if outcome is not None:
        if outcome.winner == chess.WHITE:
            udp.update_status(getLogComment(2, 'endgameStatus'))
            return 2
        elif outcome.winner == chess.BLACK:
            udp.update_status(getLogComment(1, 'endgameStatus'))
            return 1
        else:
            udp.update_status(getLogComment(0, 'endgameStatus'))
            return 0
    else:
        return -1

def main():
    """
    The main function that orchestrates the chess game detection, move making, and communication.

    This function initializes various components, such as the UDP socket for communication, the picture taker
    for capturing images of the chessboard, the chessboard detector for analyzing the chessboard state, and
    the move maker for handling the game moves.

    It then enters a loop where it continuously captures images of the chessboard, analyzes the chessboard state,
    updates the status via the UDP socket, makes moves based on the detected changes, and checks for the game's
    end condition.

    The loop continues until the game is over, after which it displays the winner.
    """

    # Initialize the UDP socket for communication
    logObject = Log("127.0.0.1", 10369)

    # Initialize the picture taker for capturing images of the chessboard
    picTaker = pictureTaker(1, "chessboard")

    # Initialize the chessboard detector for analyzing the chessboard state
    detector = ChessboardDetector()

    # Initialize the move maker for handling the game moves
    game = MoveMaker(6)

    move_finder = MoveFinder(game.get_board())

    logObject.log([0, 'bootStatus'])

    while True:
        # Take a picture of the chessboard
        picTaker.Take_Picture()

        detector.push_image(picTaker._saveFile_name)

        # Analyze the chessboard state
        detector_status = detector.run_pipeline()

        # Update the status via the UDP socket
        logObject.log([detector_status, 'detectorStatus'])

        # Get the delta of the board (the move made)
        move_ucis = move_finder.find_move(detector._detected)

        for move_uci in move_ucis:
            # Make the player's move
            move_status = game.makePlayerMove(move_uci)
            # Update the status via the UDP socket
            logObject.log([[move_status, move_uci], 'playerMoveStatus'])

        if getStatus(game) > -1:
            game.endGame()
            return 0

        # Make the bot's move
        botMove = game.makeBotMove()

        logObject.log([botMove, 'botMoveStatus'])

        if getStatus(game) > -1:
            game.endGame()
            return 0

        move_finder.push_board(game.get_board())

if __name__ == "__main__":
   main()