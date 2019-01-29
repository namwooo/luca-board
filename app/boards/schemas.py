from marshmallow import post_load

from app import ma
from .models import Board


class BoardsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'writer_id',
                  'title', 'created_at',
                  'updated_at')

    @post_load
    def make_board(self, data):
        return Board(**data)


board_schema = BoardsSchema()
boards_schema = BoardsSchema(many=True)