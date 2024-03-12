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
