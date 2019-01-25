import pytest
from tests.users.factories import UserFactory


class Describe_User:
    @pytest.fixture
    def user(self):
        user = UserFactory.create()

        return user

    @pytest.fixture
    def password(self):
        return 'vi8c4i9vho'

    class Describe_set_check_password:
        def test_해쉬된_비밀번호를_설정_및_체크한다(self, user, password):
            user.set_password(password)
            assert 'pbkdf2:sha256' in user.password
            assert True is user.check_password(password)

    class Describe_get_full_name:
        def test_full_name_을_가져온다(self, user):
            full_name = f'{user.first_name} {user.last_name}'
            assert full_name == user.get_full_name()
