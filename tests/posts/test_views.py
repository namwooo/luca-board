import pytest

from app import db
from tests.posts.factories import PostFactory


class Describe_PostsView:
    class Describe_list:
        @pytest.fixture
        def posts(self):
            post1 = PostFactory.build()
            post2 = PostFactory.build()

            db.session.add(post1)
            db.session.add(post2)
            db.session.commit()

            return [post1, post2]

        def test_게시글_목록을_가져온다(self, client, posts):
            response = client.get('/posts/')
            data = response.get_json()

            assert 200 == response.status_code
            assert posts[0].title == data[0]['title']
            assert posts[0].body == data[0]['body']
            assert posts[1].title == data[1]['title']
            assert posts[1].body == data[1]['body']

    # class Describe_detail:
    # class Describe_create:
    # class Describe_update:
    # class Describe_delete:
