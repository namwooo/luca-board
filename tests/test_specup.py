from specup import __version__
import os
import tempfile
import pytest
from specup import app


def test_version():
    assert __version__ == '0.1.0'


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(client):
    rv = client.get('/')
    assert b'Hello, World!' in rv.data
