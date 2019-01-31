import pytest

from app import db
from tests.boards.factories import BoardFactory
from tests.posts.factories import PostFactory


class Describe_PostsView:
    class Describe_list:
        @pytest.fixture
        def board(self):
            board = BoardFactory.build()
            board.post = PostFactory.build_batch(16)

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

        def test_게시글_목록을_가져온다(self, subject):
            data = subject.get_json()

            assert 15 == len(data)
            assert 200 == subject.status_code

        class Context_게시판이_존재하지_않을_경우:
            @pytest.fixture
            def board(self):
                board = BoardFactory.build()
                board.post = PostFactory.build_batch(10)

                return board

            def test_404를_반환한다(self, subject):
                data = subject.get_json()

                assert 404 == subject.status_code
                assert 'The board does not exist' == data['message']

    class Describe_detail:
        @pytest.fixture
        def post(self):
            post = PostFactory.build()

            db.session.add(post)
            db.session.commit()

            return post

        def test_게시글_세부_목록을_가져온다_조회수_1_증가(self, client, post):
            url = f'/posts/{post.id}'
            response = client.get(url)
            data = response.get_json()

            assert 200 == response.status_code
            assert 1 == data['view_count']
            assert 0 == data['like_count']

    class Describe_create:

        @pytest.fixture
        def board(self):
            board = BoardFactory.build()

            db.session.add(board)
            db.session.commit()

            return board

        @pytest.fixture
        def form(self):
            post = PostFactory.build()

            return post

        @pytest.fixture
        def subject(self, client, board, form):
            url = f'/boards/{board.id}/posts'
            response = client.post(url, json={
                'title': form.title,
                'body': form.body,
                'is_published': form.is_published
            })

            return response

        def test_게시글이_생성된다(self, logged_in_user, subject):
            assert 200 == subject.status_code

        class Context_게시판이_존재하지_않는_경우:
            @pytest.fixture
            def board(self):
                board = BoardFactory.build()

                return board

            def test_404를_반환한다(self, logged_in_user, subject):
                assert 404 == subject.status_code

        class Context_비로그인_유저인_경우:
            def test_401을_반환한다(self, not_logged_in_user, subject):
                assert 401 == subject.status_code

        class Context_title값이_없는_경우:
            @pytest.fixture
            def form(self):
                post = PostFactory.build(title=None)

                return post

            def test_422을_반환한다(self, logged_in_user, subject):
                assert 422 == subject.status_code

        class Context_body값이_없는_경우:
            @pytest.fixture
            def form(self):
                post = PostFactory.build(body=None)

                return post

            def test_422을_반환한다(self, logged_in_user, subject):
                assert 422 == subject.status_code

    class Describe_rank:
        @pytest.fixture
        def post(self):
            post = PostFactory.build()

            db.session.add(post)
            db.session.commit()

            return post

        @pytest.fixture
        def subject(self, client):
            response = client.get('/posts/rank')

            return response

        def test_게시글_랭킹_목록을_가져온다(self, post, subject):
            assert 200 == subject.status_code

        class Context_게시글이_없는_경우:
            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

    # class Describe_update:
    # class Describe_delete:
    # class Describe_like:
