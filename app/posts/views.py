from flask_classful import FlaskView

from app.posts.models import Board
from app.posts.schema import boards_schema


class BoardView(FlaskView):

    def index(self):
        boards = Board.query.order_by(Board.created_at).all()

        return boards_schema.jsonify(boards)



