import socket
import pickle
import threading
import logging
from queue import Queue


class Segment(object):
    def __init__(self, source_port, 
                destination_port, sequence_number, 
                acknowledge_number,
                ack, syn,
                fin, checksum,
                receive_window, payload):
        self.source_port = source_port
        self.destination_port = destination_port
        self.sequence_number = sequence_number
        self.acknowledge_number = acknowledge_number
        self.ack = ack
        self.syn = syn
        self.fin = fin
        self.checksum = checksum
        self.receive_window = receive_window
        self.payload = payload

    def __str__(self):
        return "\nSegment \n \tsource_port: {0}\n \tdestination_port: {1}\n \
       sequence_number: {2}\n \tack_number: {3}\n \tpayload: {4}\n\
       ".format(self.source_port, self.destination_port, 
            self.sequence_number, self.acknowledge_number,
            self.payload)


class TCPControlBlock(object):
    def __init__(self):
        self.state = "CLOSED"
        self.local_ip = "127.0.0.1"
        self.local_port = None
        self.local_address = None
        self.router_ip = "127.0.0.1"
        self.router_port = 9000
        self.router_address = (self.router_ip, self.router_port)
        self.remote_ip = "127.0.0.1"
        self.remote_port = None
        self.remote_address = None
        self.sender_isn = 0 # sender's initial sequence number
        self.sending_sequence_number = 0 # sender's next sequence number
        self.send_base = 0 # lowest unacked byte in the sequence
        self.receiver_isn = 0 # receiver's initial sequence number
        self.receiving_sequence_number = 0 # receiver's next sequence number
        self.last_byte_received = 0
        self.last_byte_read = 0
        self.last_byte_acked = 0
        self.last_byte_sent = 0
        self.receiving_window = 0
        self.maximum_segment_size = 3 # unit of mss : bytes
        self.sending_window = 1 * self.maximum_segment_size
        self.timer = threading.Timer(interval=0, function=None)
        self.ssthresh = 1024
        self.rtt_estimate = 3
        self.deviation_rtt = 1
        self.time_out_interval = 5
        self.retransmission_count = 0
        self.duplicate_ack_count = 0


class Buffer(object):
    def __init__(self, max_size):
        self.head = 0
        self.tail = 0
        self.size = 0
        self.max_size = max_size
        self.buffer = bytearray()

    def is_empty(self):
        if self.head == self.tail:
            return True
        else:
            return False

    def is_full(self):
        if self.head == (self.tail % self.max_size) + 1:
            return True
        else:
            return False

    def write(self, data):
        if self.is_full():
            logging.info("Buffer is Full")
        elif data is not None:
            data_size = len(data)
            self.tail = (self.tail + data_size) % self.max_size
            self.size += len(data)
            self.buffer += data

    def read(self, data_size):
        data = None
        if self.is_empty():
            logging.info("Buffer is empty")
        elif self.size >= data_size:
            data = self.buffer[self.head:self.head+data_size]
            self.size -= data_size
            self.head = (self.head + data_size) % self.max_size
        else:
            # partial success
            logging.info("%d size data is unavailable", data_size)
            logging.info("just read %d size data", self.size)
            data_size = self.size
            data = self.buffer[self.head:self.head+data_size]
            self.size -= data_size
            self.head = (self.head + data_size) % self.max_size
        return data

    def peek(self, data_size):
        data = None
        if self.is_empty():
            logging.info("Buffer is empty")
        elif self.size >= data_size:
            data = self.buffer[self.head:self.head+data_size]
        else:
            # partial success
            logging.info("%s size data is unavailable", data_size)
            logging.info("just peek %d size data", self.size)
            data_size = self.size
            data = self.buffer[self.head:self.head+data_size]
        return data

    def flush(self):
        self.head = 0
        self.tail = 0
        self.size = 0


