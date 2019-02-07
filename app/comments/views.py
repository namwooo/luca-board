from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_login import login_required, current_user
from marshmallow import ValidationError

from app.comments.models import Comment
from app.comments.schemas import CommentsSchema
from app.posts.models import Post


class CommentsView(FlaskView):

    @route('', methods=['POST'])
    @login_required
    def create(self):
        """create a comment in post"""
        data = request.get_json()
        data['writer_id'] = current_user.id

        if 'post_id' in data.keys():
            post = Post.query.get_or_404(data['post_id'])
        if 'comment_parent_id' in data.keys():
            comment = Comment.query.get_or_404(data['comment_parent_id'])

        comment_schema = CommentsSchema()
        try:
            result = comment_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        new_comment = result.data
        new_comment.save()

        return comment_schema.jsonify(new_comment), 200
