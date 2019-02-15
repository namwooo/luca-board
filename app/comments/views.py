from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_login import login_required, current_user
from marshmallow import ValidationError

from app import db, WriterOnlyException, handle_error, transaction
from app.comments.models import Comment
from app.comments.schemas import CommentSchema, CommentsUpdateSchema, CommentWriteSchema
from app.posts.models import Post


class CommentView(FlaskView):
    decorators = [transaction, handle_error]

    @route('/posts/<id>/comments', methods=['GET'])
    def comment_list(self, id):
        post = Post.query.get_or_404(id)
        comments = Comment.query.filter_by(post_id=id) \
            .order_by(Comment.path.asc()).all()

        post.comments.order_by(Comment.path.asc()).all()

        comments_schema = CommentSchema(many=True)
        return comments_schema.jsonify(comments), 200

    @route('', methods=['POST'])
    @login_required
    def post(self):
        """create a comment in post"""
        json_data = request.get_json()

        comment_write_schema = CommentWriteSchema(context={'writer': current_user})
        new_comment = comment_write_schema.load(data).data

        # if 'post_id' in data.keys():
        #     post = Post.query.get_or_404(data['post_id'])
        if 'comment_parent_id' in data.keys():
            comment = Comment.query.get_or_404(data['comment_parent_id'])

        new_comment.set_path()
        post.add_comment(new_comment)

        return '', 201

    @route('/<id>', methods=['PATCH'])
    @login_required
    def update(self, id):
        """update a comment"""
        data = request.get_json()

        comment = Comment.query.get_or_404(id)

        if not comment.is_writer(current_user):
            raise WriterOnlyException('Writer Only: permission denied')

        comment_schema = CommentsSchema()
        comment_update_schema = CommentsUpdateSchema(context={'instance': comment})
        try:
            result = comment_update_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        updated_comment = result.data
        db.session.add(updated_comment)
        db.session.commit()

        return comment_schema.jsonify(updated_comment), 200

    @route('/<id>', methods=['DELETE'])
    @login_required
    def delete(self, id):
        """delete a comment"""
        comment = Comment.query.get_or_404(id)

        if not comment.is_writer(current_user):
            raise WriterOnlyException('Writer Only: permission denied')

        db.session.delete(comment)  # integrity issue here
        db.session.commit()

        return '', 200
