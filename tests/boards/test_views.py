import pytest

from app import db
from tests.boards.factories import BoardFactory


class Describe_BoardsView:
    @pytest.fixture
    def boards(self):
        board1 = BoardFactory.build()
        board2 = BoardFactory.build()

        db.session.add(board1)
        db.session.add(board2)
        db.session.commit()

        return [board1, board2]

    class Describe_list:
        def test_게시판_목록을_가져온다(self, client, boards):
            response = client.get('/boards/')
            data = response.get_json()

            assert 200 == response.status_code
            assert boards[0].title == data[0]['title']
            assert boards[1].title == data[1]['title']