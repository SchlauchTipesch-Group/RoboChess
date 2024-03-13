from UDP_Socket import udpSocket
from log_comments import getLogComment
from datetime import datetime

class Log:
    """
    This class is responsible for logging messages and sending them over a UDP socket.

    Attributes:
        _socket (udpSocket): An instance of the udpSocket class used for sending messages over UDP.

    Methods:
        __init__(self, ip, port): Initializes the Log instance with the specified IP address and port number.
        log(self, status): Logs a message based on the provided status and sends it over the UDP socket.
    """

    def __init__(self, ip, port):
        """
        Initializes the Log instance with the specified IP address and port number.

        Args:
            ip (str): The IP address to which the UDP socket should bind.
            port (int): The port number to which the UDP socket should bind.
        """
        self._socket = udpSocket(ip, port)

    def log(self, status):
        """
        Logs a message based on the provided status and sends it over the UDP socket.

        Args:
            status (list): A list containing two elements:
                - status[0] (int): A numeric status code.
                - status[1] (str): A string identifier for the log message.

        Returns:
            str: The sealed message that was sent over the UDP socket.

        The log message format is as follows:
        [YYYY/MM/DD/HH:MM:SS] -> <log_message>

        Where:
            - YYYY/MM/DD/HH:MM:SS is the current timestamp.
            - <log_message> is the log message obtained from the getLogComment function based on the provided status.
        """

        # Get the current timestamp
        current_time = datetime.now()

        # Format the timestamp as YYYY/MM/DD/HH:MM:SS
        formatted_time = current_time.strftime("%Y/%m/%d/%H:%M:%S")

        # Get the log message based on the provided status
        message = getLogComment(status[0], status[1])

        # Construct the sealed message with the timestamp and log message
        sealed_message = f"[{formatted_time}] -> {message}\n"

        # Send the sealed message over the UDP socket
        self._socket.update_status(sealed_message)

        # Return the sealed message
        return sealed_message