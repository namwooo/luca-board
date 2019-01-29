import pytest

from app import db
from tests.users.factories import UserFactory


class Describe_UsersView:
    class Describe_signup:
        @pytest.fixture
        def user_param(self):
            user_param = {
                'username': 'luca',
                'password1': 'vi8c4i9vho',
                'password2': 'vi8c4i9vho',
                'first_name': 'luca',
                'last_name': 'kim',
                'email': 'luca@test.com'
            }

            return user_param

        @pytest.fixture
        def subject(self, client, user_param):
            response = client.post('/users/signup/', json=user_param)

            return response

        def test_회원가입을_한다(self, subject):
            data = subject.get_json()

            assert 200 == subject.status_code
            assert 'luca' == data['username']
            assert 'luca' == data['first_name']
            assert 'kim' == data['last_name']
            assert 'luca@test.com' == data['email']

        class Context_password1과_password2가_불일치_할_때:
            @pytest.fixture
            def user_param(self, user_param):
                user_param['password2'] = '5j5f29re23'  # wrong password

                return user_param

            def test_422을_반환한다(self, subject):
                data = subject.get_json()

                assert 422 == subject.status_code
                assert 'password1 and password2 must match' == data['_schema'][0]

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

        @pytest.fixture
        def subject(self, client, user, password):
            response = client.post('/users/login/', json={
                'username': user.username,
                'password': password
            })
            return response

        def test_로그인_한다(self, subject):
            assert 200 == subject.status_code

        class Context_비밀번호가_틀린_경우:
            @pytest.fixture
            def password(self):
                return '5j5f29re23'

            def test_422을_반환한다(self, subject):
                data = subject.get_json()
                assert 422 == subject.status_code
                assert 'password does not match' == data['_schema'][0]

        class Context_유저가_존재하지_않을_경우:
            @pytest.fixture
            def user(self):
                user = UserFactory.build()
                return user

            def test_422을_반환한다(self, subject):
                data = subject.get_json()
                assert 422 == subject.status_code
                assert 'user does not exist' == data['_schema'][0]

    class Describe_logout:
        @pytest.fixture
        def user(self):
            user = UserFactory.build()

            db.session.add(user)
            db.session.commit()

            return user

        @pytest.fixture
        def password(self):
            return 'vi8c4i9vho'

        @pytest.fixture
        def login_user(self, client, user, password):
            response = client.post('/users/login/', json={
                'username': user.username,
                'password': password
            })

            return user

        def test_로그아웃_한다(self, client, login_user):
            response = client.get('/users/logout/')
            data = response.get_json()

            assert 200 == response.status_code
            assert 'logout success' == data['message']
