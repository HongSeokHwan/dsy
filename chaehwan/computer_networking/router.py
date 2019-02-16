import socket
import random
from queue import Queue
import os
import json
import logging.config

import networking


class Router(object):
    def __init__(self, drop_rate):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.drop_rate = drop_rate
        self.buffer_size = 1024
        self.receiving_buffer = Queue()
        self.sending_buffer = Queue() 
        self.source_ip = "127.0.0.1"
        self.source_port = None
        self.source_address = None
        self.destination_ip = "127.0.0.1"
        self.destination_port = None
        self.destination_address = None

    def set_source(self, source_address):
        self.source_port = source_address[1]
        self.source_address = source_address

    def receive(self, buffer_size):
        received = self.socket.recvfrom(buffer_size)
        received_data = networking.restore_segment(received[0])
        sender_address = received[1]
        if random.random() > self.drop_rate:
            self.receiving_buffer.put(received_data, block=True)
        else:
            logging.info("Packet dropped")
        self.set_source(sender_address)
        packet = self.receiving_buffer.get(block=True)
        return packet

    def set_destination(self, destination_port):
        self.destination_ip = "127.0.0.1"
        self.destination_port = destination_port
        self.destination_address = (self.destination_ip, 
                                    self.destination_port)

    def send(self, packet):
        self.sending_buffer.put(packet)
        packet = self.sending_buffer.get(block=True)
        packet = networking.convert_into_byte_stream(packet)
        self.socket.sendto(packet, self.destination_address)

    def route(self):
        segment = self.receive(self.buffer_size)
        logging.info("Router received: %s", segment)
        self.set_destination(destination_port=segment.destination_port)
        self.send(segment)
        logging.info("Router sent: %s", segment)

def setup_logger(default_path = 'log.json', 
                default_level='logging.INFO', 
                env_key = 'LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as config_file:
            config = json.load(config_file)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == "__main__":
    setup_logger()
    TCPRouter = Router(drop_rate = 0)
    TCPRouter.socket.bind(('', 9000))
    logging.info("Router info") 
    logging.info("drop_rate: %d", TCPRouter.drop_rate)
    while True:
        TCPRouter.route()