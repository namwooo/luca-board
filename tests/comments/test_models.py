import pytest

from tests.comments.factories import CommentFactory


class Describe_Comment:
    @pytest.fixture
    def comment(self):
        comment = CommentFactory.create()
        return comment

    class Describe___repr__:
        def test_Comment_객체를_나타낸다(self, comment):
            assert str(comment.__repr__()) == '<{}(id: {}, writer_id: {}, post_id: {}, path: {})>' \
                .format(comment.__class__.__name__, comment.id, comment.writer_id,
                        comment.post_id, comment.path)
