import factory

from app import db
from app.comments.models import Comment
from tests.posts.factories import PostInBoardFactory
from tests.users.factories import UserFactory


class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    # Number of path digit
    _N = 6

    class Meta:
        model = Comment
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = None

    writer = factory.SubFactory(UserFactory)
    body = factory.Faker('paragraph')
    path = factory.PostGenerationMethodCall('set_path')


class CommentInPostFactory(factory.alchemy.SQLAlchemyModelFactory):
    # Number of path digit
    _N = 6

    class Meta:
        model = Comment
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = None

    writer = factory.SubFactory(UserFactory)
    body = factory.Faker('paragraph')
    path = factory.PostGenerationMethodCall('set_path')
    post = factory.SubFactory(PostInBoardFactory)
