## Chessboard Detector

The Chessboard Detector is a Python class designed to detect chessboard patterns and identify pieces on a chessboard image. It provides functionalities to preprocess the image, detect lines using Hough Line Transform, extract contours, crop sections of the chessboard, determine colors representing black and white squares, and identify pieces based on intensity thresholds.

## Installation

Ensure you have the required dependencies installed. You can install them using pip:

```bash
pip install opencv-python numpy
```

## Usage

1. Import the `ChessboardDetector` class:

```python
from ChessboardDetector import ChessboardDetector
```

2. Create an instance of the `ChessboardDetector` class, providing the path to the input chessboard image:

```python
detector = ChessboardDetector('chessboard.jpg')
```

3. Run the pipeline:

```python
detector.run()
```

4. View the processed images (cleaned mask, marked image, contour canvas):

```python
detector.display_images()
```

## Parameters

- `image_path` (str): Path to the input chessboard image.
- `square_size` (int, optional): Size of the chessboard squares. Defaults to 8.

## Attributes

- `image` (numpy.ndarray): The input chessboard image.
- `square_size` (int): Size of the chessboard squares.
- `BLACK_S_WHITE_P` (int): Threshold value for black square with white piece.
- `WHITE_S_WHITE_P` (int): Threshold value for white square with white piece.
- `BLACK_S_BLACK_P` (int): Threshold value for black square with black piece.
- `WHITE_S_BLACK_P` (int): Threshold value for white square with black piece.
- `cleaned_mask` (numpy.ndarray): Preprocessed image mask after cleaning.
- `marked_image` (numpy.ndarray): Image with detected lines marked in green.
- `contour_canvas` (numpy.ndarray): Image with contours drawn on a blank canvas.
- `status` (int): Unique ID for the current state of available data.

## Methods

- `preprocess_image()`: Preprocesses the input image.
- `detect_lines()`: Detects lines in the preprocessed image.
- `extract_contours()`: Extracts contours from the marked image.
- `crop_sections(contours)`: Crops the sections of the chessboard based on the detected contours.
- `determine_colors(cropped_sections)`: Determines the colors representing black and white squares.
- `identify_pieces(cropped_sections, black, white)`: Identifies the pieces on the chessboard.
- `display_images()`: Displays the processed images.

## Example

```python
detector = ChessboardDetector('chessboard.jpg')
detector.run()
detector.display_images()
```

# Chess MoveFinder

Chess MoveFinder is a Python class responsible for finding the move made on a chessboard based on the difference between the current and next board states.

## Usage

To use the MoveFinder class, follow these steps:

1. Import the class into your Python script:

```from move_finder import MoveFinder```

2. Create an instance of the MoveFinder class, passing the current state of the chessboard:

```current_board = chess.Board()
move_finder = MoveFinder(current_board)```

3. Find the move made on the chessboard based on the difference between the current and next board states:

# Assuming next_board is the next state of the chessboard
```next_board = ...  # numpy.ndarray representing the next state of the chessboard
move = move_finder.find_move(next_board)
print("Move made:", move)```

4. Update the current chessboard with the new state:

# Assuming new_board is the new state of the chessboard
```new_board = ...  # chess.Board representing the new state of the chessboard
move_finder.push_board(new_board)```

## Methods

- __init__(self, board): Initializes the MoveFinder object with the given chessboard.
- set_status(self, new_status): Sets the status of the class.
- find_move(self, next_board): Finds the move made on the chessboard based on the difference between the current and next board states.
- push_board(self, board): Updates the current chessboard with the given board.

## Example

Here's an example of how to use the MoveFinder class:
```
from move_finder import MoveFinder

# Create an instance of the MoveFinder class
current_board = chess.Board()
move_finder = MoveFinder(current_board)

# Assuming next_board is the next state of the chessboard
next_board = ...  # numpy.ndarray representing the next state of the chessboard
move = move_finder.find_move(next_board)
print("Move made:", move)

# Assuming new_board is the new state of the chessboard
new_board = ...  # chess.Board representing the new state of the chessboard
move_finder.push_board(new_board)
```

## Notes

- The find_move method returns a list containing the UCI notation of the move made if it can be determined. Otherwise, it returns the string 'p1z1'.
- The class utilizes the chess library for handling chess-related operations.

## License

Chess MoveFinder is licensed under the MIT License. See the LICENSE file for more information.
