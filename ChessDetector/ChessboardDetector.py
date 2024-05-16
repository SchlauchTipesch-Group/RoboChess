import cv2
import numpy as np

class ChessboardDetector:
    def __init__(self, squares_per_row=8):
        """
        Constructor for the ChessboardDetector class.

        Args:
            squares_per_row (int, optional): Number of squares per row on the chessboard. Defaults to 8.

        Attributes:
            _image (numpy.ndarray): The input chessboard image.
            _squares_per_row (int): Number of squares per row on the chessboard.
            BLACK_S_WHITE_P (int): Threshold value for black square with white piece.
            WHITE_S_WHITE_P (int): Threshold value for white square with white piece.
            BLACK_S_BLACK_P (int): Threshold value for black square with black piece.
            WHITE_S_BLACK_P (int): Threshold value for white square with black piece.
            _cleaned_mask (numpy.ndarray): Preprocessed image mask after cleaning.
            _marked_image (numpy.ndarray): Image with detected lines marked in green.
            _contour_canvas (numpy.ndarray): Image with contours drawn on a blank canvas.
            _detected (numpy.ndarray): 2D array representing the detected chessboard state.
            _status (int): Unique ID for the current state of available data.
        """
        self._image = None
        self._squares_per_row = squares_per_row
        self.BLACK_S_WHITE_P = 35
        self.WHITE_S_WHITE_P = 18
        self.BLACK_S_BLACK_P = 18
        self.WHITE_S_BLACK_P = 100
        self._cleaned_mask = None
        self._marked_image = None
        self._contour_canvas = None
        self._detected = None
        self._status = 0

    def read_image(self, image_path):
        """
        Reads an image from the specified path.

        Args:
            image_path (str): Path to the input image.

        Returns:
            tuple: A tuple containing the loaded image and a status code.
                   The status code is -1 if the image could not be loaded, and 0 otherwise.
        """
        image = cv2.imread(image_path)  # Read the input image
        if image is None:
            status = -1  # Set status to -1 if image could not be loaded
        else:
            status = 0  # Set status to 0 if image is loaded successfully

        return image, status

    def push_image(self, image_path):
        """
        Pushes a new image to the detector for processing.

        Args:
            image_path (str): Path to the input image.
        """
        self._cleaned_mask = None
        self._marked_image = None
        self._contour_canvas = None
        self._detected = None

        self._image, self._status = self.read_image(image_path)

    def preprocess_image(self):
        """
        Preprocesses the input image by converting to grayscale, applying adaptive thresholding,
        and performing erosion and dilation to clean up the mask.
        """
        if self._status == -1:
            return
        image_gray = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        # Apply adaptive thresholding
        thresholded = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        kernel = np.ones((3, 3), np.uint8)  # Create a 3x3 kernel
        self._cleaned_mask = cv2.erode(thresholded, kernel, iterations=1)  # Perform erosion
        self._cleaned_mask = cv2.dilate(self._cleaned_mask, kernel, iterations=1)  # Perform dilation
        self._status = 1  # Update status to 1

    def detect_lines(self):
        """
        Detects lines in the preprocessed image using the Hough Line Transform and draws
        the detected lines on a copy of the original image in green color.
        """
        if self._status > 0:
            self._marked_image = self._image.copy()  # Create a copy of the original image
            lines = cv2.HoughLines(self._cleaned_mask, 1, np.pi / 180, threshold=600)  # Detect lines using Hough Line Transform
            if lines is not None:
                for rho, theta in lines[:, 0]:  # Loop through detected lines
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 2000 * (-b))
                    y1 = int(y0 + 2000 * (a))
                    x2 = int(x0 - 2000 * (-b))
                    y2 = int(y0 - 2000 * (a))
                    cv2.line(self._marked_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw line on the marked image
                self._status = 2  # Update status to 2 if marked image is available
            else:
                self._marked_image = None
                self._status = -2

    def extract_contours(self):
        """
        Extracts contours from the marked image containing the detected lines.

        Returns:
            list: A list of contours detected in the image.
        """
        if self._status > 1 and self._marked_image is not None:
            thresh = cv2.inRange(self._marked_image, np.array([0, 254, 0]), np.array([0, 255, 0]))  # Threshold for green lines
            kernel = np.ones((3, 3), np.uint8)
            cleaned_lines_mask = cv2.erode(thresh, kernel, iterations=5)  # Erode the mask
            cleaned_lines_mask = cv2.dilate(thresh, kernel, iterations=5)  # Dilate the mask
            edges = cv2.Canny(cleaned_lines_mask, 50, 150)  # Apply Canny edge detection
            dilated_edges = cv2.dilate(edges, kernel, iterations=1)  # Dilate the edges
            contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
            self._contour_canvas = np.zeros_like(self._marked_image)  # Create a blank canvas
            cv2.drawContours(self._contour_canvas, contours, -1, (0, 255, 0), 2)  # Draw contours on the canvas

            return contours
        else:
            return []

    def crop_sections(self, contours):
        """
        Crops the sections of the chessboard based on the detected contours.

        Args:
            contours (list): A list of contours detected in the image.

        Returns:
            list: A list of cropped sections from the chessboard.
        """
        if self._status > 1 and contours:
            cropped_sections = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)  # Get the bounding rectangle for each contour
                section = self._marked_image[y:y+h, x:x+w].copy()  # Crop the section from the marked image
                cropped_sections.append(section)

            average_section_size = sum(section.shape[0] * section.shape[1] for section in cropped_sections) / len(cropped_sections)  # Calculate the average section size
            cropped_sections = [section for section in cropped_sections if (section.shape[0] * section.shape[1]) >= (0.7 * average_section_size)]  # Filter out small sections
            cropped_sections.reverse()  # Reverse the order of the cropped sections
            self._status = 3
            return cropped_sections
        else:
            return []

    def determine_colors(self, cropped_sections):
        """
        Determines the colors representing black and white squares based on the cropped sections.

        Args:
            cropped_sections (list): A list of cropped sections from the chessboard.

        Returns:
            tuple: A tuple containing the values representing black and white colors.
        """
        if cropped_sections:
            color1 = np.mean(cv2.cvtColor(cropped_sections[0], cv2.COLOR_BGR2GRAY))  # Calculate the average intensity of the first section
            color2 = np.mean(cv2.cvtColor(cropped_sections[1], cv2.COLOR_BGR2GRAY))  # Calculate the average intensity of the second section
            black = max(color1, color2)  # Assign the higher intensity to black
            white = min(color1, color2)  # Assign the lower intensity to white
            return black, white

    def identify_pieces(self, cropped_sections, black, white):
        """
        Identifies the pieces on the chessboard and draws them on a canvas.

        Args:
            cropped_sections (list): A list of cropped sections from the chessboard.
            black (int): Value representing the black color.
            white (int): Value representing the white color.

        Returns:
            numpy.ndarray: The canvas with the chessboard and pieces drawn on it.
        """

        board = np.zeros((self._squares_per_row, self._squares_per_row), dtype=int)

        if cropped_sections and black is not None and white is not None:

            for i, section in enumerate(cropped_sections):
                gray = cv2.cvtColor(section, cv2.COLOR_BGR2GRAY)  # Convert the section to grayscale
                avg_intensity = np.mean(gray)  # Calculate the average intensity of the section
                square_type = "Black Square" if abs(avg_intensity - black) > abs(avg_intensity - white) else "White Square"  # Determine the square type

                crop_width = 100
                crop_height = 100
                mask_height, mask_width = gray.shape
                start_x = (mask_width - crop_width) // 2  # Calculate the start x-coordinate for cropping
                end_x = start_x + crop_width  # Calculate the end x-coordinate for cropping
                start_y = (mask_height - crop_height) // 2  # Calculate the start y-coordinate for cropping
                end_y = start_y + crop_height  # Calculate the end y-coordinate for cropping
                cropped_mask = gray[start_y:end_y, start_x:end_x]  # Crop the section

                cropped_mask = cv2.GaussianBlur(cropped_mask, (31, 31), 0)  # Apply Gaussian blur

                threshold_value = np.min(cropped_mask)  # Find the minimum intensity value

                vicinity_range = 10
                binary_mask = np.abs(cropped_mask - threshold_value) <= vicinity_range  # Create a binary mask
                binary_mask = binary_mask.astype(np.uint8) * 255

                binary_mask = cv2.bitwise_not(binary_mask)  # Invert the binary mask

                piece_color = 0

                if (square_type == "Black Square" and abs(threshold_value - avg_intensity) > self.BLACK_S_WHITE_P) or (
                        square_type == "White Square" and abs(threshold_value - avg_intensity) > self.WHITE_S_WHITE_P and abs(
                        threshold_value - avg_intensity) < self.WHITE_S_BLACK_P):

                    piece_color = 2  # Identify the piece as white

                elif (square_type == "Black Square" and abs(threshold_value - avg_intensity) > self.BLACK_S_BLACK_P) > (
                        square_type == "White Square" and abs(threshold_value - avg_intensity) > self.WHITE_S_BLACK_P):

                    piece_color = 1  # Identify the piece as black

                else:
                    pass  # No piece detected

                board[(i % self._squares_per_row), int(i / self._squares_per_row)] = piece_color

            self._detected = board
            self._status = 4

    def display_images(self):
        """
        Displays the cleaned mask, marked image, and contour canvas in separate windows.
        """
        if self._status >= 2:
            cv2.imshow("Cleaned Mask", self._cleaned_mask)  # Display the cleaned mask
            cv2.imshow("Marked Image", self._marked_image)  # Display the marked image
            cv2.imshow("Contour Canvas", self._contour_canvas)  # Display the contour canvas
            cv2.waitKey(0)  # Wait for a key press
            cv2.destroyAllWindows()  # Close all windows

    def run_pipeline(self):
        """
        Runs the entire pipeline for chessboard detection and piece identification.

        Returns:
            int: The final status code after running the pipeline.
        """

        if self._status == 0:
            self.preprocess_image()  # Preprocess the image
        if self._status == 1:
            self.detect_lines()  # Detect lines
        if self._status == 2:
            contours = self.extract_contours()  # Extract contours
            cropped_sections = self.crop_sections(contours)  # Crop sections
        if self._status == 3:
            black, white = self.determine_colors(cropped_sections)  # Determine colors
            self.identify_pieces(cropped_sections, black, white)  # Identify pieces colors
        return self._status