import pytest

from tests.boards.factories import BoardFactory
from tests.users.factories import UserFactory


class Describe_Board:
    @pytest.fixture
    def board(self):
        board = BoardFactory.create()
        return board

    @pytest.fixture
    def user(self):
        user = UserFactory.create()
        return user

    class Describe___repr__:
        def test_Board_객체를_보여준다(self, board):
            assert str(board.__repr__()) == '<{} id: {}, writer_id: {}, title: {}>' \
                .format(board.__class__.__name__, board.id, board.writer_id, board.title)

    class Describe_is_writer:
        class Context_작성자가_다른_경우:
            def test_False를_반환한다(self, board, user):
                assert board.is_writer(user) == False

        class Context_작성자가_같은_경우:
            def test_True를_반환한다(self, board):
                assert board.is_writer(board.writer) == True
