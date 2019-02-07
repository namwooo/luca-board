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

    @pytest.fixture
    def subject(self, comment):
        comment.save()

        return comment

    def test_path가_저장된다(self, subject):
        comment = Comment.query.get(subject.id)

        assert comment.path == '000001'
