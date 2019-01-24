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

    def __init__(self, title=None, writer_id=None):
        self.title = title
        self.writer_id = writer_id

    def __str__(self):
        return '{}'.format(self.title)

    def __repr__(self):
        return '<Board {}>'.format(self.title)
