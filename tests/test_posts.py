from app.posts.models import Board
from app.users.models import User


def test_board_model(db):
    new_user = User(username='luca',
                    email='luca@luca.com',
                    first_name='luca',
                    last_name='kim')
    new_user.set_password('qwer1234')
    db.session.add(new_user)
    db.session.commit()

    new_board = Board(writer_id=new_user.id,
                      title='Recruit')
    db.session.add(new_board)
    db.session.commit()

    board = Board.query.filter_by(id=1).first()
    assert board.writer_id == 1
    assert board.title == 'Recruit'


def test_post_model(db):
    new_user = User(username='luca',
                    email='luca@luca.com',
                    first_name='luca',
                    last_name='kim')
    new_user.set_password('qwer1234')
    db.session.add(new_user)
    db.session.commit()

    new_board = Board(writer_id=new_user.id,
                      title='Recruit')
    db.session.add(new_board)
    db.session.commit()

    new_post = Post(writer_id=new_user.id,
                    board_id=new_board.id,
                    title='recruit bluewhale',
                    body='wanted ios developer',
                    is_published=True)
    db.session.add(new_post)
    db.session.commit()

    post = Post.query.filter_by(id=1).first()
    assert post.writer_id == 1
    assert post.board_id == 1
    assert post.title == 'recruit bluewhale'
    assert post.body == 'wanted ios developer'
    assert post.is_published is True
    assert post.like_count == 0
    assert post.view_count == 0
