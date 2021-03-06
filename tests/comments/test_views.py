import pytest

from app import db
from app.comments.models import Comment
from tests.comments.factories import CommentFactory, CommentInPostFactory


class Describe_CommentView:
    @pytest.fixture
    def response_data(self, subject):
        json_data = subject.get_json()

        return json_data

    @pytest.fixture
    def comment(self):
        comment = CommentInPostFactory.build()

        db.session.add(comment)
        db.session.commit()

        return comment

    class Describe_post:
        @pytest.fixture
        def comment_data(self, comment):
            comment_data = {
                'post_id': comment.post.id,
                'comment_parent_id': comment.id,
                'body': 'This is test comment.'
            }

            return comment_data

        @pytest.fixture
        def subject(self, client, comment_data):
            response = client.post('/comments', json=comment_data)
            return response

        def test_201을_반환한다(self, logged_in_user, subject):
            assert subject.status_code == 201

        def test_자식_댓글을_생성한다(self, logged_in_user, subject, comment_data):
            comment = Comment.query.filter(Comment.body == comment_data['body']).all()

            assert len(comment) != 0

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

            def test_201을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 201

            def test_부모_댓글을_생성한다(self, logged_in_user, subject, comment_data):
                comment = Comment.query.filter(Comment.body == comment_data['body']).first()

                assert comment.comment_parent_id is None

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
        def comment(self, logged_in_user):
            comment = CommentFactory.build(writer=logged_in_user)

            db.session.add(comment)
            db.session.commit()

            return comment

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

        class Context_작성자가_아닌_경우:
            @pytest.fixture
            def comment(self):
                comment = CommentFactory.build()

                db.session.add(comment)
                db.session.commit()

                return comment

            def test_403을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 403

            def test_WriterOnly_메세지를_반환한다(self, logged_in_user, response_data):
                assert response_data['writer'] == \
                       'Writer Only: permission denied'

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
            @pytest.fixture
            def comment(self):
                comment = CommentFactory.build()

                db.session.add(comment)
                db.session.commit()

                return comment

            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

    class Describe_delete:
        @pytest.fixture
        def comment(self, logged_in_user):
            comment = CommentFactory.build(writer=logged_in_user)

            db.session.add(comment)
            db.session.commit()

            return comment

        @pytest.fixture
        def subject(self, client, comment, comment_data):
            response = client.delete(f'/comments/{comment.id}')

            return response

        def test_200을_반환한다(self, logged_in_user, subject):
            assert subject.status_code == 200

        def test_댓글을_삭제한다(self, logged_in_user, response_data):
            comment = Comment.query.all()

            assert comment == []

        class Context_작성자가_아닌_경우:
            @pytest.fixture
            def comment(self):
                comment = CommentFactory.build()

                db.session.add(comment)
                db.session.commit()

                return comment

            def test_403을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 403

            def test_WriterOnly_메세지를_반환한다(self, logged_in_user, response_data):
                assert response_data['writer'] == \
                       'Writer Only: permission denied'

        class Context_댓글이_존재하지_않는_경우:
            @pytest.fixture
            def comment(self):
                comment = CommentFactory.build()

                return comment

            def test_404를_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 404

        class Context_비로그인_유저인_경우:
            @pytest.fixture
            def comment(self):
                comment = CommentFactory.build()

                db.session.add(comment)
                db.session.commit()

                return comment

            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

    class Describe_comment_list:

        @pytest.fixture
        def parent_comment(self):
            comment = CommentFactory.build()

            comment.save()

            return comment

        @pytest.fixture
        def children_comments(self, parent_comment):
            c1 = CommentFactory.build(post=parent_comment.post,
                                      comment_parent_id=parent_comment.id)
            c2 = CommentFactory.build(post=parent_comment.post,
                                      comment_parent_id=parent_comment.id)
            c3 = CommentFactory.build(post=parent_comment.post,
                                      comment_parent_id=parent_comment.id)

            for c in [c1, c2, c3]:
                c.save()

            return c1

        @pytest.fixture
        def subject(self, client, children_comments):
            url = f'/posts/{children_comments.post_id}/comments'
            response = client.get(url)

            return response

        def test_200을_반환한다(self, subject):
            assert subject.status_code == 200

        def test_댓글_목록을_가져온다(self, response_data):
            assert len(response_data) == 4
