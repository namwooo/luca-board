from flask import request
from flask_classful import FlaskView, route
from flask_login import login_required, current_user
from sqlalchemy import exc
from werkzeug import exceptions

from app import db
from app.boards.models import Board
from app.boards.schema import boards_schema, board_schema


class BoardView(FlaskView):

    def index(self):
        """List all boards ordered by created date"""
        boards = Board.query.order_by(Board.created_at).all()

        return boards_schema.jsonify(boards), 200

    @route("/create/", methods=['POST'])
    @login_required
    def create(self):
        """Create a board"""
        data = request.get_json()

        result = board_schema.load(data)
        new_board = result.data
        new_board.writer_id = current_user.id

        db.session.add(new_board)
        db.session.commit()

        board = Board.query.get(new_board.id)
        return board_schema.jsonify(board), 201

    @route("/delete/<id>/", methods=['DELETE'])
    @login_required
    def delete(self, id):
        """Delete a board"""
        board = Board.query.filter_by(id=id).first_or_404()

        db.session.delete(board)
        db.session.commit()

        return 'Delete success', 200

    @route("/update/<id>/", methods=['PUT'])
    @login_required
    def update(self, id):
        """Update a board title"""
        data = request.get_json()

        title = data['title']

        board = Board.query.filter_by(id=id).first()
        board.title = title

        try:
            db.session.commit()
            return board_schema.jsonify(board), 200
        except exc.SQLAlchemyError:
            return 'internal server error', 500













