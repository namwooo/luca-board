from app import db
from app.mixins import TimestampMixin


class Board(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(240))

    writer = db.relationship('User', back_populates='boards', lazy=True)
    posts = db.relationship('Post', back_populates='board', lazy=True)

    def __repr__(self):
        return '<{} id: {}, writer_id: {}, title: {}>'\
            .format(self.__class__.__name__, self.id, self.writer_id, self.title)

    def is_writer(self, user):
        return self.writer_id == user.id

    def add_post(self, post):
        post.board_id = self.id
        db.session.add(post)
        db.session.flush()

        return post
