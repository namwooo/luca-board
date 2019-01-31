from sqlalchemy import func

from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'),
                         nullable=False)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text)
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    view_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now(),
                           server_onupdate=func.now())
    image = db.relationship('PostImage', backref='image', lazy=True)

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f'<Post {self.title}>'


class PostImage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),
                        nullable=False)
    image_url = db.Column(db.String(100), nullable=False)
    caption = db.Column(db.String(30), nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now())

    def __str__(self):
        return f'{self.image_url}'

    def __repr__(self):
        return f'<PostImage {self.image_url}>'
