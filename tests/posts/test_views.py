import pytest

from app import db
from tests.posts.factories import PostFactory


class Describe_PostsView:
    class Describe_list:
        @pytest.fixture
        def posts(self):
            post1 = PostFactory.build(is_published=True)
            post2 = PostFactory.build(is_published=True)

            db.session.add(post1)
            db.session.add(post2)
            db.session.commit()

            return [post1, post2]

        def test_게시글_목록을_생성일_순으로_가져온다(self, client, posts):
            response = client.get('/posts/')
            data = response.get_json()

            post1 = data[0]
            post2 = data[1]

            assert 200 == response.status_code
            assert posts[0].id == post1['id']
            assert posts[0].writer_id == post1['writer_id']
            assert posts[0].board_id == post1['board_id']
            assert posts[0].title == post1['title']
            assert posts[0].is_published == post1['is_published']
            assert posts[0].view_count == post1['view_count']
            assert posts[0].like_count == post1['like_count']
            assert posts[1].id == post2['id']
            assert posts[1].writer_id == post2['writer_id']
            assert posts[1].board_id == post2['board_id']
            assert posts[1].title == post2['title']
            assert posts[1].is_published == post2['is_published']
            assert posts[1].view_count == post2['view_count']
            assert posts[1].like_count == post2['like_count']

    class Describe_detail:
        @pytest.fixture
        def post(self):
            post = PostFactory.build(is_published=True)

            db.session.add(post)
            db.session.commit()

            return post

        def test_조회수_1_증가_및_게시글_세부_목록을_가져온다(self, client, post):
            url = f'/posts/{post.id}/'
            response = client.get(url)
            data = response.get_json()

            assert 200 == response.status_code
            assert post.id == data['id']
            assert post.writer_id == data['writer_id']
            assert post.board_id == data['board_id']
            assert post.title == data['title']
            assert post.body == data['body']
            assert post.is_published == data['is_published']
            assert 1 == data['view_count']  #
            assert 0 == data['like_count']

    # class Describe_rank:
    #     def test_게시글_랭킹_목록을_가져온다(self, client):
    #         response = client.get('/posts/rank/')

    # class Describe_create:
    # class Describe_update:
    # class Describe_delete:
