import pytest

from app import db
from tests.users.factories import UserFactory


class Describe_UsersView:
    class Describe_signup:
        def test_회원가입을_한다(self, client):
            response = client.post('/users/signup/', json={
                'username': 'luca',
                'password1': 'vi8c4i9vho',
                'password2': 'vi8c4i9vho',
                'first_name': 'luca',
                'last_name': 'kim',
                'email': 'luca@test.com'
            })
            data = response.get_json()

            assert 201 == response.status_code
            assert 'luca' == data['username']
            assert 'luca' == data['first_name']
            assert 'kim' == data['last_name']
            assert 'luca@test.com' == data['email']

        class Context_비밀번호1과_비밀번호2가_불일치_할_때:
            def test_400을_반환한다(self, client):
                response = client.post('/users/signup/', json={
                    'username': 'luca',
                    'password1': 'vi8c4i9vho',
                    'password2': '5j5f29re23',
                    'first_name': 'luca',
                    'last_name': 'kim',
                    'email': 'luca@test.com'
                })
                data = response.get_json()

                assert 400 == response.status_code
                assert 'password1 and password2 must match' == data['message']

    class Describe_login:
        @pytest.fixture
        def user(self):
            user = UserFactory.build()

            db.session.add(user)
            db.session.commit()

            return user

        @pytest.fixture
        def password(self):
            return 'vi8c4i9vho'

        def test_로그인_한다(self, client, user, password):
            response = client.post('/users/login/', json={
                'username': user.username,
                'password': password
            })
            assert 200 == response.status_code

        class Context_비밀번호가_틀린_경우:
            def test_400을_반환한다(self, client, user):
                response = client.post('/users/login/', json={
                    'username': user.username,
                    'password': '5j5f29re23'
                })
                data = response.get_json()
                assert 400 == response.status_code
                assert 'password does not match' == data['message']

        class Context_유저가_존재하지_않을_경우:
            def test_400을_반환한다(self, client, password):
                response = client.post('/users/login/', json={
                    'username': 'NotExistUser',
                    'password': password
                })
                data = response.get_json()
                assert 400 == response.status_code
                assert 'User does not exist' == data['message']
