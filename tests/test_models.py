from app import __version__
from app.models import User


def test_version():
    assert __version__ == '0.1.0'


def test_user_model(db):
    new_user = User(username='test',
                    password='test123',
                    email='test@test.com',
                    first_name='luca',
                    last_name='kim')
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(username='test').first()
    assert user.username == 'test'
    assert user.password == 'test123'
    assert user.email == 'test@test.com'
    assert user.first_name == 'luca'
    assert user.last_name == 'kim'


def test_user_model2(db):
    new_user = User(username='test',
                    password='test123',
                    email='test@test.com',
                    first_name='luca',
                    last_name='kim')
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(username='test').first()
    assert user.username == 'test'
    assert user.password == 'test123'
    assert user.email == 'test@test.com'
    assert user.first_name == 'luca'
    assert user.last_name == 'kim'
