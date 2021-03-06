import pytest

from app import db
from app.boards.models import Board
from tests.boards.factories import BoardFactory


class Describe_BoardView:

    @pytest.fixture
    def response_data(self, subject):
        json_data = subject.get_json()
        return json_data

    class Describe_index:
        @pytest.fixture
        def boards(self):
            boards = BoardFactory.build_batch(10)

            db.session.add_all(boards)
            db.session.commit()

            return boards

        @pytest.fixture
        def subject(self, client, boards):
            response = client.get('/boards')
            return response

        def test_200을_반환한다(self, subject):
            assert subject.status_code == 200

        def test_게시판_목록을_가져온다(self, response_data):
            assert len(response_data) == 10

    class Describe_create:
        @pytest.fixture
        def board_data(self):
            board_data = {
                'title': 'Company life'
            }

            return board_data

        @pytest.fixture
        def subject(self, client, board_data):
            response = client.post('/boards', json=board_data)
            return response

        class Context_로그인한_유저의_경우:
            def test_201을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 201

            def test_게시판을_만든다(self, logged_in_user, subject, board_data):
                board = Board.query.filter(Board.title == board_data['title']).first()

                assert board_data['title'] == board.title
                assert logged_in_user.id == board.writer_id

        class Context_비로그인_유저의_경우:
            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

        class Context_title값이_없는_경우:
            @pytest.fixture
            def board_data(self, board_data):
                board_data.pop('title')

                return board_data

            def test_422을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 422

    class Describe_patch:
        @pytest.fixture
        def board_data(self):
            board_data = {
                'title': 'Company life'
            }

            return board_data

        @pytest.fixture
        def subject(self, client, board, board_data):
            url = f'/boards/{board.id}'
            response = client.patch(url, json=board_data)

            return response

        class Context_로그인한_유저가_작성자인_경우:
            @pytest.fixture
            def board(self, logged_in_user):
                board = BoardFactory.build(writer=logged_in_user)

                db.session.add(board)
                db.session.commit()

                return board

            def test_200을_반환한다(self, subject):
                assert subject.status_code == 200

            def test_게시판을_수정한다(self, response_data, board_data):
                board = Board.query.all()[0]

                assert board.title == board_data['title']

        class Context_게시판이_없는_경우:
            @pytest.fixture
            def board(self, logged_in_user):
                board = BoardFactory.build(writer=logged_in_user)

                return board

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

        class Context_비로그인_유저인_경우:
            @pytest.fixture
            def board(self):
                board = BoardFactory.build()

                db.session.add(board)
                db.session.commit()

                return board

            def test_401을_반환한다(self, not_logged_in_user, subject):
                assert subject.status_code == 401

        class Context_작성자가_아닌_경우:
            @pytest.fixture
            def board(self):
                board = BoardFactory.build()

                db.session.add(board)
                db.session.commit()

                return board

            def test_403을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 403

            def test_WriterOnly_메세지를_반환한다(self, logged_in_user, response_data):
                assert response_data['message'] == \
                       'writer only'

    class Describe_delete:
        @pytest.fixture
        def board(self, logged_in_user):
            board = BoardFactory.build(writer=logged_in_user)

            db.session.add(board)
            db.session.commit()

            return board

        @pytest.fixture
        def subject(self, client, board):
            url = f'/boards/{board.id}'
            response = client.delete(url)

            return response

        class Context_로그인한_유저가_작성자인_경우:

            def test_200을_반환한다(self, subject):
                assert subject.status_code == 200

            def test_게시판을_삭제한다(self, subject):
                board = Board.query.all()

                assert len(board) == 0

        class Context_게시판이_없는_경우:
            @pytest.fixture
            def board(self, logged_in_user):
                board = BoardFactory.build(writer=logged_in_user)

                return board

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

        class Context_비로그인_유저인_경우:
            @pytest.fixture
            def board(self):
                board = BoardFactory.build()

                db.session.add(board)
                db.session.commit()

                return board

            def test_401을_반환한다(self, not_logged_in_user, subject):
                assert subject.status_code == 401

        class Context_작성자가_아닌_경우:
            @pytest.fixture
            def board(self):
                board = BoardFactory.build()

                db.session.add(board)
                db.session.commit()

                return board

            def test_403을_반환한다(self, logged_in_user, subject):
                assert subject.status_code == 403

            def test_WriterOnly_메세지를_반환한다(self, logged_in_user, response_data):
                assert response_data['message'] == \
                       'writer only'
