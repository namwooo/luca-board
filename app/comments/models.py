from app import db
from app.mixins import TimestampMixin


class Comment(db.Model, TimestampMixin):
    _N = 6

    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer,
                          db.ForeignKey('user.id'),
                          nullable=False)
    post_id = db.Column(db.Integer,
                        db.ForeignKey('post.id'),
                        nullable=False)
    comment_parent_id = db.Column(db.Integer,
                                  db.ForeignKey('comment.id'),
                                  nullable=True)
    body = db.Column(db.Text)
    path = db.Column(db.Text)
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]),
                              lazy='dynamic')

    def __str__(self):
        return f'<Comment:{self.id}>'

    def __repr__(self):
        return f'<Comment: {self.id}>'

    def get_path(self):
        prefix = self.parent.path + '.' if self.parent else ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)

        return self.path

    def save(self):
        db.session.add(self)
        db.session.commit()

        self.get_path()

        db.session.commit()

    def level(self):
        return len(self.path) // self._N - 1
