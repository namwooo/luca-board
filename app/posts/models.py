from sqlalchemy_utils import URLType

from app import db
from app.mixins import TimestampMixin


class Post(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer,
                          db.ForeignKey('user.id'),
                          nullable=False)
    board_id = db.Column(db.Integer,
                         db.ForeignKey('board.id'),
                         nullable=False)
    title = db.Column(db.String(240), nullable=False)
    body = db.Column(db.Text)
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    view_count = db.Column(db.Integer, nullable=False, default=0)
    image = db.relationship('PostImage', backref='post', lazy=True)
    comment = db.relationship('Comment', backref='post', lazy=True)

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f'<Post {self.title}>'


class PostImage(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer,
                        db.ForeignKey('post.id'),
                        nullable=False)
    image_url = db.Column(URLType, nullable=False)
    caption = db.Column(db.String(120), nullable=True)

    def __str__(self):
        return f'{self.image_url}'

    def __repr__(self):
        return f'<PostImage {self.image_url}>'
