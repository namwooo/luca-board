from app.users.models import User


def test_create_user_model(db):
    new_user = User(username='luca',
                    password='luca123',
                    email='luca@luca.com',
                    first_name='luca',
                    last_name='kim')
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(username='luca').first()
    assert user.username == 'luca'
    assert user.password == 'luca123'
    assert user.email == 'luca@luca.com'
    assert user.first_name == 'luca'
    assert user.last_name == 'kim'
    assert user.__repr__() == '<User luca>'

