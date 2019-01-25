import factory

from app import db
from app.boards.models import Board
from tests.users.factories import UserFactory


class BoardFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Board
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = None

    title = factory.Faker('word')
    writer = factory.SubFactory(UserFactory)
