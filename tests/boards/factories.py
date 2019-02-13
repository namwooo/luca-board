import factory

from app import db
from app.boards.models import Board
from ..users.factories import UserFactory


class BoardFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Board
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = None

    title = factory.Faker('word')
    writer = factory.SubFactory(UserFactory)
