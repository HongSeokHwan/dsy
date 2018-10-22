import logging

import networking
import logger


logger.setup_logger()
logging.info("Server started")

server_port = 10000
server_socket = networking.Socket()
server_socket.bind('', server_port)
server_socket.listen(5)
logging.info("Server is ready to receive")
"""
while True:
    connection_socket = server_socket.accept()
    received_data = connection_socket.receive(1024)
    logging.info("Server received: %s", received_data)
    connection_socket.send(received_data)
    logging.info("Server sent: %s", received_data)
"""
while True:
    received_data = server_socket.receive(1024)
    logging.info("Server received: %s", received_data)
    server_socket.send(received_data)
    logging.info("Server sent: %s", received_data)