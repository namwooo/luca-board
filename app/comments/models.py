from app import db
from app.mixins import TimestampMixin


class Comment(db.Model, TimestampMixin):
    # Number of path digit
    _N = 6

    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='SET NULL'), nullable=True)
    comment_parent_id = db.Column(db.Integer, db.ForeignKey('comment.id', onupdate='SET NULL'), nullable=True)
    body = db.Column(db.Text)
    path = db.Column(db.Text)

    writer = db.relationship('User', back_populates='comments', lazy='joined')
    post = db.relationship('Post', back_populates='comments', lazy='select')
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]),
                              lazy='dynamic')

    def __repr__(self):
        return '<{}(id: {}, writer_id: {}, post_id: {}, path: {})>' \
            .format(self.__class__.__name__, self.id, self.writer_id,
                    self.post_id, self.path)

    def set_path(self):
        db.session.add(self)
        db.session.flush()

        if self.parent.path:
            prefix = self.parent.path + '.'
        else:
            prefix = ''

        self.path = prefix + '{:0{}d}'.format(self.id, self._N)

        return self.path

    def level(self):
        return len(self.path) // self._N - 1

    def is_writer(self, user):
        return self.writer_id == user.id

    def add_child_comment(self, comment):
        comment.comment_parent_id = self.id
        db.session.add(comment)
        db.session.flush()

        return comment