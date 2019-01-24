import pytest
from flask import Response, url_for, json

from app import db
from app.boards.models import Board
from app.users.models import User
from tests.test_users import login


@pytest.mark.usefixtures('client_class')
class Describe_BoardView:
    class Describe_create:
        @pytest.fixture
        def user(self):
            user = User(username='luca', email='luca@luca.com', first_name='luca', last_name='kim')
            user.set_password('luca_good')
            db.session.add(user)
            db.session.commit()
            return user

        @pytest.fixture
        def boards(self, user):
            board = Board(title='Testing Board')
            board.writer_id = user.id
            db.session.add(board)
            db.session.commit()

        @pytest.fixture
        def logged_in_user(self, user):
            data = json.dumps(dict(username=user.username, password='luca_good'))
            response: Response = self.client.post(url_for('UserView:login'), data=data, content_type='application/json')
            assert 200 == response.status_code
            return user

        def test_board_리스트를_가져온다(self, boards):
            response: Response = self.client.get(url_for('BoardView:index'))
            assert 200 == response.status_code
            assert 1 == len(response.get_json())

        def test_board가_생성된다(self, logged_in_user):
            data = dict(title='Test Board')
            response: Response = self.client.post(url_for('BoardView:create'), data=json.dumps(data), content_type='application/json')
            assert 201 == response.status_code

        def test_board가_삭제된다(self):
            pass

        def test_board가_수정된다(self):
            pass
