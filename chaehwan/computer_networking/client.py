import socket
import logging.config
import os
import json
from collections import deque
import threading

import networking


class Client(object):
    def __init__(self):
        self.socket = networking.Socket()
        self.proxy_buffer = networking.Buffer(max_size=1024)
        self.tcp_control_block = networking.TCPControlBlock(state="CLOSED", 
                                    sequence_number=0, ack_number = 0, 
                                    last_byte_received=0, last_byte_read=0, 
                                    last_byte_sent=0, last_byte_acked=0, 
                                    receive_window=0, congestion_window=0, 
                                    timer=threading.Timer(interval= 1.0, 
                                        function=self.send_syn), 
                                    maximum_segment_size=512,
                                    ssthresh=1024)

    def log_status(self):
        client_logger.info("Client state: %s", 
                            self.tcp_control_block.state)
        client_logger.info("Seq#: %d", 
                            self.tcp_control_block.sequence_number)
        client_logger.info("ACK#: %d", 
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
        
    def set_remote(self, remote_ip, remote_port_number):
        self.socket.set_remote(remote_ip, remote_port_number)

    def send_segment(self, segment):
        self.socket.sending_buffer.append(segment)
        sending_segment = self.socket.sending_buffer[0]
        self.socket.send(sending_segment)

    def receive_segment(self):
        segment = self.socket.receive(1024)
        self.socket.receiving_buffer.append(segment)
        segment = self.socket.receiving_buffer.popleft()
        return segment

    def send_syn(self):
        if (self.tcp_control_block.state == "CLOSED") or \
                (self.tcp_control_block.state == "SYN_SENT"):
            segment = self.tcp_control_block.create_segment()
            segment.syn = 1
            # Arbitrary initial sequence number(client) : 100
            self.tcp_control_block.sequence_number = 100
            segment.sequence_number = self.tcp_control_block.sequence_number
            self.tcp_control_block.sequence_number += 1
            # Set the timer when client sends the SYN segment
            self.set_timer(interval = 1.0, function = self.send_syn)
            if not self.tcp_control_block.timer.is_alive():
                self.tcp_control_block.timer.start()  
            self.send_segment(segment)
            self.tcp_control_block.state = "SYN_SENT"
            self.log_status()
        else:
            client_logger.info("Client: impossible state to send SYN")

    def receive_syn_ack(self, segment):
        if segment.syn == 1 and segment.ack == 1:
            self.tcp_control_block.timer.cancel()
            self.tcp_control_block.ack_number = segment.sequence_number + 1
            self.socket.sending_buffer.popleft()
        self.log_status()

    def send_ack(self):
        segment = self.tcp_control_block.create_segment()
        segment.ack = 1
        segment.sequence_number = self.tcp_control_block.sequence_number
        segment.ack_number = self.tcp_control_block.ack_number
        self.tcp_control_block.sequence_number += 1
        self.send_segment(segment)
        self.tcp_control_block.state = "ESTABLISHED"
        self.log_status()

    def connect(self):
        client_logger.info("Trying to connect to ...")
        self.send_syn()
        syn_ack_segment = self.receive_segment()
        self.receive_syn_ack(syn_ack_segment)
        self.send_ack()
        client_logger.info("Connected ...")

    def ecncapsulate(self, data):
        segment = self.tcp_control_block.create_segment()
        # load source port and dest port to identify the socket
        segment.sequence_number = self.tcp_control_block.sequence_number
            # segment.ack = ack
            # segment.ack_number = self.tcp_control_block.ack_number
            # calculate the checksum
        # Get the receive window by calculating availble buffer space
        receiving_buffer_space = len(self.socket.receiving_buffer)
        occupied_buffer_space = self.tcp_control_block.last_byte_received \
            - self.tcp_control_block.last_byte_read
        self.tcp_control_block.receive_window = receiving_buffer_space \
            - occupied_buffer_space
        segment.receive_window = self.tcp_control_block.receive_window
        # Determine the payload size as the min between cwnd and rwnd
        cwnd = self.tcp_control_block.congestion_window
        rwnd = self.tcp_control_block.receive_window
        payload_size = min(cwnd, rwnd)
        # segment.payload = data
        segment.payload = self.proxy_buffer.read(payload_size)
        return segment
        
    def decapsulate(self, segment):
        # source port and destination port to identify the socket
        if segment.ack == 1:
            # Determine the cwnds depending on the sssthresh
            ssthresh = self.tcp_control_block.ssthresh
            mss = self.tcp_control_block.maximum_segment_size
            cwnd = self.tcp_control_block.congestion_window
            if self.tcp_control_block.congestion_window < ssthresh:
                self.tcp_control_block.congestion_window += mss
            else:
                self.tcp_control_block.congestion_window += (mss/cwnd)
            # triple duplicate ACKs
        # compare with the checksum calculated
        # Store receive window in TCP control block from the segment
        self.tcp_control_block.receive_window = segment.receive_window
        # len(segment.payload)
        data = segment.payload
        data = networking.decode_data(data)
        return data

    def write(self, data):
        """Represents write system call to copy the data of proxy buffer
           to the sending buffer"""
        data = self.proxy_buffer.write(data)
        segment = self.ecncapsulate(data)
        self.socket.sending_buffer.append(segment)

    def read(self, segment):
        data = self.decapsulate(segment)
        return data

    def send(self, data):
        """Sends data after load it to the segment"""
        self.write(data)
        # no popleft to retransmit the data 
        # segment = self.socket.sending_buffer.popleft()
        segment = self.socket.sending_buffer[0]
        self.socket.send(segment)

    def receive(self, buffer_size):
        """Receive data in the segment from the remote host"""
        segment = self.socket.receive(buffer_size)
        self.socket.receiving_buffer.append(segment)
        segment = self.socket.receiving_buffer.popleft()
        data = self.read(segment)
        client_logger.info("Client received: %s", data)
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
    client_logger = logging.getLogger("client_logger")
    setup_logger()

    tcp_client = Client()
    tcp_client.create_socket(socket_name="client socket")
    tcp_client.bind('', 8000)
    tcp_client.set_remote("127.0.0.1", 9000)
    tcp_client.connect()
#    tcp_client.send("hello world")
#    received_data = tcp_client.receive(1024)