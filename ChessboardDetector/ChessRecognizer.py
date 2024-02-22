import cv2
import numpy as np

class ChessboardDetector:
    def __init__(self, image_path, square_size=8):
        """
        Constructor for the ChessboardDetector class.

        Args:
            image_path (str): Path to the input chessboard image.
            square_size (int, optional): Size of the chessboard squares. Defaults to 8.

        Attributes:
            image (numpy.ndarray): The input chessboard image.
            square_size (int): Size of the chessboard squares.
            BLACK_S_WHITE_P (int): Threshold value for black square with white piece.
            WHITE_S_WHITE_P (int): Threshold value for white square with white piece.
            BLACK_S_BLACK_P (int): Threshold value for black square with black piece.
            WHITE_S_BLACK_P (int): Threshold value for white square with black piece.
            cleaned_mask (numpy.ndarray): Preprocessed image mask after cleaning.
            marked_image (numpy.ndarray): Image with detected lines marked in green.
            contour_canvas (numpy.ndarray): Image with contours drawn on a blank canvas.
            status (int): Unique ID for the current state of available data.
        """
        self.image = cv2.imread(image_path)  # Read the input image
        if self.image is None:
            print("Error: Unable to load the image.")
            self.status = -1  # Set status to -1 if image could not be loaded
        else:
            self.status = 0  # Set status to 0 if image is loaded successfully

        self.square_size = square_size
        self.BLACK_S_WHITE_P = 35
        self.WHITE_S_WHITE_P = 18
        self.BLACK_S_BLACK_P = 18
        self.WHITE_S_BLACK_P = 100
        self.cleaned_mask = None
        self.marked_image = None
        self.contour_canvas = None

    def preprocess_image(self):
        """
        Preprocesses the input image by converting to grayscale, applying adaptive thresholding,
        and performing erosion and dilation to clean up the mask.
        """
        if self.status == -1:
            print("Error: Unable to preprocess the image.")
            return
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        # Apply adaptive thresholding
        thresholded = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        kernel = np.ones((3, 3), np.uint8)  # Create a 3x3 kernel
        self.cleaned_mask = cv2.erode(thresholded, kernel, iterations=1)  # Perform erosion
        self.cleaned_mask = cv2.dilate(self.cleaned_mask, kernel, iterations=1)  # Perform dilation
        self.status = 1  # Update status to 1

    def detect_lines(self):
        """
        Detects lines in the preprocessed image using the Hough Line Transform and draws
        the detected lines on a copy of the original image in green color.
        """
        if self.status > 0:
            self.marked_image = self.image.copy()  # Create a copy of the original image
            lines = cv2.HoughLines(self.cleaned_mask, 1, np.pi / 180, threshold=600)  # Detect lines using Hough Line Transform
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
                    cv2.line(self.marked_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw line on the marked image
                self.status = 2  # Update status to 2 if marked image is available
            else:
                print("Error: No lines detected in the image.")
        else:
            print("Error: Unable to detect lines in the image.")

    def extract_contours(self):
        """
        Extracts contours from the marked image containing the detected lines.

        Returns:
            list: A list of contours detected in the image.
        """
        if self.status > 1 and self.marked_image is not None:
            thresh = cv2.inRange(self.marked_image, np.array([0, 254, 0]), np.array([0, 255, 0]))  # Threshold for green lines
            kernel = np.ones((3, 3), np.uint8)
            cleaned_lines_mask = cv2.erode(thresh, kernel, iterations=5)  # Erode the mask
            cleaned_lines_mask = cv2.dilate(thresh, kernel, iterations=5)  # Dilate the mask
            edges = cv2.Canny(cleaned_lines_mask, 50, 150)  # Apply Canny edge detection
            dilated_edges = cv2.dilate(edges, kernel, iterations=1)  # Dilate the edges
            contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
            self.contour_canvas = np.zeros_like(self.marked_image)  # Create a blank canvas
            cv2.drawContours(self.contour_canvas, contours, -1, (0, 255, 0), 2)  # Draw contours on the canvas
            return contours
        else:
            print("Error: Unable to extract contours from the image.")
            return []

    def crop_sections(self, contours):
        """
        Crops the sections of the chessboard based on the detected contours.

        Args:
            contours (list): A list of contours detected in the image.

        Returns:
            list: A list of cropped sections from the chessboard.
        """
        if self.status > 1 and self.marked_image is not None and contours:
            cropped_sections = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)  # Get the bounding rectangle for each contour
                section = self.marked_image[y:y+h, x:x+w].copy()  # Crop the section from the marked image
                cropped_sections.append(section)

            average_section_size = sum(section.shape[0] * section.shape[1] for section in cropped_sections) / len(cropped_sections)  # Calculate the average section size
            cropped_sections = [section for section in cropped_sections if (section.shape[0] * section.shape[1]) >= (0.7 * average_section_size)]  # Filter out small sections
            cropped_sections.reverse()  # Reverse the order of the cropped sections
            return cropped_sections
        else:
            print("Error: Unable to crop sections from the image.")
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
            black = color1 if color1 > color2 else color2  # Assign the higher intensity to black
            white = color2 if color1 > color2 else color1  # Assign the lower intensity to white
            return black, white
        else:
            print("Error: No cropped sections available to determine colors.")
            return None, None

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
        if cropped_sections and black is not None and white is not None:
            canvas_size = 1000
            canvas = np.ones((canvas_size, canvas_size, 3), dtype=np.uint8) * 255  # Create a white canvas
            square_size = canvas_size // self.square_size

            for i, section in enumerate(cropped_sections):
                gray = cv2.cvtColor(section, cv2.COLOR_BGR2GRAY)  # Convert the section to grayscale
                avg_intensity = np.mean(gray)  # Calculate the average intensity of the section
                square_type = "Black Square" if abs(avg_intensity - black) > abs(avg_intensity - white) else "White Square"  # Determine the square type
                square_color = (0, 0, 0) if square_type == "Black Square" else (255, 255, 255)  # Set the square color
                row = i // self.square_size  # Calculate the row index
                col = i % self.square_size  # Calculate the column index
                cv2.rectangle(canvas, (col * square_size, row * square_size),
                              ((col + 1) * square_size, (row + 1) * square_size),
                              square_color, -1)  # Draw the square on the canvas

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

                if (square_type == "Black Square" and abs(threshold_value - avg_intensity) > self.BLACK_S_WHITE_P) or (
                        square_type == "White Square" and abs(threshold_value - avg_intensity) > self.WHITE_S_WHITE_P and abs(
                        threshold_value - avg_intensity) < self.WHITE_S_BLACK_P):
                    piece_color = 'White'  # Identify the piece as white
                    center_x = int((col + 0.5) * square_size)  # Calculate the center x-coordinate
                    center_y = int((row + 0.5) * square_size)  # Calculate the center y-coordinate
                    cv2.circle(canvas, (center_x, center_y), radius=10, color=(255, 0, 0), thickness=-1)  # Draw a red circle for white pieces
                elif (square_type == "Black Square" and abs(threshold_value - avg_intensity) > self.BLACK_S_BLACK_P) > (
                        square_type == "White Square" and abs(threshold_value - avg_intensity) > self.WHITE_S_BLACK_P):
                    piece_color = 'Black'  # Identify the piece as black
                    center_x = int((col + 0.5) * square_size)
                    center_y = int((row + 0.5) * square_size)
                    cv2.circle(canvas, (center_x, center_y), radius=10, color=(0, 0, 255), thickness=-1)  # Draw a blue circle for black pieces
                else:
                    piece_color = 'No'  # No piece detected

            return canvas
        else:
            print("Error: Unable to identify pieces on the chessboard.")
            return None

    def display_images(self):
        """
        Displays the cleaned mask, marked image, and contour canvas in separate windows.
        """
        if self.status > 2:
            cv2.imshow("Cleaned Mask", self.cleaned_mask)  # Display the cleaned mask
            cv2.imshow("Marked Image", self.marked_image)  # Display the marked image
            cv2.imshow("Contour Canvas", self.contour_canvas)  # Display the contour canvas
            cv2.waitKey(0)  # Wait for a key press
            cv2.destroyAllWindows()  # Close all windows
        else:
            print("Error: Processed images are not available.")

    def run(self):
        """
        Runs the entire pipeline for chessboard detection and piece identification.
        """
        if self.status == -1:
            print("Error: Unable to run the pipeline due to image loading issue.")
            return

        self.preprocess_image()  # Preprocess the image
        if self.status == 1:
            self.detect_lines()  # Detect lines
            if self.status == 2:
                contours = self.extract_contours()  # Extract contours
                cropped_sections = self.crop_sections(contours)  # Crop sections
                if cropped_sections:
                    black, white = self.determine_colors(cropped_sections)  # Determine colors
                    if black is not None and white is not None:
                        canvas = self.identify_pieces(cropped_sections, black, white)  # Identify pieces and draw on canvas
                        if canvas is not None:
                            cv2.imwrite('Detected Squares.jpg', canvas)  # Save the canvas as an image
                            self.status = 3  # Update status to 3

        if self.status == 3:
            self.display_images()  # Display the processed images

if __name__ == "__main__":
    detector = ChessboardDetector('chessboard.jpg')  # Create an instance of the ChessboardDetector class
    detector.run()  # Run the pipeline