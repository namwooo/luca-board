import pytest

from tests.comments.factories import CommentFactory
from tests.users.factories import UserFactory


class Describe_Comment:
    @pytest.fixture
    def comment(self):
        comment = CommentFactory.create()
        return comment

    @pytest.fixture
    def user(self):
        user = UserFactory.create()
        return user

    class Describe___repr__:
        def test_Comment_객체를_나타낸다(self, comment):
            assert str(comment.__repr__()) == '<{}(id: {}, writer_id: {}, post_id: {}, path: {})>' \
                .format(comment.__class__.__name__, comment.id, comment.writer_id,
                        comment.post_id, comment.path)

    class Describe_is_writer:
        class Context_작성자가_다른_경우:
            def test_False를_반환한다(self, comment, user):
                assert comment.is_writer(user) == False

        class Context_작성자가_같은_경우:
            def test_True를_반환한다(self, comment):
                assert comment.is_writer(comment.writer) == True

    class Describe_set_path:
        @pytest.fixture
        def comment(self):
            comment = CommentFactory.build()
            return comment

        def test_path값을_할당한다(self, comment):
            path = comment.set_path()
            assert comment.path == '{:0{}d}'.format(comment.id, comment._N)
