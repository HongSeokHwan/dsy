import socket
import logging
import pickle 
from collections import deque
from threading import Timer


class Socket(object):
    def __init__(self):
        self.socket = None
        self.socket_name = None
        self.host_ip = None
        self.host_port_number = None
        self.host_address = None
        self.remote_ip = None
        self.remote_port_number = None
        self.remote_address = (self.remote_ip, self.remote_port_number)
        self.sending_buffer = deque(maxlen=1024)
        self.receiving_buffer = deque(maxlen=1024)

    def create(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except OSError:
            logging.exception("%s creation failed", self.socket_name)
        else:
            logging.info("%s created", self.socket_name)

    def bind(self, host_ip, host_port_number):
        self.host_ip = host_ip
        self.host_port_number = host_port_number
        self.host_address = (self.host_ip, self.host_port_number)
        self.socket.bind(self.host_address)

    def set_remote(self, remote_ip, remote_port_number):
        self.remote_ip = remote_ip
        self.remote_port_number = remote_port_number
        self.remote_address = (remote_ip, remote_port_number)

    def send(self, segment):
        """Sends segment to the remote host"""
        segment = convert_into_byte_stream(segment)        
        self.socket.sendto(segment, self.remote_address)

    def receive(self, buffer_size):
        """Receive segment from the remote host"""
        received = self.socket.recvfrom(buffer_size)
        received_data = received[0]
        sender_address = received[1]
        self.remote_address = sender_address
        segment = restore_segment(received_data)
        return segment

    def get_socket_info(self):
        return self.host_address

    def get_peer_address(self):
        return self.remote_address


class Segment(object):
    def __init__(self, source_port, 
                destination_port, sequence_number, 
                ack_number,
                ack, syn,
                fin, checksum,
                receive_window, payload):
        self.source_port = source_port
        self.destination_port = destination_port
        self._sequence_number = sequence_number
        self._ack_number = ack_number
        self._ack = ack
        self._syn = syn
        self._fin = fin
        self._checksum = checksum
        self._receive_window = receive_window
        self.payload = payload

    @property
    def syn(self):
        return self._syn

    @syn.setter
    def syn(self, syn):
        self._syn = syn

    @property
    def ack(self):
        return self._ack

    @ack.setter
    def ack(self, ack):
        self._ack = ack

    @property
    def ack_number(self):
        return self._ack_number

    @ack_number.setter
    def ack_number(self, ack_number):
        self._ack_number = ack_number

    @property
    def sequence_number(self):
        return self._sequence_number

    @sequence_number.setter
    def sequence_number(self, sequence_number):
        self._sequence_number = sequence_number

    @property
    def receive_window(self):
        return self._receive_window

    @receive_window.setter
    def receive_window(self, receive_window):
        self._receive_window = receive_window


class TCPControlBlock(object):
    def __init__(self, state,
                sequence_number, 
                ack_number, last_byte_received, 
                last_byte_read, last_byte_sent, 
                last_byte_acked, receive_window, 
                maximum_segment_size,
                congestion_window, timer,
                ssthresh):
        self._state = state
        self._sequence_number = sequence_number
        self._ack_number = ack_number
        self._last_byte_received = last_byte_received
        self._last_byte_read = last_byte_read
        self._last_byte_acked = last_byte_acked
        self._last_byte_sent = last_byte_sent
        self._receive_window = receive_window
        self._maximum_segment_size = maximum_segment_size
        self._congestion_window = 1 * maximum_segment_size
        self._timer = timer
        self._ssthresh = ssthresh

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        client_state = ["CLOSED", "SYN_SENT", 
                            "ESTABLISHED", "FIN_WAIT1", 
                            "FIN_WAIT2", "TIME_WAIT", 
                            "CLOSED"] 
        server_state = ["CLOSED", "LISTEN", 
                            "SYN_RCVD", "ESTABLISHED",
                            "CLOSE_WAIT", "LAST_ACK",
                            "TIME_OUT"]
        if (self.state not in client_state) and \
                (self.state not in server_state):
            logging.error("Host state is invalid")
        self._state = state

    @property
    def sequence_number(self):
        return self._sequence_number

    @sequence_number.setter
    def sequence_number(self, sequence_number):
        self._sequence_number = sequence_number

    @property
    def ack_number(self):
        return self._ack_number

    @ack_number.setter
    def ack_number(self, ack_number):
        self._ack_number = ack_number

    @property
    def last_byte_received(self):
        return self._last_byte_received

    @last_byte_received.setter
    def last_byte_received(self, last_byte_received):
        self._last_byte_received = last_byte_received

    @property
    def last_byte_read(self):
        return self._last_byte_read

    @last_byte_read.setter
    def last_byte_read(self, last_byte_read):
        self._last_byte_read = last_byte_read

    @property
    def last_byte_sent(self):
        return self._last_byte_sent

    @last_byte_sent.setter
    def last_byte_sent(self, last_byte_sent):
        self._last_byte_sent = last_byte_sent

    @property
    def last_byte_acked(self):
        return self._last_byte_acked

    @last_byte_acked.setter
    def last_byte_acked(self, last_byte_acked):
        self._last_byte_acked = last_byte_acked

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, timer):
        self._timer = timer

    @property
    def receive_window(self):
        return self._receive_window

    @receive_window.setter
    def receive_window(self, receive_window):
        self._receive_window = receive_window

    @property
    def congestion_window(self):
        return self._congestion_window

    @congestion_window.setter
    def congestion_window(self, congestion_window):
        self._congestion_window = congestion_window
    
    @property
    def maximum_segment_size(self):
        return self._maximum_segment_size

    @maximum_segment_size.setter
    def maximum_segment_size(self, maximum_segment_size):
        self._maximum_segment_size = maximum_segment_size

    @property
    def ssthresh(self):
        return self._ssthresh

    @ssthresh.setter
    def ssthresh(self, ssthresh):
        self._ssthresh = ssthresh

    def create_segment(self):
        segment = Segment(source_port = None,
                destination_port = None,
                sequence_number = self.sequence_number,
                ack_number = self.ack_number,
                ack = 0,
                syn = 0, 
                fin = 0,
                checksum = None,
                receive_window = None,
                payload = None)
        return segment


