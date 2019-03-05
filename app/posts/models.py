from sqlalchemy_utils import URLType

from app import db
from app.mixins import TimestampMixin

likes = db.Table('likes',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                 db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                 )


class Post(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(240), nullable=False)
    body = db.Column(db.Text)
    has_image = db.Column(db.Boolean, nullable=False, default=False)
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    view_count = db.Column(db.Integer, nullable=False, default=0)

    writer = db.relationship('User', back_populates='posts', lazy='joined')
    board = db.relationship('Board', back_populates='posts', lazy='joined')
    comments = db.relationship('Comment', back_populates='post', lazy='select')
    images = db.relationship('PostImage', back_populates='post', lazy='select')  # joined
    like_users = db.relationship('User', secondary=likes,
                                 back_populates='like_posts', lazy='subquery')

    def __repr__(self):
        return '<{}(id: {}, writer_id: {}, board_id: {}, title: {}, is_published: {})>' \
            .format(self.__class__.__name__, self.id, self.writer_id, self.board_id,
                    self.title, self.is_published)

    def read(self):
        self.view_count += 1

    def like(self):
        self.like_count += 1

    def unlike(self):
        if self.like_count == 0:
            pass
        else:
            self.like_count -= 1

    def add_comment(self, comment):
        comment.post_id = self.id
        db.session.add(comment)
        db.session.flush()

        return comment


class PostImage(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    image_url = db.Column(URLType, nullable=False)
    caption = db.Column(db.String(120), nullable=True)

    post = db.relationship('Post', back_populates='images', lazy=True)

    def __repr__(self):
        return '<{} id: {}, post_id: {}, image_url: {}, caption: {}>' \
            .format(self.__class__.__name__, self.id, self.post_id, self.image_url,
                    self.caption)
