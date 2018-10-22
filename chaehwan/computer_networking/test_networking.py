import pytest
from queue import Queue

import networking


@pytest.fixture
def buffer():
    return networking.Buffer(max_size=10)

@pytest.fixture
def byte_stream():
    data = "hello"
    byte_stream = networking.encode_data(data)
    return byte_stream

def test_write(buffer, byte_stream):
    buffer.write(byte_stream)
    # Verify that all the data is completely written
    # in the buffer 
    assert buffer.size == 5
    byte_stream = buffer.read(1)
    written = networking.decode_data(byte_stream)
    assert written == 'h'
    # Verify that tail index moves correctly
    # with the given size
    assert buffer.tail == 5
    # Verify that process should be temporarily blocked 
    # if there is no buffer space

def test_read(buffer, byte_stream):
    buffer.write(byte_stream)
    byte_stream = buffer.read(5)
    written = networking.decode_data(byte_stream)
    # Verify that read function reads all the data correctly
    # with the given size
    assert written == "hello"
    # Verify that head index moves correctly
    # with the given size
    assert buffer.head == 5
    # Verify that process should be temporarily blocked 
    # if there is no data in the receiving buffer

def test_peek(buffer, byte_stream):
    buffer.write(byte_stream)
    byte_stream = buffer.peek(5)
    written = networking.decode_data(byte_stream)
    # Verify that read function reads all the data correctly
    # with the given size
    assert written == "hello"
    # Verify that head dosen't move
    # with the given size after the peek call 
    assert buffer.head == 0


@pytest.fixture
def client():
    client = networking.Socket()
    client.set_remote("127.0.0.1", 9000)
    return client

@pytest.fixture
def server():
    server = networking.Socket()
    server.set_remote("127.0.0.1", 9000)
    server.syn_queue = Queue()
    server.accept_queue = Queue(maxsize=5)
    server.tcb.state = "LISTEN"
    return server

@pytest.fixture
def segment(client):
    segment = client.initialize_segment()
    return segment

@pytest.fixture
def syn_segment(client):
    segment = client.initialize_segment()
    segment.syn = 1
    return segment

@pytest.fixture
def syn_ack_segment(server):
    segment = server.initialize_segment()
    segment.syn = 1
    return segment

@pytest.fixture
def ack_segment(client):
    segment = client.initialize_segment()
    segment.ack = 1
    return segment


def test_send(client, server, syn_segment, syn_ack_segment):
    # Verify the state after the client.send(control_bits=["SYN"])
    client.send_segment(control_bits=["SYN"])
    assert client.tcb.state == "SYN_SENT"
    # Verify the seq#, ACK# after calling the
    # client...send(control_bits=["SYN"])
    # client's initial sequence number : 0
    assert client.tcb.sending_sequence_number \
        == client.tcb.sender_isn + 1
    
    # Verify the state after the server.send(
    # control_bits=["SYN", "ACK"])
    payload = server.decapsulate(syn_segment)
    server.send_segment(control_bits=["SYN", "ACK"])
    assert server.tcb.state == "SYN_RCVD"
    # Verify the seq#, ACK# after calling the
    # server.send(control_bits=["SYN", "ACK"])
    # sending sequence number should be 1 
    # because It should be updated after sending SYN/ACK
    # receiving sequence number should be 1 
    # now that server already received the SYN
    assert server.tcb.sending_sequence_number \
        == server.tcb.sender_isn + 1

    # Verify the state after the client.send(
    # control_bits=[ACK"])
    payload = client.decapsulate(syn_ack_segment)
    client.send_segment(control_bits=["ACK"])
    assert client.tcb.state == "ESTABLISHED"
    # Verify the seq#, ACK# after calling the
    # client.send(control_bits=[ACK"])
    # because It should be updated after sending ACK
    # receiving sequence number should be initial sequence number plus 2
    assert client.tcb.sending_sequence_number \
        == client.tcb.sender_isn + 2


def test_decapsulate(server, client, 
                    syn_segment, 
                    syn_ack_segment, 
                    ack_segment):
    # Verify the state after the server...decapsulate(syn_segment) 
    # in the received function, It should be SYN RCVD
    assert server.tcb.state == "LISTEN"
    payload = server.decapsulate(syn_segment)
    assert server.tcb.state == "SYN_RCVD"
    # Verify the seq#, ACK# after the server...decapsulate(syn_segment) 
    # server's initial sequence number : 0
    # client's initial sequence number : 0
    # receiving sequence number should be 1 
    assert server.tcb.receiving_sequence_number \
        == syn_segment.sequence_number + 1

    # Verify the state after the client...decapsulate(syn_ack_segment) 
    client.send_segment(control_bits=["SYN"])
    assert client.tcb.state == "SYN_SENT"
    payload = client.decapsulate(syn_ack_segment)
    assert client.tcb.state == "SYN_SENT"
    # Verify the seq#, ACK# after the client...decapsulate(
    # syn_ack_segment)
    # client's receiving sequence number : 0 
    # because client didn't receive any packet
    # receiving sequence number should be 1 
    assert client.tcb.receiving_sequence_number \
        == syn_ack_segment.sequence_number + 1

    # Verify the state after the server...decapsulate(
    # ack_segment) 
    # in the received function, It should be "ESTABLISHED"
    assert server.tcb.state == "SYN_RCVD"
    payload = server.decapsulate(ack_segment)
    assert server.tcb.state == "ESTABLISHED"
    # Verify the seq#, ACK# after the server...decapsulate(
    # syn_segment) 
    # server's initial sequence number : 0
    # client's initial sequence number : 0
    # receiving sequence number should be 1 
    assert server.tcb.receiving_sequence_number \
        == syn_segment.sequence_number + 1


def test_listen(server, syn_segment, ack_segment):
    server.syn_queue = Queue()
    server.accept_queue = Queue(maxsize=1)
    server.tcb.state = "LISTEN"
    payload = server.decapsulate(syn_segment)
    # Verify that syn queue is not empty after 
    # server receive the syn segment
    assert server.tcb.state == "SYN_RCVD"
    assert server.syn_queue.empty() == False
    # Verify that the status is same
    # after server sent the syn/ack segment
    server.send_segment(control_bits=["SYN", "ACK"])
    assert server.tcb.state == "SYN_RCVD"
    assert server.syn_queue.empty() == False
    # Verify that the syn queue is empty and 
    # the accept queue is not empty 
    # after server receive the ack segment
    payload = server.decapsulate(ack_segment)
    assert server.tcb.state == "ESTABLISHED"
    assert server.syn_queue.empty() == True
    assert server.accept_queue.empty() == False
    # Verify that if the accept queue is full
    # server just drops the pakcet 
    # if the syn packet comes in, It can not be 
    # put into the syn queue
    payload = server.decapsulate(syn_segment)
    server.send_segment(control_bits=["SYN", "ACK"])
    payload = server.decapsulate(ack_segment)
    # if the syn packet comes in, It can not be 
    # put into the syn queue
    assert server.syn_queue.empty() == True
    payload = server.decapsulate(syn_segment)
    assert server.syn_queue.empty() == True


def test_accept(server):
    pass

