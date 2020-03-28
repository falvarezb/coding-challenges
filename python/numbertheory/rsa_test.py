import pytest
from rsa import RSA


def test_rsa_successful():
    rsa = RSA(100)
    msg = "hello world"

    c = rsa.encrypt(msg)
    assert rsa.decrypt(c) == msg


def test_rsa_message_too_long():
    rsa = RSA(10)
    msg = "hello world"

    with pytest.raises(ValueError, match="message too long"):
        rsa.encrypt(msg)
