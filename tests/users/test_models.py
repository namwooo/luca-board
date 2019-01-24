import pytest

from app import db
from app.users.models import User


class Describe_User:
    @pytest.fixture
    def user_params(self):
        return dict(username='luca',
                    email='luca@luca.com',
                    first_name='luca',
                    last_name='kim')

    @pytest.fixture
    def password(self):
        return 'fake_password'

    class Describe_get_full_name:
        @pytest.fixture
        def user(self, user_params, password):
            new_user = User(**user_params)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return new_user

        @pytest.fixture
        def subject(self, user):
            return user.get_full_name()

        def test_full_name_을_가져온다(self, subject):
            assert 'luca kim' == subject
