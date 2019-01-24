from app.posts.models import Board, Post
from app.users.models import User
from tests.test_users import login


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
    assert board.__str__() == 'Recruit'
    assert board.__repr__() == '<Board Recruit>'


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


def test_board_list(client, db):
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

    new_board = Board(writer_id=new_user.id,
                      title='Company life')
    db.session.add(new_board)
    db.session.commit()

    response = client.get('/board/')
    data = response.get_json()

    assert response.status == '200 OK'
    assert response.status_code == 200
    assert data[0]['title'] == 'Recruit'
    assert data[1]['title'] == 'Company life'


def test_board_creation(client, db):
    new_user = User(username='luca',
                    email='luca@luca.com',
                    first_name='luca',
                    last_name='kim')
    new_user.set_password('qwer1234')
    db.session.add(new_user)
    db.session.commit()

    login(client, 'luca', 'qwer1234')

    response = client.post('/board/create/', json={
        'title': 'Recruit',
    })
    data = response.get_json()

    assert response.status == '201 CREATED'
    assert response.status_code == 201
    assert data['title'] == 'Recruit'


def test_board_deletion(client, db):
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

    url = '/board/delete/{}/'.format(board.id)

    response = client.delete(url)

    board = Board.query.filter_by(title='Recruit').first()

    assert board is None
    assert response.status == '200 OK'
    assert response.status_code == 200


def test_board_update(client, db):
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

    url = '/board/update/{}/'.format(board.id)

    response = client.put(url, json={
        'title': 'Company life',
    })

    updated_board = Board.query.filter_by(id=board.id).first()

    assert updated_board.title == 'Company life'
    assert response.status == '200 OK'
    assert response.status_code == 200
