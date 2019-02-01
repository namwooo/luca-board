from app import db
from app.mixins import TimestampMixin


class Board(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    title = db.Column(db.Text)  # string
    post = db.relationship('Post', backref='board', lazy=True)

    def __str__(self):
        return '{}'.format(self.title)

    def __repr__(self):
        return '<Board {}>'.format(self.title)
