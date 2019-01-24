import pytest

from app import db
from app.boards.models import Board
from app.users.models import User
from tests.test_users import login


# Describe , Context


class Describe_BoardView:

    # fixture 가 동작하는 순서는 무엇일까요?
    @pytest.fixture
    def new_user(self):
        # UserFactory 로 비밀번호를 같이 set 해줄수 있는 방법을 연구해볼까요?
        new_user = User(username='luca',
                        email='luca@luca.com',
                        first_name='luca',
                        last_name='kim')
        new_user.set_password('qwer1234')
        db.session.add(new_user)
        db.session.commit()
        return new_user

    class Describe_index:
        @pytest.fixture
        def new_boards(self, new_user):
            new_board1 = Board(title='Test Board1', writer_id=new_user.id)
            new_board2 = Board(title='Test Board2', writer_id=new_user.id)
            db.session.add(new_board1)
            db.session.add(new_board2)
            db.session.commit()

        def test_board를_가져온다(self, client, new_boards):
            response = client.get('/boards/')
            data = response.get_json()

            assert response.status_code == 200
            assert 2 == len(data)
            assert 'Test Board1' == data[0]['title']
            assert 'Test Board2' == data[1]['title']

    class Describe_create:
        @pytest.fixture
        def subject(self, client):
            login(client, 'luca', 'qwer1234')

            response = client.post('/boards/create/', json={
                'title': 'Recruit',
            })

            return response

        def test_board를_생성한다(self, subject, new_user):
            data = subject.get_json()

            board = Board.query.filter_by(title=data['title']).first()
            assert board is not None

        def test_201을_반환한다(self, subject, new_user):
            assert 201 == subject.status_code

        class Context_로그인이_안됐을_때:
            def test_401을_반환한다(self, subject, new_user):
                # Expected 가 앞에 오게 된다.
                assert 401 == subject.status_code

            def test_board가_생성되지_않는다(self, subject, new_user):
                assert 0 == Board.query.count()

    class Describe_delete:
        @pytest.fixture
        def new_board(self, new_user):
            new_board = Board(title='Test Board1', writer_id=new_user.id)
            db.session.add(new_board)
            db.session.commit()
            return new_board

        def test_board를_삭제한다(self, client, new_board):
            login(client, 'luca', 'qwer1234')

            url = '/boards/delete/{}/'.format(new_board.id)

            response = client.delete(url)
            assert 200 == response.status_code

        class Context_본인이_아닐_때:
            @pytest.fixture
            def other_user(self):
                other_user = User(username='luca2',
                                  email='luca2@luca.com',
                                  first_name='luca2',
                                  last_name='kim')
                other_user.set_password('qwer12345')
                db.session.add(other_user)
                db.session.commit()
                return other_user

            def test_board를_삭제할_수_없다(self, client, new_board, other_user):
                login(client, 'luca2', 'qwer12345')
                url = '/boards/delete/{}/'.format(new_board.id)

                response = client.delete(url)
                assert 403 == response.status_code

    class Describe_update:
        def test_board를_수정한다(self, client):
            new_user = User(username='luca',
                            email='luca@luca.com',
                            first_name='luca',
                            last_name='kim')
            new_user.set_password('qwer1234')

            db.session.add(new_user)
            db.session.commit()

            login(client, 'luca', 'qwer1234')

            user = User.query.filter_by(username='luca').first()

            new_board = Board(writer_id=user.id,
                              title='Recruit')

            db.session.add(new_board)
            db.session.commit()

            board = Board.query.filter_by(title='Recruit').first()

            url = f'/boards/update/{board.id}/'

            response = client.put(url, json={
                'title': 'Company life',
            })

            updated_board = Board.query.filter_by(id=board.id).first()

            assert updated_board.title == 'Company life'
            assert response.status == '200 OK'
            assert response.status_code == 200

# import pytest
# from flask import Response, url_for, json
#
# from app import db
# from app.boards.models import Board
# from app.users.models import User
# from tests.test_users import login
#
#
# @pytest.mark.usefixtures('client_class')
# class Describe_BoardView:
#     class Describe_create:
#         @pytest.fixture
#         def user(self):
#             user = User(username='luca', email='luca@luca.com', first_name='luca', last_name='kim')
#             user.set_password('luca_good')
#             db.session.add(user)
#             db.session.commit()
#             return user
#
#         @pytest.fixture
#         def boards(self, user):
#             board = Board(title='Testing Board')
#             board.writer_id = user.id
#             db.session.add(board)
#             db.session.commit()
#
#         @pytest.fixture
#         def logged_in_user(self, user):
#             data = json.dumps(dict(username=user.username, password='luca_good'))
#             response: Response = self.client.post(url_for('UserView:login'), data=data, content_type='application/json')
#             assert 200 == response.status_code
#             return user
#
#         def test_board_리스트를_가져온다(self, boards):
#             response: Response = self.client.get(url_for('BoardView:index'))
#             assert 200 == response.status_code
#             assert 1 == len(response.get_json())
#
#         def test_board가_생성된다(self, logged_in_user):
#             data = dict(title='Test Board')
#             response: Response = self.client.post(url_for('BoardView:create'), data=json.dumps(data), content_type='application/json')
#             assert 201 == response.status_code
#
#         def test_board가_삭제된다(self):
#             pass
#
#         def test_board가_수정된다(self):
#             pass
