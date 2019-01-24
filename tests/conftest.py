import pytest
from app import create_app
from app import db as _db

TEST_DATABASE_URI = 'mysql+pymysql://parker:parker@localhost/test_specup'


@pytest.fixture(scope='session')
def app():
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI,
    }
    app = create_app(settings_override)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    app.testing = True
    client = app.test_client()

    return client


@pytest.fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={}, expire_on_commit=False)
    _session = db.create_scoped_session(options=options)

    db.session = _session

    yield _session

    transaction.rollback()
    connection.close()
    _session.remove()
