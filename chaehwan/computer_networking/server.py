import socket
import os
import json
import logging.config
from collections import deque
import queue
import threading

import networking


class Server(object):
    def __init__(self):
        self.socket = networking.Socket()
        self.client_socket = []
        self.proxy_buffer = networking.Buffer(max_size=1024)
        self.syn_queue = None
        self.accept_queue = None
        self.tcp_control_block = networking.TCPControlBlock(state="CLOSED", 
                                    sequence_number=0, ack_number = 0, 
                                    last_byte_received=0, last_byte_read=0, 
                                    last_byte_sent=0, last_byte_acked=0, 
                                    receive_window=0, congestion_window=0, 
                                    timer=threading.Timer(interval=1.0,
                                        function=self.send_syn_ack), 
                                    maximum_segment_size=512,
                                    ssthresh=1024)

    def log_status(self):
        server_logger.info("Server state: %s", 
                            self.tcp_control_block.state)
        server_logger.info("Seq#: %d", 
                            self.tcp_control_block.sequence_number)
        server_logger.info("ACK#: %d", 
                            self.tcp_control_block.ack_number)

    def create_socket(self, socket_name):
        self.socket.socket_name = socket_name
        self.socket.create()
        self.log_status()

    def bind(self, host_ip, host_port_number):
        self.socket.bind(host_ip, host_port_number)

    def set_timer(self, interval, function):
        self.tcp_control_block.timer.interval = interval
        self.tcp_control_block.timer.function = function

    def send_segment(self, segment):
        self.socket.sending_buffer.append(segment)
        sending_segment = self.socket.sending_buffer[0]
        self.socket.send(sending_segment)

    def receive_segment(self):
        segment = self.socket.receive(1024)
        self.socket.receiving_buffer.append(segment)
        segment = self.socket.receiving_buffer.popleft()
        return segment

    def receive_syn(self, segment):
        self.log_status()
        if segment.syn == 1:
            self.tcp_control_block.ack_number = segment.sequence_number + 1
            self.tcp_control_block.state = "SYN RCVD"
            self.syn_queue.put((segment.source_port, segment.destination_port))

    def send_syn_ack(self):
        """Send segment with SYN and ACK on"""
        segment = self.tcp_control_block.create_segment()
        segment.syn = 1
        segment.ack = 1
        # arbitrary initial sequence number(server) : 500
        self.tcp_control_block.sequence_number = 500
        segment.sequence_number = self.tcp_control_block.sequence_number
        self.tcp_control_block.sequence_number += 1
        self.set_timer(interval=1.0, function=self.send_syn_ack)
        if not self.tcp_control_block.timer.is_alive():
            self.tcp_control_block.timer.start()
        self.send_segment(segment)
        self.log_status()

    def receive_ack(self, segment):
        if segment.ack == 1 and self.tcp_control_block.state == "SYN RCVD":
            self.tcp_control_block.timer.cancel()
            accepted = self.syn_queue.get(block=True)
            self.accept_queue.put(accepted, block=True)
            self.tcp_control_block.state = "ESTABLISHED"
            self.tcp_control_block.ack_number = segment.sequence_number + 1
            self.socket.sending_buffer.popleft()
        self.log_status()

    def listen(self, backlog):
        self.syn_queue = queue.Queue()
        self.accept_queue = queue.Queue(maxsize=backlog)
        self.tcp_control_block.state = "LISTEN"
        # When the accept queue is full then simply drop the SYN packet
        if not self.accept_queue.full():
            syn_segment = self.receive_segment()
            self.receive_syn(syn_segment)
            self.send_syn_ack()
            ack_segment = self.receive_segment()
            self.receive_ack(ack_segment)
        else:
            server_logger.info("backlog queue is full")

    def initialize_socket(self, remote_port_number, host_port_number):
        client_socket = networking.Socket()
        client_socket.create()
        client_socket.remote_ip = "127.0.0.1"
        client_socket.remote_port_number = remote_port_number
        client_socket.host_ip = "127.0.0.1"
        client_socket.host_port_number = host_port_number
        return client_socket

    def accept(self):
        """Returns pair (connection, address), 
           connection : new socket object usable to send and receive data 
           address : the address bound to the socket on the other end of 
           connection 
        """
        accepted = self.accept_queue.get(block=True)
        client_socket = self.initialize_socket(
                            remote_port_number=accepted[0],
                            host_port_number=accepted[1])
        client_address = (client_socket.remote_ip, client_socket.remote_port_number)
        return (client_socket, client_address)

    def ecncapsulate(self, data):
        segment = self.tcp_control_block.create_segment()
        segment.payload = data
        return segment
        
    def decapsulate(self, segment):
        self.tcp_control_block.ack_number = segment.sequence_number + 1
        data = segment.payload
        data = networking.decode_data(data)
        return data
        
    def write(self, data):
        data = self.proxy_buffer.write(data)
        segment = self.ecncapsulate(data)
        self.socket.sending_buffer.append(segment)

    def read(self, segment):
        data = self.decapsulate(segment)
        return data

    def send(self, data):
        """Sends data after load it to the segment"""
        self.write(data)
        segment = self.socket.sending_buffer[0]
        self.socket.send(segment)

    def receive(self, buffer_size):
        """Receive data in the segment from the remote host"""
        segment = self.socket.receive(buffer_size)
        self.socket.receiving_buffer.append(segment)
        segment = self.socket.receiving_buffer.popleft()
        data = self.read(segment)
        server_logger.info("Server received: %s", data)
        return data

    def close(self):
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
    server_logger = logging.getLogger("server_logger")
    setup_logger()

    tcp_server = Server()
    tcp_server.create_socket(socket_name="server socket")
    tcp_server.bind('', 10000)
    tcp_server.listen(5)
#    received_data = tcp_server.receive(1024)
#    tcp_server.send(received_data)