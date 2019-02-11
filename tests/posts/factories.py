import factory

from app import db
from app.posts.models import Post, PostImage
from tests.boards.factories import BoardFactory
from tests.users.factories import UserFactory


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    writer = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    title = factory.Faker('sentence')
    body = factory.Faker('paragraph')
    is_published = True


class PostImageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = PostImage
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    image_url = factory.Faker('url')
    caption = factory.Faker('sentence')
    post = factory.SubFactory(PostFactory)

