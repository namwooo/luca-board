import random
import string
import pytest
from app import create_app
from app import db as _db
from tests.users.factories import UserFactory

TEST_DATABASE_URI = 'mysql+pymysql://root:Demian!89@localhost/test_specup'


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

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()


@pytest.fixture
def password(size=10):
    """Return combination of random characters and digits"""
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))


@pytest.fixture
def logged_in_user(client, password):
    user = UserFactory.build(password=password)

    _db.session.add(user)
    _db.session.commit()

    # Access load attribute after commit
    login_data = {
        'email': user.email,
        'password': password
    }

    response = client.post('/users/login', json=login_data)
    assert response.status_code == 200

    return user


@pytest.fixture
def not_logged_in_user(client, password):
    user = UserFactory.build()

    # It has to be executed before commit
    user.set_password(password)

    _db.session.add(user)
    _db.session.commit()

    return user
