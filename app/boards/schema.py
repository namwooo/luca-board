from marshmallow import post_load, post_dump

from app import ma
from app.boards.models import Board


class BoardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'writer_id',
                  'title', 'created_at',
                  'updated_at')

    @post_load
    def make_board(self, data):
        return Board(**data)


board_schema = BoardSchema()
boards_schema = BoardSchema(many=True)