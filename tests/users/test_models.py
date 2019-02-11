import pytest

from app import db
from tests.users.factories import UserFactory


class Describe_User:
    @pytest.fixture
    def user(self):
        user = UserFactory.build()

        db.session.add(user)
        db.session.commit()

        return user

    class Describe___repr__:
        def test_User_객체를_보여준다(self, user):
            assert str(user) == '<{}(id: {}, name: {}, email: {}, is_admin: {}, is_active: {})>'\
                .format(user.__class__.__name__, user.id,
                        user.full_name, user.email,
                        user.is_admin, user.is_active)

    class Describe_full_name:
        def test_full_name_을_가져온다(self, user):
            full_name = f'{user.first_name} {user.last_name}'
            assert user.full_name == full_name
