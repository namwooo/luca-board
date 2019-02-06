from app import db
from app.mixins import TimestampMixin


class Comment(db.Model, TimestampMixin):
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

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return f'<Post {self.id}>'
