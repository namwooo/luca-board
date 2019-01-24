import factory
from factory.alchemy import SQLAlchemyModelFactory

from app import db
from app.boards.models import Board
from tests.users.factories import UserFactory


class BoardFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Board
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    title = factory.Sequence(lambda n: 'Board title %d' % n)
    writer = factory.SubFactory(UserFactory)
