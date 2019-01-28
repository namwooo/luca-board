import pytest

from app import db
from app.boards.models import Board
from tests.boards.factories import BoardFactory
from tests.users.factories import UserFactory


class Describe_BoardsView:
    @pytest.fixture
    def user(self):
        user = UserFactory.build()

        db.session.add(user)
        db.session.commit()

        return user

    @pytest.fixture
    def password(self):
        return 'vi8c4i9vho'

    @pytest.fixture
    def login_user(self, client, user, password):
        response = client.post('/users/login/', json={
            'username': user.username,
            'password': password
        })

        return user

    @pytest.fixture
    def board(self):
        board = BoardFactory.build()

        db.session.add(board)
        db.session.commit()

        return board

    class Describe_list:
        @pytest.fixture
        def boards(self):
            board1 = BoardFactory.build()
            board2 = BoardFactory.build()

            db.session.add(board1)
            db.session.add(board2)
            db.session.commit()

            return [board1, board2]

        def test_게시판_목록을_가져온다(self, client, boards):
            response = client.get('/boards/')
            data = response.get_json()

            assert 200 == response.status_code
            assert boards[0].title == data[0]['title']
            assert boards[1].title == data[1]['title']

    class Describe_create:
        @pytest.fixture
        def subject(self, client):
            response = client.post('/boards/create/', json={
                'title': 'Company life'
            })

            return response

        class Context_로그인한_유저의_경우:
            def test_게시판을_만든다(self, login_user, subject):
                board = Board.query.filter_by(title='Company life').first()

                assert 200 == subject.status_code
                assert 'Company life' == board.title
                assert login_user.id == board.writer_id

        class Context_비로그인_유저의_경우:
            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

    class Describe_delete:
        @pytest.fixture
        def subject(self, client, board):
            url = f'/boards/delete/{board.id}/'
            response = client.delete(url)

            return response

        class Context_로그인한_유저가_작성자인_경우:
            @pytest.fixture
            def board(self, login_user):
                board = BoardFactory.build(writer=login_user)

                db.session.add(board)
                db.session.commit()

                return board

            def test_게시판을_삭제한다(self, subject):
                board = Board.query.all()

                assert [] == board
                assert 200 == subject.status_code

        class Context_비로그인_유저인_경우:
            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_작성자가_아닌_경우:
            @pytest.fixture
            def board(self, login_user):
                board = BoardFactory.build()

                db.session.add(board)
                db.session.commit()

                return board

            def test_403을_반환한다(self, subject):
                assert 403 == subject.status_code

    class Describe_update:
        @pytest.fixture
        def subject(self, client, board):
            url = f'/boards/update/{board.id}/'
            response = client.put(url, json={
                'title': 'Recruit'
            })

            return response

        class Context_로그인한_유저가_작성자인_경우:
            @pytest.fixture
            def board(self, login_user):
                board = BoardFactory.build(writer=login_user)

                db.session.add(board)
                db.session.commit()

                return board

            def test_게시판을_수정한다(self, subject):
                assert 200 == subject.status_code

        class Context_비로그인_유저인_경우:
            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_작성자가_아닌_경우:
            @pytest.fixture
            def board(self, login_user):
                board = BoardFactory.build()

                db.session.add(board)
                db.session.commit()

                return board

            def test_403을_반환한다(self, subject):
                assert 403 == subject.status_code
