import pytest

from app import db
from app.comments.models import Comment
from tests.comments.factories import CommentFactory


class Describe_CommentsView:
    @pytest.fixture
    def response_data(self, subject):
        json_data = subject.get_json()

        return json_data

    @pytest.fixture
    def comment(self):
        comment = CommentFactory.build()

        db.session.add(comment)
        db.session.commit()

        return comment

    class Describe_create:

        @pytest.fixture
        def comment_data(self, comment):
            comment_data = {
                'post_id': comment.post_id,
                'comment_parent_id': comment.id,
                'body': 'This is test comment.'
            }

            return comment_data

        @pytest.fixture
        def subject(self, client, comment_data):
            response = client.post('/comments', json=comment_data)

            return response

        def test_200을_반환한다(self, subject):
            assert subject.status_code == 200

        def test_댓글이_생성된다(self, response_data, comment_data):
            comment_id = response_data['id']

            comment = Comment.query.get_or_404(comment_id)

            assert comment.post_id == comment_data['post_id']
            assert comment.comment_id == comment_data['comment_id']
            assert comment.body == comment_data['body']

        class Context_부모_댓글이_존재하지_않을_경우:
            @pytest.fixture
            def comment_data(self, comment_data):
                # put wrong id
                comment_data['comment_parent_id'] = 10000

                return comment_data

            def test_404를_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 404

        class Context_게시글이_존재하지_않을_경우:
            @pytest.fixture
            def comment(self):
                comment = CommentFactory.build()

                return comment

            def test_404를_반환한다(self, logged_in_user, subject):
                assert subject.status_cdde == 404

        class Context_비로그인_유저인_경우:
            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

        class Context_body값이_없는_경우:
            @pytest.fixture
            def comment_data(self, comment_data):
                comment_data.pop('body')

                return comment_data

            def test_422을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 422

        class Context_post_id가_없는_경우:
            @pytest.fixture
            def comment_data(self, comment_data):
                comment_data.pop('post_id')

                return comment_data

            def test_422을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 422

    # class Describe_update:
    #
    # class Describe_delete:
