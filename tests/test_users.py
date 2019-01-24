import pytest

from app.users.models import User


def test_user_model(db):
    new_user = User(username='luca',
                    email='luca@luca.com',
                    first_name='luca',
                    last_name='kim')
    new_user.set_password('qwer1234')
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(username='luca').first()
    assert user.username == 'luca'
    assert user.check_password('qwer1234') is True
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


def test_signup_user(client):
    response = client.post('/users/signup/', json={
        'username': 'luca',
        'password1': 'qwer1234',
        'password2': 'qwer1234',
        'first_name': 'luca',
        'last_name': 'kim',
        'email': 'luca@test.com'
    })
    data = response.get_json()

    assert response.status == '201 CREATED'
    assert response.status_code == 201
    assert data['username'] == 'luca'
    assert data['first_name'] == 'luca'
    assert data['last_name'] == 'kim'
    assert data['email'] == 'luca@test.com'


def login(client, username, password):
    return client.post('/users/login/', json={
        'username': username,
        'password': password
    })


def logout(client):
    return client.get('/users/logout/')


def test_login_logout(client, db):
    new_user = User(username='luca',
                    email='luca@luca.com',
                    first_name='luca',
                    last_name='kim')
    new_user.set_password('qwer1234')
    db.session.add(new_user)
    db.session.commit()

    response = login(client, 'luca', 'qwer1234')
    assert response.status == '200 OK'
    assert response.status_code == 200

    response = logout(client)
    assert response.status == '200 OK'
    assert response.status_code == 200

