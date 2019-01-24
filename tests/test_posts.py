from app.boards.models import Board
from app.posts.models import Post
from app.users.models import User


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
                    body='wanted ios developer')
    db.session.add(new_post)
    db.session.commit()

    post = Post.query.filter_by(id=1).first()
    assert post.title == 'recruit bluewhale'
    assert post.body == 'wanted ios developer'
    assert post.is_published is False
    assert post.like_count == 0
    assert post.view_count == 0
    assert post.__str__() == 'recruit bluewhale'
    assert post.__repr__() == '<Post recruit bluewhale>'
