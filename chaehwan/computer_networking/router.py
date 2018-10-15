import socket
import os
import json
import logging.config
import random

import networking


class Router(object):
    def __init__(self, drop_rate):
        self.socket = networking.Socket()
        self.buffer_size = 1024
        self.source_address = None
        self.destination_address = None
        self.drop_rate = drop_rate
        self.out_of_order_rate = 0.2

    def create_socket(self, socket_name):
        self.socket.socket_name = socket_name
        self.socket.create()

    def bind(self, host_ip, host_port_number):
        self.socket.bind(host_ip, host_port_number)

    def set_remote(self, remote_ip, remote_port_number):
        self.socket.set_remote(remote_ip, remote_port_number)

    def ecncapsulate(self, data):
        pass

    def decapsulate(self, segment):
        data = segment.payload
        data = networking.decode_data(data)
        return data

    def write(self, segment):
        if random.random() > self.drop_rate: 
            self.socket.sending_buffer.append(segment)
        else:
            router_logger.info("Packet dropped")

    def encapsulate(self, data):
        data = networking.encode_data(data)
        return data

    def read(self, segment):
        data = self.decapsulate(segment)
        return data

    def send(self, data):
        self.write(data)
        while not self.socket.sending_buffer:
            pass
        segment = self.socket.sending_buffer.popleft()
        self.socket.send(segment)

    def receive(self, buffer_size):
        segment = self.socket.receive(buffer_size)
        self.socket.receiving_buffer.append(segment)
        segment = self.socket.receiving_buffer.popleft()
        # data = self.read(segment)
        router_logger.info("Router received: %s", segment)
        return segment

    def route(self, remote_ip, remote_port_number):
        received_pakcet = self.receive(self.buffer_size)
        self.set_remote(remote_ip, remote_port_number)
        self.send(received_pakcet)

    def shuffle(self):
        pass


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
    router_logger = logging.getLogger("router_logger")
    setup_logger()

    tcp_router = Router(drop_rate = 0)
    tcp_router.create_socket(socket_name="router socket")
    tcp_router.bind('', 9000)
    while True:
        tcp_router.route("127.0.0.1", 10000)
        tcp_router.route("127.0.0.1", 8000)