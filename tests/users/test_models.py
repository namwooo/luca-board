import pytest

from tests.users.factories import UserFactory


class Describe_User:
    @pytest.fixture
    def user(self):
        user = UserFactory.build()

        return user

    class Describe_get_full_name:
        def test_full_name_을_가져온다(self, user):
            full_name = f'{user.first_name} {user.last_name}'
            assert user.get_full_name() == full_name
