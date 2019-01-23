from sqlalchemy import func

from app import db


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    title = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now(),
                           server_onupdate=func.now())

    def __str__(self):
        return '{}'.format(self.title)

    def __repr__(self):
        return '<Board {}>'.format(self.title)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'),
                         nullable=False)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text)
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    view_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now(),
                           server_onupdate=func.now())

    def __str__(self):
        return '{}'.format(self.title)

    def __repr__(self):
        return '<Post {}>'.format(self.title)




