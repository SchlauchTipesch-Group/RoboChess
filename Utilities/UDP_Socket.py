import socket

class udpSocket():
    """
    A class representing a UDP socket for sending data.

    Attributes:
        _udp_ip (str): The IP address of the UDP socket.
        _udp_port (int): The port number of the UDP socket.
        _udp_socket (socket.socket): The UDP socket object.
    """

    def __init__(self, ip, port):
        """
        Initializes the UDP socket with the provided IP address and port.

        Args:
            ip (str): The IP address of the UDP socket.
            port (int): The port number of the UDP socket.
        """
        # IP address and port
        self._udp_ip = ip 
        self._udp_port = port

        # Create a UDP socket
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update_status(self, data):
        """
        Sends data over the UDP socket to the specified IP address and port.

        Args:
            data (str): The data to be sent over the UDP socket.
        """
        # Send data
        self._udp_socket.sendto(data.encode('utf-8'), (self._udp_ip, self._udp_port))

    def __del__(self):
        """
        Closes the UDP socket.
        """
        # Close the socket
        self._udp_socket.close()
