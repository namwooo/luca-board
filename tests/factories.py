import factory

from app.posts.models import Board, Post
from app.users.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = 'luca'
    first_name = 'luca'
    last_name = 'kim'
    email = 'luca@test.com'


class BoardFactory(factory.Factory):
    class Meta:
        model = Board

    title = 'Recruit'


class PostFactory(factory.Factory):
    class Meta:
        model = Post

    title = 'recruit bluewhale'
    body = 'wanted ios developer'
