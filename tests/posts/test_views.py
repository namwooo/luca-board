import pytest

from app import db
from app.posts.models import Post
from tests.boards.factories import BoardFactory
from tests.comments.factories import CommentFactory
from tests.posts.factories import PostFactory, PostInBoardFactory


class Describe_PostView:
    @pytest.fixture
    def response_data(self, subject):
        json_data = subject.get_json()

        return json_data

    class Describe_list:
        @pytest.fixture
        def posts(self):
            posts = PostFactory.build_batch(16)
            return posts

        @pytest.fixture
        def board(self, posts):
            board = BoardFactory.build()
            board.posts = posts

            db.session.add(board)
            db.session.commit()

            return board

        @pytest.fixture
        def param(self):
            return '?p=1'  # page 1

        @pytest.fixture
        def subject(self, client, board, param):
            url = f'/boards/{board.id}/posts{param}'
            response = client.get(url)

            return response

        def test_200을_반환한다(self, subject):
            assert subject.status_code == 200

        def test_게시글_목록을_가져온다(self, response_data):
            assert len(response_data['items']) == 15
            assert response_data['total'] == 16

        class Context_게시판이_존재하지_않을_경우:
            @pytest.fixture
            def board(self):
                board = BoardFactory.build()
                board.post = PostFactory.build_batch(15)

                return board

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

    class Describe_post:

        @pytest.fixture
        def board(self):
            board = BoardFactory.build()

            db.session.add(board)
            db.session.commit()

            return board

        @pytest.fixture
        def post_data(self, board):
            post_data = {
                'title': 'Blue Whale vs Blue Dragon',
                'body': 'Blue Whale win',
                'is_published': True,
                'board_id': board.id
            }

            return post_data

        @pytest.fixture
        def subject(self, client, post_data):
            response = client.post('/posts', json=post_data)

            return response

        def test_201을_반환한다(self, logged_in_user, subject):
            assert subject.status_code == 201

        def test_게시글이_생성된다(self, logged_in_user, post_data):
            post = Post.query.filter(Post.title == post_data['title'])

            assert post is not None

        class Context_게시판이_존재하지_않는_경우:
            @pytest.fixture
            def board(self):
                board = BoardFactory.build(id=99)

                return board

            def test_404를_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 404

        class Context_비로그인_유저인_경우:
            def test_401을_반환한다(self, not_logged_in_user, subject):
                assert subject.status_code == 401

        class Context_title값이_없는_경우:
            @pytest.fixture
            def post_data(self, post_data):
                post_data.pop('title')

                return post_data

            def test_422을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 422

        class Context_body값이_없는_경우:
            @pytest.fixture
            def post_data(self, post_data):
                post_data.pop('body')

                return post_data

            def test_422을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 422

    class Describe_get:
        @pytest.fixture
        def post(self):
            post = PostInBoardFactory.build()

            db.session.add(post)
            db.session.commit()

            return post

        @pytest.fixture
        def subject(self, client, post):
            url = f'/posts/{post.id}'
            response = client.get(url)
            return response

        def test_200을_반환한다(self, subject):
            assert subject.status_code == 200

        def test_조회수가_1_증가한다(self, response_data):
            assert response_data['view_count'] == 1

        class Context_게시글이_없는_경우:
            @pytest.fixture
            def post(self):
                post = PostInBoardFactory.build()

                return post

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

    class Describe_patch:
        @pytest.fixture
        def post(self):
            post = PostInBoardFactory.build()

            db.session.add(post)
            db.session.commit()

            return post

        @pytest.fixture
        def patch_data(self):
            data = {
                'title': 'Recruit',
                'body': 'Wanted BACKEND developer',
                'is_published': True
            }

            return data

        @pytest.fixture
        def subject(self, client, post, patch_data):
            response = client.patch(f'/posts/{post.id}', json=patch_data)
            return response

        def test_200을_반환한다(self, logged_in_user, subject):
            assert subject.status_code == 200

        def test_게시글을_수정한다(self, logged_in_user, subject, patch_data):
            post = Post.query.filter(Post.title == patch_data['title']).first()

            assert patch_data['title'] == post.title
            assert patch_data['body'] == post.body
            assert patch_data['is_published'] == post.is_published

        class Context_게시글이_없는_경우:
            @pytest.fixture
            def post(self):
                post = PostFactory.build()

                return post

            def test_404를_반환한다(self, logged_in_user, subject):
                assert 404 == subject.status_code

        class Context_비로그인_유저인_경우:
            def test_401을_반환한다(self, not_logged_in_user, subject):
                assert 401 == subject.status_code

    class Describe_delete:
        @pytest.fixture
        def post(self):
            post = PostInBoardFactory.build()

            db.session.add(post)
            db.session.commit()

            return post

        @pytest.fixture
        def subject(self, client, post):
            response = client.delete(f'/posts/{post.id}')
            return response

        def test_200을_반환한다(self, logged_in_user, subject):
            assert subject.status_code == 200

        def test_게시글을_삭제한다(self, logged_in_user, subject):
            post = Post.query.all()

            assert len(post) == 0

        class Context_게시글이_없는_경우:
            @pytest.fixture
            def post(self):
                post = PostFactory.build()

                return post

            def test_404를_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 404

        class Context_비로그인_유저인_경우:
            def test_401을_반환한다(self, not_logged_in_user, subject):
                assert subject.status_code == 401

    class Describe_rank:
        @pytest.fixture
        def post(self):
            post = PostInBoardFactory.build()

            db.session.add(post)
            db.session.commit()

            return post

        @pytest.fixture
        def subject(self, client, post):
            response = client.get('/posts/rank')
            return response

        def test_게시글_랭킹_목록을_가져온다(self, subject):
            assert subject.status_code == 200

    class Describe_like:
        @pytest.fixture
        def post(self):
            post = PostInBoardFactory.build()

            db.session.add(post)
            db.session.commit()

            return post

        @pytest.fixture
        def subject(self, client, post):
            response = client.patch(f'/posts/{post.id}/like')
            return post.id, response

        def test_200을_반환한다(self, logged_in_user, subject):
            assert subject[1].status_code == 200

        def test_좋아요_수가_1_증가한다(self, logged_in_user, subject):
            post_id = subject[0]
            post = Post.query.get(post_id)

            assert post.like_count == 1

        class Context_게시글이_없는_경우:
            @pytest.fixture
            def post(self):
                post = PostFactory.build()

                return post

            def test_404를_반환한다(self, logged_in_user, subject):
                assert subject[1].status_code == 404

        class Context_비로그인_유저인_경우:
            def test_401을_반환한다(self, not_logged_in_user, subject):
                assert subject[1].status_code == 401

    class Describe_unlike:
        @pytest.fixture
        def post(self):
            post = PostInBoardFactory.build(like_count=100)

            db.session.add(post)
            db.session.commit()

            return post

        @pytest.fixture
        def subject(self, client, post):
            response = client.patch(f'/posts/{post.id}/unlike')
            return post.id, response

        def test_200을_반환한다(self, logged_in_user, subject):
            assert subject[1].status_code == 200

        def test_좋아요_수가_1_감소한다(self, logged_in_user, subject):
            post_id = subject[0]
            post = Post.query.get_or_404(post_id)

            assert post.like_count == 99

        class Context_좋아요_카운트가_0인_경우:
            @pytest.fixture
            def post(self):
                post = PostInBoardFactory.build()

                db.session.add(post)
                db.session.commit()

                return post

            def test_좋아요_수는_0이다(self, logged_in_user, subject):
                post_id = subject[0]
                post = Post.query.get_or_404(post_id)

                assert post.like_count == 0

        class Context_게시글이_없는_경우:
            @pytest.fixture
            def post(self):
                post = PostInBoardFactory.build()

                return post

            def test_404를_반환한다(self, logged_in_user, subject):
                assert subject[1].status_code == 404

        class Context_비로그인_유저인_경우:
            def test_401을_반환한다(self, not_logged_in_user, subject):
                assert subject[1].status_code == 401
