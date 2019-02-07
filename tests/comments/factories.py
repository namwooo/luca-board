import factory

from app import db
from app.comments.models import Comment
from tests.posts.factories import PostFactory
from tests.users.factories import UserFactory


class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Comment
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n + 1)
    writer = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    body = factory.Faker('paragraph')
    path = factory.PostGenerationMethodCall('get_path')
