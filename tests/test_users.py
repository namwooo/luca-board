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
    assert user.__str__() == 'luca'
    assert user.get_full_name() == 'luca kim'
    assert user.is_admin is False
    assert user.is_authenticated is True
    assert user.is_active is True
    assert user.is_anonymous is False
    assert user.get_id() == '1'


def test_signup_user(client):
    response = client.post('/users/signup/', json={
        'username': 'luca1212',
        'password1': 'qwer1234',
        'password2': 'qwer1234',
        'first_name': 'luca',
        'last_name': 'kim',
        'email': 'luca@test.com'
    })
    data = response.get_json()

    assert response.status == '200 OK'
    assert response.status_code == 200
    assert data['username'] == 'luca1212'
    assert data['first_name'] == 'luca'
    assert data['last_name'] == 'kim'
    assert data['email'] == 'luca@test.com'
