# Chess MoveMaker

Chess MoveMaker is a Python class responsible for managing a chess game, including making moves for both the player and the bot (powered by the Stockfish chess engine), and checking the game status.

## Installation

Before using the MoveMaker class, you need to install the Stockfish chess engine. You can download Stockfish from the official website: https://stockfishchess.org/download/. After downloading, make sure to replace the path to the Stockfish executable in the code with the correct path on your system.

## Usage

To use the MoveMaker class, follow these steps:

1. Import the class into your Python script:

from move_maker import MoveMaker

2. Create an instance of the MoveMaker class, specifying the difficulty level:

move_maker = MoveMaker(difficulty=10)  # Adjust the difficulty level as needed

3. Make moves for the player and the bot:

# Make a move for the player
player_move_status = move_maker.makePlayerMove("e2e4")

# Make a move for the bot
bot_move = move_maker.makeBotMove()

4. Check the game outcome:

outcome = move_maker.getOutcome()

5. End the game:

move_maker.endGame()

## Methods

- __init__(self, difficulty): Initializes the MoveMaker object with the specified difficulty level.
- get_board(self): Returns the current state of the chess board.
- getOutcome(self): Returns the outcome of the game (None if ongoing).
- makePlayerMove(self, move_uci): Makes a move for the player on the chess board.
- makeBotMove(self): Makes a move for the bot using the Stockfish engine.
- endGame(self): Ends the game and quits the Stockfish engine.

## Example

Here's an example of how to use the MoveMaker class:

from move_maker import MoveMaker

# Create an instance of the MoveMaker class
move_maker = MoveMaker(difficulty=10)

# Make a move for the player
player_move_status = move_maker.makePlayerMove("e2e4")

# Make a move for the bot
bot_move = move_maker.makeBotMove()

# Check the game outcome
outcome = move_maker.getOutcome()
if outcome:
    print("Game over. Result:", outcome)

# End the game
move_maker.endGame()

## Credits

This project utilizes the Stockfish chess engine for bot moves. Stockfish is an open-source chess engine developed by the Stockfish community and is licensed under the GNU General Public License v3.0.

## License

Chess MoveMaker is licensed under the MIT License. See the LICENSE file for more information.
