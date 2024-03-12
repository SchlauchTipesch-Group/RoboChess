from Utilities.UDP_Socket import udpSocket
from Utilities.Take_Picture import pictureTaker
from ChessDetector.ChessboardDetector import ChessboardDetector
from MoveMaker.MoveMaker import MoveMaker

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
    udp = udpSocket("127.0.0.1", 10369)

    # Initialize the picture taker for capturing images of the chessboard
    picTaker = pictureTaker(1, "chessboard")

    # Initialize the chessboard detector for analyzing the chessboard state
    detector = ChessboardDetector(picTaker._saveFile_name)

    # Initialize the move maker for handling the game moves
    game = MoveMaker(6)

    while True:
        # Take a picture of the chessboard
        picTaker.Take_Picture()

        # Analyze the chessboard state
        detector.run()

        # Update the status via the UDP socket
        udp.update_status(detector.get_status)

        # Get the delta of the board (the move made)
        move_uci = 'a1h1'

        # Make the player's move
        game.makePlayerMove(move_uci)

        # Update the status via the UDP socket
        udp.update_status(game.get_status())

        # Check if the game is over
        if game.isOver() == True:
            print("Win")
            # Display the game winner

            break

        # Make the bot's move
        game.makeBotMove()

        # Check if the game is over
        if game.isOver() == True:
            print("Win")
            # Display the game winner
            
            break

if __name__ == "__main__":
    main()