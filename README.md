# Automated Chess Game Orchestrator

This Python script orchestrates an automated chess game detection, move making, and communication system. It integrates various components such as image capturing, chessboard detection, move analysis, and communication via UDP socket.

## Requirements
```bash
pip install numpy opencv-python python-chess python-chess-engine pyzmq
```

## Installation
```bash
pip install git+https://github.com/SchlauchTipesch-Group/RoboChess.git
```

## Usage
   
1. Import the required classes and functions into your Python script:

from Utilities.UDP_Socket import udpSocket
from Utilities.log import Log
from Utilities.Take_Picture import pictureTaker
from ChessDetector.ChessboardDetector import ChessboardDetector
from ChessDetector.MoveFinder import MoveFinder
from MoveMaker.MoveMaker import MoveMaker

2. Define the getStatus function to check the game status and determine the winner based on the outcome:

def getStatus(game):
    # Your implementation here

3. Define the main function to orchestrate the chess game detection, move making, and communication:

def main():
    # Your implementation here

4. Run the main function:

if __name__ == "__main__":
   main()

## Components

- UDP Socket: Handles communication between components using UDP protocol.
- Log: Logs status updates and game events.
- Take Picture: Captures images of the chessboard.
- Chessboard Detector: Analyzes the chessboard state using computer vision techniques.
- MoveFinder: Finds the move made on the chessboard based on the difference between the current and next board states.
- MoveMaker: Manages the chess game, including making moves for both players and checking the game status.

## Workflow

1. Initialize all required components such as UDP socket, image capturer, chessboard detector, and move maker.
2. Continuously capture images of the chessboard, analyze the state, and make moves accordingly.
3. Update the game status and log events via the UDP socket.
4. Check for the game's end condition and display the winner when the game is over.

## License

This automated chess game orchestrator is provided under the MIT License. See the LICENSE file for more information.
