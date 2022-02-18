import os
import tempfile

import pytest
from src import create_app
from src.models.models import db



@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()

    print(db_path)

    app = create_app()
    app.config.update({
        "TESTING":True,
        # 'SQLALCHEMY_DATABASE_URI':'sqlite:///'+db_path
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()