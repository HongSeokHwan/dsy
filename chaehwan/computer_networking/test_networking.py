import pytest
import unittest

import networking


@pytest.fixture
def buffer():
    return networking.Buffer(max_size=10)

def test_write(buffer):
    # Verify that the write method works well
    buffer.write("hello")
    assert buffer.size == 5
    # Verify that the overflow happens in the correct situation
    buffer.write(" world~!")
    assert buffer.size == 5    

def test_read(buffer):
    # Verify that the read method works well
    buffer.write("hello")
    assert "hello" == buffer.read(5)
    # Verify that the underflow happens in the proper situation
    buffer.read(5)
    assert buffer.size == 0