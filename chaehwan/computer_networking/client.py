import logging

import networking
import logger


logger.setup_logger()
logging.info("Client started")

client_socket = networking.Socket()
client_socket.bind('', 8000)
client_socket.set_remote("127.0.0.1", 10000)
client_socket.connect()
while True:
    message = input("Enter the message: ")
    if message == "exit":
        break
    client_socket.send(message)
    logging.info("Client sent: %s", message)
    received_data = client_socket.receive(1024)
    logging.info("Client received: %s", received_data)