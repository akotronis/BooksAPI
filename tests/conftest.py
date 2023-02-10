import os
import pytest

from db import db
from factory import create_app


# Make `app` variable available in Tests. Must be passed in tests as argument: `app`
@pytest.fixture
def app():
    app = create_app('test')
    return app


# Make `test_client` variable available in Tests. Must be passed in tests as argument: `client`
@pytest.fixture
def client(app):
    return app.test_client()


# Make `app_context` available in Tests. Must be passed in tests .usefixtures as str argument: 'app_ctx'
# Use this like this to avoid writing in every test `with app.app_context(): ...`
@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield