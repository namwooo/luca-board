import pytest
from flask_login import current_user

from app import db
from app.users.models import User
from tests.users.factories import UserFactory


class Describe_UsersView:
    @pytest.fixture
    def response_data(self, subject):
        json_data = subject.get_json()

        return json_data

    class Describe_signup:
        @pytest.fixture
        def user_data(self):
            user_data = {
                'email': 'luca@test.com',
                'password': 'vi8c4i9vho',
                'first_name': 'luca',
                'last_name': 'kim',
            }

            return user_data

        @pytest.fixture
        def subject(self, client, user_data):
            response = client.post('/users/signup', json=user_data)

            return response

        def test_201을_반환한다(self, subject):
            assert subject.status_code == 201

        def test_회원가입을_한다(self, response_data, user_data):
            user_id = response_data['id']

            user = User.query.get_or_404(user_id)
            assert user.email == user_data['email']
            assert user.first_name == user_data['first_name']
            assert user.last_name == user_data['last_name']
            assert user.password == user_data['password']

        class Context_email이_중복된_경우:
            @pytest.fixture
            def user(self):
                user = UserFactory.build(email='luca@test.com')

                db.session.add(user)
                db.session.commit()

                return user

            def test_422을_반환한다(self, user, subject):
                assert subject.status_code == 422

            def test_이메일_중복_메세지를_반환한다(self, user, response_data):
                assert response_data['email'][0] == \
                       'email is duplicated'

        class Context_email을_입력하지_않았을_경우:
            @pytest.fixture
            def user_data(self, user_data):
                user_data.pop('email')

                return user_data

            def test_422을_반환한다(self, subject):
                assert subject.status_code == 422

        class Context_password를_입력하지_않았을_경우:
            @pytest.fixture
            def user_data(self, user_data):
                user_data.pop('password')

                return user_data

            def test_422을_반환한다(self, subject):
                assert subject.status_code == 422

        class Context_first_name을_입력하지_않았을_경우:
            @pytest.fixture
            def user_data(self, user_data):
                user_data.pop('first_name')

                return user_data

            def test_422을_반환한다(self, subject):
                assert subject.status_code == 422

        class Context_last_name을_입력하지_않았을_경우:
            @pytest.fixture
            def user_data(self, user_data):
                user_data.pop('last_name')

                return user_data

            def test_422을_반환한다(self, subject):
                assert subject.status_code == 422

    class Describe_login:
        @pytest.fixture
        def password(self):
            return 'vi8c4i9vho'

        @pytest.fixture
        def user(self, password):
            user = UserFactory.build(password='vi8c4i9vho')

            db.session.add(user)
            db.session.commit()

            return user

        @pytest.fixture
        def login_data(self, user, password):
            login_data = {
                'email': user.email,
                'password': password
            }

            return login_data

        @pytest.fixture
        def subject(self, client, login_data):
            response = client.post('/users/login', json=login_data)

            return response

        def test_200을_반환한다(self, subject):
            assert subject.status_code == 200

        class Context_비밀번호가_틀린_경우:
            @pytest.fixture
            def password(self):
                return '5j5f29re23'

            def test_422을_반환한다(self, subject):
                assert subject.status_code == 422

            def test_비밀번호_불일치_메시지를_반환한다(self, response_data):
                assert response_data['_schema'][0] == 'password does not match'

        class Context_유저가_존재하지_않을_경우:
            @pytest.fixture
            def user(self):
                user = UserFactory.build()
                return user

            def test_422을_반환한다(self, subject):
                assert subject.status_code == 422

            def test_유저_없음_메시지를_반환한다(self, response_data):
                assert response_data['_schema'][0] == 'user does not exist'

    class Describe_logout:
        @pytest.fixture
        def subject(self, client):
            response = client.get('/users/logout')

            return response

        def test_200을_반환한다(self, logged_in_user, subject):
            assert subject.status_code == 200
