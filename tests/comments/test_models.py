import pytest

from app import db
from app.comments.models import Comment
from tests.comments.factories import CommentFactory


class Describe_Comment:
    @pytest.fixture
    def comment(self):
        comment = CommentFactory.build()

        db.session.add(comment)
        db.session.commit()

        return comment

    class Describe_basis:
        def test_댓글_모델을_생성한다(self, comment):
            comment = Comment.query.all()

            assert len(comment) == 1
