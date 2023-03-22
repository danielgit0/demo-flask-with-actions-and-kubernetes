import pytest
from flaskr import create_app


def test_request_example(client):
    response = client.get('/')
    assert b'{"email":"alice@outlook.com","name":"alice"}' in response.data