class Buffer(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.buffer = bytearray()
        self.head = 0
        self.tail = 0
        self.size = 0

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def is_full(self):
        if self.size == self.max_size:
            return True
        else:
            return False

    def write(self, data):
        """Write binary data into proxy buffer and 
           Returns binary data"""
        if self.is_full():
            logging.warning("Buffer is full")
            return None
        if data is None:
            logging.warning("Data is invalid")
            return None
        data = encode_data(data)
        data_size = len(data)
        self.buffer += data
        self.size += data_size
        self.tail = (self.tail + data_size) % (self.max_size)
        logging.info("%d sized data is written", data_size)
        logging.info("%s is written", data)
        return data

    def read(self, data_size):
        if self.is_empty():
            logging.warning("Buffer is empty")
            return None
        logging.info("%d sized data is read", data_size)
        data = self.buffer[self.head:self.head+data_size]
        self.size -= data_size
        self.head += (self.head + data_size) % (self.max_size)
        return bytes(data)


class TCPTimer(object):
    def __init__(self, interval, action):
        self._timeout_interval = interval
        self._action = action
        self.timer = Timer(self.timeout_interval, action)

    def start(self):
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

    def is_running(self):
        self.timer.is_alive()

    @property
    def timeout_interval(self):
        return self._timeout_interval

    @timeout_interval.setter
    def timeout_interval(self, timeout_interval):
        self._timeout_interval = timeout_interval

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action
    

def encode_data(data):
    if isinstance(data, str):
        encoded_data = data.encode('utf-8')
    else:
        encoded_data = data
    return encoded_data


def decode_data(data):
    if isinstance(data, bytes):
        decoded_data = data.decode('utf-8')
    else:
        decoded_data = data
    return decoded_data


def convert_into_byte_stream(segment):
    if isinstance(segment, Segment):
        byte_stream = pickle.dumps(segment)
    return byte_stream


def restore_segment(segment):
    if isinstance(segment, bytes):
        restored_segment = pickle.loads(segment)
    return restored_segment
