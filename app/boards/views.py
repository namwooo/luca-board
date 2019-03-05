from flask import request
from flask_classful import FlaskView
from flask_login import login_required, current_user

from app import transaction, handle_error, db
from app.exceptions import WriterOnlyException
from .models import Board
from .schemas import BoardSchema, BoardUpdateSchema, BoardCreateSchema


class BoardView(FlaskView):
    decorators = [transaction, handle_error]

    def index(self):
        """List all boards ordered by created date"""
        boards = Board.query.order_by(Board.created_at).all()

        boards_schema = BoardSchema(many=True)
        return boards_schema.jsonify(boards), 200

    def get(self, id):
        board = Board.query.get_or_404(id)
        
        board_schema = BoardSchema()
        return board_schema.jsonify(board), 200

    # @login_required
    def post(self):
        """Create a board"""
        data = request.get_json()

        board_create_schema = BoardCreateSchema()
        new_board = board_create_schema.load(data).data

        current_user.add_board(new_board)

        return '', 201

    # @login_required
    def patch(self, id):
        """Partial-update a board"""
        data = request.get_json()

        board = Board.query.get_or_404(id)
        if not board.is_writer(current_user):
            raise WriterOnlyException()

        board_update_schema = BoardUpdateSchema()
        board_update_schema.load(data)

        board.title = data['title']

        return '', 200

    # @login_required
    def delete(self, id):
        """Delete a board"""
        board = Board.query.get_or_404(id)
        if not board.is_writer(current_user):
            raise WriterOnlyException()

        db.session.delete(board)  # db integrityError issue here

        return '', 200
