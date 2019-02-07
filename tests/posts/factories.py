import factory

from app import db
from app.posts.models import Post
from tests.boards.factories import BoardFactory
from tests.users.factories import UserFactory


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = None

    id = factory.Sequence(lambda n: n + 1)
    writer = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    title = factory.Faker('sentence')
    body = factory.Faker('paragraph')
    is_published = True

