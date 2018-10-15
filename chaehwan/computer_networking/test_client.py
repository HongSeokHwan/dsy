import pytest

from client import Client


@pytest.fixture
def client():
    client = Client()
    client.create_socket(socket_name="client socket")
    client.bind('', 8000)
    client.socket.remote_address = ("127.0.0.1", 9000)
    return client

@pytest.fixture
def segment(client):
    segment = client.tcp_control_block.create_segment()
    return segment

@pytest.fixture
def syn_ack_segment(client):
    segment = client.tcp_control_block.create_segment()
    segment.syn = 1
    segment.ack = 1
    # server's initial sequence number
    segment.sequence_number = 500
    return segment


def test_send_syn(client, segment):
    # Verify that the state after the send_syn call is SYN_SENT
    client.send_syn()
    assert client.tcp_control_block.state == "SYN_SENT"
    # Verify that sending data is still in the buffer to retransmit
    # after the send_syn function call
    client.socket.sending_buffer.clear()
    assert len(client.socket.sending_buffer) == 0
    client.send_syn()
    assert len(client.socket.sending_buffer) == 1
    # Verify that client keeps proper Seq# and ACK# number
    # after the send_syn function call
    # Client's initial seq# : 100
    # Client's ACK# yet : 0
    # after the send_syn call, seq# should be changed
    # by reflecting the current syn segment sent 
    assert client.tcp_control_block.sequence_number == 101
    assert client.tcp_control_block.ack_number == 0
    # Verify that timer started and is alive
    # after the send_syn function call
    # assert client.tcp_control_block.timer.is_alive() == True


def test_receive_syn_ack(client, syn_ack_segment):
    client.send_syn()
    client.receive_syn_ack(syn_ack_segment)
    # Verify that client keeps proper Seq# and ACK# number
    # after the receive_syn_ack function call
    assert syn_ack_segment.sequence_number == 500
    assert client.tcp_control_block.ack_number == 501
    # Verify that the front element of the sending buffer has removed
    # after the receive_syn_ack function call(ACK)
    assert len(client.socket.sending_buffer) == 0
    client.send_syn()
    assert len(client.socket.sending_buffer) == 1
    client.receive_syn_ack(syn_ack_segment)
    assert len(client.socket.sending_buffer) == 0

def test_send_ack(client, segment, syn_ack_segment):
    client.send_syn()
    client.receive_syn_ack(syn_ack_segment)
    assert len(client.socket.sending_buffer) == 0
    client.send_ack()
    # Verify that the state after the send_ack call is ESTABLISHED
    assert client.tcp_control_block.state == "ESTABLISHED"
    # Verify that sending data is still in the buffer to retransmit
    # after the send_syn function call
    assert len(client.socket.sending_buffer) == 1
    # Verify that client keeps proper Seq# and ACK# number
    # after the send_ack function call
    assert client.tcp_control_block.sequence_number == 102
    assert client.tcp_control_block.ack_number == 501

def test_connect(client):
    pass

def test_send(client):
    pass