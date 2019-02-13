import pytest

from app import db
from tests.posts.factories import PostInBoardFactory
from tests.posts.factories import PostImageFactory


class Describe_Post:
    @pytest.fixture
    def post(self):
        post = PostInBoardFactory.build()

        db.session.add(post)
        db.session.commit()

        return post

    class Describe___repr__:
        def test_Post_객체를_보여준다(self, post):
            assert str(post) == '<{}(id: {}, writer_id: {}, board_id: {}, title: {}, is_published: {})>' \
                .format(post.__class__.__name__, post.id, post.writer_id, post.board_id,
                        post.title, post.is_published)


class Describe_PostImage:
    @pytest.fixture
    def post_image(self):
        post_image = PostImageFactory.build()

        db.session.add(post_image)
        db.session.commit()

        return post_image

    class Describe___repr__:
        def test_PostImage_객체를_보여준다(self, post_image):
            assert str(post_image) == '<{} id: {}, post_id: {}, image_url: {}, caption: {}>' \
                .format(post_image.__class__.__name__, post_image.id, post_image.post_id, post_image.image_url,
                        post_image.caption)