class Socket(object):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_number = -1 # initial state : no client socket exists
        self.proxy_buffer = Buffer(max_size=1024)
        self.copy_size = 4
        self.sending_buffer = Buffer(max_size=1024)
        self.receiving_buffer = Buffer(max_size=1024)
        self.tcb = TCPControlBlock()
        self.syn_queue = None
        self.accept_queue = None

    def log_status(self):
        logging.info("State: %s", 
                            self.tcb.state)
        logging.info("Seq#: %d", 
                            self.tcb.sending_sequence_number)
        logging.info("ACK#: %d", 
                            self.tcb.receiving_sequence_number)

    def bind(self, local_ip, local_port):
        self.tcb.local_ip = local_ip
        self.tcb.local_port = local_port
        self.tcb.local_address = (self.tcb.local_ip, self.tcb.local_port)
        self.socket.bind(self.tcb.local_address)

    def set_remote(self, remote_ip, remote_port):
        self.tcb.remote_ip = remote_ip
        self.tcb.remote_port = remote_port
        self.tcb.remote_address = (remote_ip, remote_port)

    def set_timer(self, interval, action, kwargs=None):
        self.tcb.timer.interval = 10.0
        self.tcb.timer.function = action
        self.tcb.timer.kwargs = kwargs

    def initialize_segment(self):
        # check if it possible to tranfer the data
        # considering the tcb
        total_buffer_size = len(self.receiving_buffer.buffer)
        occupied_buffer_size = self.tcb.last_byte_received \
            - self.tcb.last_byte_read
        segment = Segment(source_port = None,
            destination_port= None,
            sequence_number = self.tcb.sending_sequence_number,
            ack = 0,
            acknowledge_number = self.tcb.receiving_sequence_number,
            syn = 0,
            fin = 0,
            checksum = 0,
            receive_window = total_buffer_size - occupied_buffer_size,
            payload = None)
        return segment

    def set_syn_bit(self, segment):
        if (self.tcb.state == "CLOSED") or \
                (self.tcb.state == "SYN_SENT"):
            segment.syn = 1
            self.set_timer(interval=3.0,
                    action=self.send_segment, 
                    kwargs=({"control_bits":["SYN"]}))
            self.tcb.state = "SYN_SENT"
        else:
            logging.info("It's invalid state to set SYN")

    def set_syn_ack_bit(self, segment):
        if self.tcb.state == "SYN_RCVD":
            segment.syn = 1
            segment.ack = 1
            self.set_timer(interval=3.0,
                    action=self.send_segment, 
                    kwargs=({"control_bits":["SYN", "ACK"]}))
        else:
            logging.info("It's invalid state to set SYN/ACK")

    def set_ack_bit(self, segment):
        if self.tcb.state == "SYN_SENT":
            segment.ack = 1
            self.tcb.state = "ESTABLISHED"
        else:
            logging.info("It's invalid state to set ACK")

    def set_fin_bit(self, segment):
        pass

    def set_control_bits(self, segment, control_bits):
        if "SYN" in control_bits:
            self.set_syn_bit(segment)
            if "ACK" in control_bits:
                self.set_syn_ack_bit(segment)
            if not self.tcb.timer.is_alive():
                self.tcb.timer.start()
        if "ACK" in control_bits:
            self.set_ack_bit(segment)
        if "FIN" in control_bits:
            self.set_fin_bit(segment)
        segment.payload = None

    def is_sendable(self, segment):
        pass

    def set_port(self, segment):
        segment.source_port = self.tcb.local_port
        segment.destination_port = self.tcb.remote_port

    def set_acknowledge_number(self, segment):
        if segment.ack == 1:
            self.acknowledge_number = self.tcb.receiving_sequence_number

    def set_sequence_number(self, segment):
        # consider the situation that the control bit is set
        if segment.payload != None:
            segment.sequence_number = self.tcb.sending_sequence_number
            payload_size = len(segment.payload)
            self.tcb.sending_sequence_number += payload_size
        else:
            segment.sequence_number = self.tcb.sender_isn
            self.tcb.sending_sequence_number += 1

    def set_payload(self, segment):
        # determine the payload size depending on the cwnd and etc
        payload_size = self.tcb.maximum_segment_size
        payload = self.sending_buffer.peek(payload_size)
        segment.payload = payload

    def calculate_checksum(self, segment):
        pass

    def set_receive_window(self, segment):
        pass

    def encapsulate(self, segment, control_bits):
        self.is_sendable(segment)
        self.set_port(segment)
        self.set_acknowledge_number(segment)
        self.calculate_checksum(segment)
        self.set_receive_window(segment)
        self.set_control_bits(segment, control_bits)
        self.set_payload(segment)
        self.set_sequence_number(segment)
        return segment

    def handle_syn_bit(self, segment):
        if self.tcb.state == "LISTEN":
            self.tcb.state = "SYN_RCVD"
            self.syn_queue.put((segment.source_port, 
                                segment.destination_port))
        else:
            logging.info("It's invalid state to handle SYN")

    def handle_syn_ack_bit(self, segment):
        if self.tcb.state == "SYN_SENT":
            self.tcb.timer.cancel()
            print("after cancel")
            print(self.tcb.timer.is_alive())
        else:
            logging.info("It's invalid state to handle SYN/ACK")

    def handle_ack_bit(self, segment):
        if self.tcb.state == "SYN_RCVD":
            accepted = self.syn_queue.get(block=True)
            self.accept_queue.put(accepted)
            self.tcb.state = "ESTABLISHED"
        if self.tcb.state == "ESTABLISHED":
            if segment.acknowledge_number > self.tcb.send_base:
                self.tcb.send_base = segment.acknowledge_number
                last_acked = segment.acknowledge_number - 1
                acked_size = last_acked - self.tcb.send_base
                self.sending_buffer.read(acked_size)

    def handle_fin_bit(self, segment):
        pass

    def verify_checksum(self, segment):
        pass

    def handle_control_bits(self, segment):
        if segment.syn == 1:
            self.handle_syn_bit(segment)
            if segment.ack == 1:
                self.handle_syn_ack_bit(segment)
        if segment.ack == 1:
            self.handle_ack_bit(segment)
        if segment.fin == 1:
            self.handle_fin_bit(segment)

    def demultiplex(self, segment):
        """Find the correct TCB for the segment"""
        # check there's correct TCB
        # destination port
        self.tcb.remote_port = segment.source_port

    def is_receivable(self, segment):
        """Verify the segment is acceptable for the current window"""
        pass

    def update_rwnd(self, segment):
        self.tcb.receive_window = segment.receive_window
        pass

    def update_receiving_sequence_number(self, segment):
        if segment.payload != None:
            payload_size = len(segment.payload)
            self.tcb.receiving_sequence_number = \
            segment.sequence_number + payload_size
        else:
            self.tcb.receiving_sequence_number = \
            segment.sequence_number + 1

    def get_payload(self, segment):
        data = segment.payload
        if data is not None:
            self.send_segment(control_bits="ACK")
        return data

    def decapsulate(self, segment):
        self.verify_checksum(segment)
        self.demultiplex(segment)
        self.update_receiving_sequence_number(segment)
        # acknowledgement number
        self.is_receivable(segment) # rwnd
        self.handle_control_bits(segment)
        self.update_rwnd(segment) # update remote rwnd
        data = self.get_payload(segment)
        return data

    def send_segment(self, control_bits=[]):
        """Sends segment to the remote host"""
        self.log_status()
        segment = self.initialize_segment()
        segment = self.encapsulate(segment, control_bits)
        segment = convert_into_byte_stream(segment)
        self.socket.sendto(segment, self.tcb.router_address) 
        self.log_status()

    def receive_segment(self, buffer_size):
        """Receive segment from the remote host and write it to 
           the receiving buffer"""
        received = self.socket.recvfrom(buffer_size)
        segment = restore_segment(received[0])
        sender_address = received[1]
        payload = self.decapsulate(segment)        
        self.receiving_buffer.write(payload)
        print("payload :", payload)
        self.tcb.remote_address = sender_address
        self.log_status()

    def send(self, data):
        byte_stream = encode_data(data)
        self.proxy_buffer.write(byte_stream)
        data = self.proxy_buffer.read(self.copy_size)
        self.sending_buffer.write(data)
        self.send_segment()

    def receive(self, buffer_size):
        self.receive_segment(buffer_size)
        data = self.receiving_buffer.read(buffer_size)
        data = decode_data(data)
        return data

    def connect(self):
        logging.info("Client is trying to connect...")
        self.send_segment(control_bits=["SYN"])
        self.receive_segment(1024)
        self.send_segment(control_bits=["ACK"])
        logging.info("Connected...")

    def listen(self, backlog):
        self.syn_queue = Queue()
        self.accept_queue = Queue(maxsize=backlog)
        self.tcb.state = "LISTEN"
        if not self.accept_queue.full():
            self.receive_segment(1024)
            self.send_segment(control_bits=["SYN", "ACK"])
            self.receive_segment(1024)
        else:
            logging.info("backlog queue is full")

    def initialize_socket(self, local_port, remote_port):
        client_socket = Socket()
        client_socket.tcb.remote_ip = "127.0.0.1"
        client_socket.tcb.local_port = local_port
        client_socket.tcb.local_ip = "127.0.0.1"
        client_socket.tcb.remote_port = remote_port
        return client_socket

    def accept(self):
        established = self.accept_queue.get(block=True)
        connection_socket = self.initialize_socket(established[0], established[1])
        connection_socket.bind('', self.tcb.local_port+1000)
        # originally, welcome socket and client socket share the same port 
        # but they use the different port in the code because of the matter 
        # of implementation
        return connection_socket

    def close(self):
        pass


def convert_into_byte_stream(segment):
    if isinstance(segment, Segment):
        byte_stream = pickle.dumps(segment)
        return byte_stream
    else:
        raise TypeError("Input is not a segment type")


def restore_segment(segment):
    if isinstance(segment, bytes):
        restored_segment = pickle.loads(segment)
        return restored_segment
    else:
        raise TypeError("Input is not a bytes type")


def encode_data(data):
    if isinstance(data, str):
        encoded_data = data.encode('utf-8')
    else:
        encoded_data = data
    return encoded_data


def decode_data(data):
    if isinstance(data, bytes):
        decoded_data = data.decode('utf-8')
    elif isinstance(data, bytearray):
        decoded_data = data.decode('utf-8')
    else:
        decoded_data = data
    return decoded_data