from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db, WriterOnlyException, handle_error, transaction
from app.comments.models import Comment
from app.comments.schemas import CommentSchema, CommentsUpdateSchema, CommentWriteSchema
from app.helpers import convert_dump
from app.posts.models import Post


class CommentView(FlaskView):
    decorators = [transaction, handle_error]

    @route('/posts/<id>/comments', methods=['GET'])
    def index(self, id):
        post = Post.query.get_or_404(id)

        comments = Comment.query.filter_by(post_id=id) \
            .order_by(Comment.path.asc()).all()

        comments_schema = CommentSchema(many=True)
        response = convert_dump(comments, comments_schema)
        return response, 200

    @route('/comments', methods=['POST'])
    @jwt_required
    def post(self):
        """create a comment in post"""
        data = request.data
        post_id = request.args.get('post_id', 0)
        comment_parent_id = request.args.get('comment_id', 0)

        # check existence of post
        post = Post.query.get_or_404(post_id)

        writer_id = get_jwt_identity()
        data['writer_id'] = writer_id
        data['post_id'] = post_id

        # check only when parent comment id is passed
        if comment_parent_id:
            parent_comment = Comment.query.get_or_404(comment_parent_id)
            data['comment_parent_id'] = comment_parent_id

        comment_write_schema = CommentWriteSchema()
        result = comment_write_schema.load(data)
        new_comment = result.data

        new_comment.set_path()

        comment_schema = CommentSchema()

        return comment_schema.jsonify(new_comment), 201

    @route('/comments/<id>', methods=['PATCH'])
    @jwt_required
    def update(self, id):
        """update a comment"""
        data = request.data

        comment = Comment.query.get_or_404(id)

        user_id = get_jwt_identity()

        if not comment.is_writer(user_id):
            raise WriterOnlyException('Writer Only: permission denied')

        # comment_schema = CommentsSchema()
        comment_update_schema = CommentsUpdateSchema(context={'instance': comment})
        try:
            result = comment_update_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        return '', 200

    @route('comments/<id>', methods=['DELETE'])
    @jwt_required
    def delete(self, id):
        """delete a comment"""
        comment = Comment.query.get_or_404(id)

        user_id = get_jwt_identity()

        if not comment.is_writer(user_id):
            raise WriterOnlyException('Writer Only: permission denied')

        db.session.delete(comment)  # integrity issue here
        db.session.commit()

        return '', 200
