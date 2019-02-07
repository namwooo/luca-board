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
                'post_id': comment.post.id,
                'comment_parent_id': comment.post.id,
                'body': 'This is test comment.'
            }

            return comment_data

        @pytest.fixture
        def subject(self, client, comment_data):
            response = client.post('/comments', json=comment_data)

            return response

        def test_200을_반환한다(self, logged_in_user, subject):
            assert subject.status_code == 200

        def test_자식_댓글을_생성한다(self, logged_in_user, response_data, comment_data):
            comment_id = response_data['id']

            comment = Comment.query.get_or_404(comment_id)

            assert comment.post_id == comment_data['post_id']
            assert comment.comment_parent_id == comment_data['comment_parent_id']
            assert comment.body == comment_data['body']

        class Context_부모_댓글이_존재하지_않을_경우:
            @pytest.fixture
            def comment_data(self, comment_data):
                # put wrong id
                comment_data['comment_parent_id'] = 999999

                return comment_data

            def test_404를_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 404

        class Context_comment_parent_id값이_없는_경우:
            @pytest.fixture
            def comment_data(selfs, comment_data):
                comment_data.pop('comment_parent_id')

                return comment_data

            def test_200을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 200

            def test_부모_댓글을_생성한다(self, logged_in_user, response_data, comment_data):
                comment_id = response_data['id']

                comment = Comment.query.get_or_404(comment_id)

                assert comment.post_id == comment_data['post_id']
                assert comment.comment_parent_id is None
                assert comment.body == comment_data['body']

            class Context_게시글이_존재하지_않을_경우:
                @pytest.fixture
                def comment(self):
                    comment = CommentFactory.build()

                    return comment

                def test_404를_반환한다(self, logged_in_user, subject):
                    assert subject.status_code == 404

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

            class Context_비로그인_유저인_경우:
                def test_401을_반환한다(self, subject):
                    assert subject.status_code == 401

        class Describe_update:

            @pytest.fixture
            def comment_data(self):
                comment_data = {
                    'body': 'This is test comment.'
                }

                return comment_data

            @pytest.fixture
            def subject(self, client, comment, comment_data):
                response = client.patch(f'/comments/{comment.id}', json=comment_data)

                return response

            def test_200을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 200

            def test_댓글을_수정한다(self, logged_in_user, response_data, comment_data):
                comment_id = response_data['id']

                comment = Comment.query.get_or_404(comment_id)

                assert comment.body == comment_data['body']

            class Context_body값이_없는_경우:
                @pytest.fixture
                def comment_data(self, comment_data):
                    comment_data.pop('body')

                    return comment_data

                def test_422을_반환한다(self, logged_in_user, subject):
                    assert subject.status_code == 422

            class Context_댓글이_존재하지_않는_경우:
                @pytest.fixture
                def comment(self):
                    comment = CommentFactory.build()

                    return comment

                def test_404를_반환한다(self, logged_in_user, subject):
                    assert subject.status_code == 404

            class Context_비로그인_유저인_경우:
                def test_401을_반환한다(self, subject):
                    assert subject.status_code == 401

        class Describe_delete:

            @pytest.fixture
            def subject(self, client, comment, comment_data):
                response = client.delete(f'/comments/{comment.id}')

                return response

            def test_200을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 200

            def test_댓글을_삭제한다(self, logged_in_user, response_data):
                comment = Comment.query.all()

                assert comment == []

            class Context_댓글이_존재하지_않는_경우:
                @pytest.fixture
                def comment(self):
                    comment = CommentFactory.build()

                    return comment

                def test_404를_반환한다(self, logged_in_user, subject):
                    assert subject.response_code == 404

            class Context_비로그인_유저인_경우:
                def test_401을_반환한다(self, subject):
                    assert subject.status_code == 401

