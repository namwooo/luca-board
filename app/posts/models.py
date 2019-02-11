from sqlalchemy_utils import URLType

from app import db
from app.mixins import TimestampMixin


class Post(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    title = db.Column(db.String(240), nullable=False)
    body = db.Column(db.Text)
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    view_count = db.Column(db.Integer, nullable=False, default=0)

    writer = db.relationship('User', back_populates='posts', lazy=True)
    board = db.relationship('Board', back_populates='posts', lazy=True)
    comments = db.relationship('Comment', back_populates='post', lazy=True)

    # delete flag
    def __repr__(self):
        return '<{} id: {}, writer_id: {}, board_id: {}, title: {}, is_published: {}>' \
            .format(self.__class__.__name__, self.id, self.writer_id, self.board_id,
                    self.title, self.is_published)

    @property
    def image_count(self):
        return self.images.count()

    def has_image(self):
        return len(self.image_count) > 0

    def read(self):
        self.view_count += 1


class PostImage(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer,
                        db.ForeignKey('post.id'),
                        nullable=False)
    image_url = db.Column(URLType, nullable=False)
    caption = db.Column(db.String(120), nullable=True)

    post = db.relationship('Post', backref='images', lazy=True)

    def __str__(self):
        return f'{self.image_url}'

    def __repr__(self):
        return f'<PostImage {self.image_url}>'
