from flask import jsonify, request
from flask_classful import FlaskView, route
from flask_login import current_user, login_required
from marshmallow import ValidationError

from app import db
from app.boards.models import Board
from app.comments.models import Comment
from app.comments.schemas import CommentsSchema
from app.posts.schemas import posts_list_schema, posts_detail_schema, PostsSchema, PostsUpdateSchema
from .models import Post


class PostsView(FlaskView):

    @route('', methods=['POST'])
    @login_required
    def create(self):
        """Create a post in board"""
        data = request.get_json()
        board_id = data['board_id']
        post_schema = PostsSchema(context={'board_id': board_id,
                                           'writer_id': current_user.id})

        board = Board.query.get_or_404(board_id)  # find or fail

        try:
            result = post_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        new_post = result.data

        db.session.add(new_post)
        db.session.commit()

        return post_schema.jsonify(new_post), 200

    @route('/<id>', methods=['GET'])
    def detail(self, id):
        """Detail a post and plus view count"""

        post = Post.query.filter_by(id=id, is_published=True).first_or_404()

        post.view_count += 1

        db.session.add(post)
        db.session.commit()

        return posts_detail_schema.jsonify(post), 200

    @route('/<id>', methods=['PATCH'])
    @login_required
    def update(self, id):
        """Update a post"""
        data = request.get_json()
        post = Post.query.get_or_404(id)
        posts_update_schema = PostsUpdateSchema(context={'post_id': id,
                                                         'writer_id': current_user.id,
                                                         'instance': post})
        try:
            result = posts_update_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        updated_post = result.data

        db.session.add(updated_post)
        db.session.commit()

        return posts_update_schema.jsonify(updated_post), 200

    @route('/<id>', methods=['DELETE'])
    @login_required
    def delete(self, id):
        """Delete a post"""
        post = Post.query.get_or_404(id)

        db.session.delete(post)
        db.session.commit()

        return '', 200

    @route('/rank', methods=['GET'])
    def rank(self):
        """List ranked posts by its like counts"""
        # hybrid property
        posts = Post.query.filter(Post.is_published == True) \
            .order_by(Post.like_count.desc()) \
            .limit(10).all()

        print(posts)

        if not posts:
            return jsonify({'message': 'posts do not exist'}), 404

        return posts_list_schema.jsonify(posts), 200

    @route('/<id>/like', methods=['PATCH'])
    @login_required
    def like(self, id):
        """Plus 1 like count for the post"""
        posts_schema = PostsSchema()
        post = Post.query.get_or_404(id)

        post.like_count += 1

        db.session.add(post)
        db.session.commit()

        return posts_schema.jsonify(post), 200

    @route('/<id>/unlike', methods=['PATCH'])
    @login_required
    def unlike(self, id):
        """Minus 1 like count for the post"""
        posts_schema = PostsSchema()
        post = Post.query.get_or_404(id)

        if not post.like_count == 0:
            post.like_count -= 1

        db.session.add(post)
        db.session.commit()

        return posts_schema.jsonify(post), 200

    @route('/<id>/comments', methods=['GET'])
    def comment_list(self, id):
        post = Post.query.get_or_404(id)
        comments = Comment.query.filter_by(post_id=id).order_by(Comment.path.asc()).all()

        comments_schema = CommentsSchema(many=True)

        return comments_schema.jsonify(comments), 200
