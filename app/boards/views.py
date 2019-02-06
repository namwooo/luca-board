from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_login import login_required, current_user
from marshmallow import ValidationError
from sqlalchemy import exc

from app import db
from app.exceptions import WriterOnly
from .models import Board
from .schemas import BoardsSchema


class BoardsView(FlaskView):

    @route('', methods=['GET'])
    def list(self):
        """List all boards ordered by created date"""
        boards_schema = BoardsSchema(many=True)
        boards = Board.query.order_by(Board.created_at).all()

        return boards_schema.jsonify(boards), 200

    @route('', methods=['POST'])
    @login_required
    def create(self):
        """Create a board"""
        data = request.get_json()
        data['writer_id'] = current_user.id

        board_schema = BoardsSchema()
        try:
            result = board_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        new_board = result.data

        db.session.add(new_board)
        db.session.commit()

        return board_schema.jsonify(new_board), 200

    @route("/<id>", methods=['DELETE'])
    @login_required
    def delete(self, id):
        """Delete a board"""
        board = Board.query.get_or_404(id)

        if not board.is_writer(current_user):
            raise WriterOnly('Writer Only: permission denied')

        db.session.delete(board)  # integrity issue here
        db.session.commit()

        return '', 200

    @route("/update/<id>/", methods=['PUT'])
    @login_required
    def update(self, id):
        """Update a board title"""
        data = request.get_json()

        title = data['title']
        board = Board.query.filter_by(id=id).first()

        if not current_user.id == board.writer_id:
            raise WriterOnly('Only writer for the board is able to delete')

        board = Board.query.filter_by(id=id).first()
        board.title = title

        try:
            db.session.commit()
            return board_schema.jsonify(board), 200
        except exc.SQLAlchemyError:
            return 'internal server error', 500
