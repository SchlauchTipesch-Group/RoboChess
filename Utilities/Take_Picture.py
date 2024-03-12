import cv2

class pictureTaker:
    """
    This class is responsible for capturing an image from a camera and saving it to a file.

    Attributes:
        _port (int): The index of the camera port to use.
        _saveFile_name (str): The name of the file to save the captured image.
    """

    def __init__(self, port, saveFile_name):
        """
        Initializes the pictureTaker object.

        Args:
            port (int): The index of the camera port to use.
            saveFile_name (str): The name of the file to save the captured image (without extension).
        """
        self._port = port
        self._saveFile_name = f"{saveFile_name}.jpg"

    def Take_Picture(self):
        """
        Captures an image from the camera and saves it to a file.

        This method opens the specified camera port, captures a single frame from the camera,
        and saves the captured frame as a JPEG image to the file specified by _saveFile_name.

        If an error occurs while opening the camera or capturing the frame, an appropriate
        error message is printed, and the program exits.

        After saving the image, the camera is released and closed.
        """
        # Open the camera specified by self._port
        cap = cv2.VideoCapture(self._port)

        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Couldn't open camera")
            exit()

        # Capture a single frame from the camera
        ret, frame = cap.read()

        # If the frame was captured successfully (ret is True)
        if ret:
            # Save the captured frame as a JPEG image
            cv2.imwrite(self._saveFile_name, frame)
        else:
            print("Error: Failed to capture frame")

        # Release and close the camera
        cap.release()