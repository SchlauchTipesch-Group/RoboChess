# Chess Game Detection and Move Making

This project is designed to detect a chessboard, identify the pieces on it, make moves for the player and the bot (powered by the Stockfish chess engine), and communicate the game status over a UDP socket.

## File Structure

The project consists of the following Python files:

### 1. `Log.py`

This file contains a `Log` class responsible for logging messages and sending them over a UDP socket.

#### `Log` Class

- **Attributes**:
  - `_socket (udpSocket)`: An instance of the `udpSocket` class used for sending messages over UDP.

- **Methods**:
  - `__init__(self, ip, port)`: Initializes the `Log` instance with the specified IP address and port number.
  - `log(self, status)`: Logs a message based on the provided status and sends it over the UDP socket. The `status` argument is a list containing a numeric status code and a string identifier for the log message.

### 2. `Take_Picture.py`

This file contains a `pictureTaker` class responsible for capturing an image from a camera and saving it to a file.

#### `pictureTaker` Class

- **Attributes**:
  - `_port (int)`: The index of the camera port to use.
  - `_saveFile_name (str)`: The name of the file to save the captured image.

- **Methods**:
  - `__init__(self, port, saveFile_name)`: Initializes the `pictureTaker` object with the specified camera port index and file name for saving the captured image.
  - `Take_Picture(self)`: Captures an image from the camera and saves it to the file specified by `_saveFile_name`.

### 3. `UDP_Socket.py`

This file contains a `udpSocket` class representing a UDP socket for sending data.

#### `udpSocket` Class

- **Attributes**:
  - `_udp_ip (str)`: The IP address of the UDP socket.
  - `_udp_port (int)`: The port number of the UDP socket.
  - `_udp_socket (socket.socket)`: The UDP socket object.

- **Methods**:
  - `__init__(self, ip, port)`: Initializes the UDP socket with the provided IP address and port.
  - `update_status(self, data)`: Sends data over the UDP socket to the specified IP address and port.
  - `__del__(self)`: Closes the UDP socket.

## Additional Notes

- The `Log` class is responsible for logging messages and sending them over a UDP socket. It formats the log messages with a timestamp and obtains the log message text from the `getLogComment` function 'in log_comments'.
- The `pictureTaker` class handles capturing an image from a camera and saving it to a file. It opens the specified camera port, captures a single frame, and saves the captured frame as a JPEG image.
- The `udpSocket` class represents a UDP socket for sending data. It creates a UDP socket object and provides a method `update_status` to send data over the socket to a specified IP address and port.

For detailed information on the classes and their methods, refer to the docstrings in each file.