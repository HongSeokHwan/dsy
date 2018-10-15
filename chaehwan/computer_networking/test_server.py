import pytest
import queue

from server import Server


@pytest.fixture
def server():
    server = Server()
    server.create_socket(socket_name="server socket")
    server.bind('', 10000)
    server.socket.remote_address = ("127.0.0.1", 9000)
    return server

@pytest.fixture
def segment(server):
    segment = server.tcp_control_block.create_segment()
    return segment

@pytest.fixture
def syn_segment(server):
    segment = server.tcp_control_block.create_segment()
    segment.syn = 1
    # client's initial sequence number
    segment.sequence_number = 100
    return segment

@pytest.fixture
def ack_segment(server):
    segment = server.tcp_control_block.create_segment()
    segment.ack = 1
    # client's sequence number after client received syn/ack
    segment.sequence_number = 101
    return segment

def test_receive_syn(server, syn_segment):
    # Verify that client keeps proper Seq# and ACK# number
    # after the send_syn function call
    server.syn_queue = queue.Queue()
    server.receive_syn(syn_segment)
    assert server.tcp_control_block.sequence_number == 0
    assert server.tcp_control_block.ack_number == 101

def test_send_syn_ack(server, syn_segment):
    server.syn_queue = queue.Queue()
    server.receive_syn(syn_segment)
    # Verify that sending data is still in the buffer to retransmit
    # after the send_syn_ack function call
    assert len(server.socket.sending_buffer) == 0
    server.send_syn_ack()
    assert len(server.socket.sending_buffer) == 1
    # Verify that client keeps proper Seq# and ACK# number
    # after the send_syn_ack function call
    # after the send_syn_ack call, seq# should be changed
    # by reflecting the current syn segment sent 
    assert server.tcp_control_block.sequence_number == 501
    assert server.tcp_control_block.ack_number == 101

def test_receive_ack(server, syn_segment, ack_segment):
    server.syn_queue = queue.Queue()
    server.accept_queue = queue.Queue(maxsize=5)
    server.receive_syn(syn_segment)
    server.send_syn_ack()
    assert len(server.socket.sending_buffer) == 1
    # Verify that client keeps proper Seq# and ACK# number
    # after the send_syn function call
    server.receive_ack(ack_segment)
    assert server.tcp_control_block.ack_number == 102
    # Verify that the front element of the sending buffer has removed
    # after the receive_ack function call
    assert len(server.socket.sending_buffer) == 0

def test_listen(server):
    pass

def test_accept(server):
    pass