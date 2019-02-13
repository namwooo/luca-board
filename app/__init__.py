from functools import wraps

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from werkzeug.exceptions import Unauthorized

from app.exceptions import NotFoundException, UnauthorizedException, WriterOnlyException
from app.queries import CustomBaseQuery

db = SQLAlchemy(query_class=CustomBaseQuery)
ma = Marshmallow()
lm = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:Demian!89@localhost/specup",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # import models
    from .users.models import User
    from .boards.models import Board
    from .posts.models import Post, PostImage
    from .comments.models import Comment

    # initialize db, schema, login manager
    db.init_app(app)
    ma.init_app(app)
    lm.init_app(app)

    # register views
    from .users.views import UsersView
    from .boards.views import BoardsView
    from .posts.views import PostsView
    from .comments.views import CommentsView

    UsersView.register(app, trailing_slash=False)
    BoardsView.register(app, trailing_slash=False)
    PostsView.register(app, trailing_slash=False)
    CommentsView.register(app, trailing_slash=False)

    return app


def handle_error(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundException as e:
            return jsonify({'message': e.message}), 404
        except ValidationError as e:
            return jsonify(e.messages), 422
        except Unauthorized as e:
            return jsonify({'message': e.description}), 401
        except WriterOnlyException as e:
            return jsonify({'message': e.message}), 403
        except Exception as e:
            return jsonify({'message': e.message}), 500

    return decorated_view


def transaction(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()

    return decorated_view

    # @app.errorhandler(Exception)
    # def handle_error(error):
    #     response = jsonify(error.to_dict())
    #     response.status_code = error.status_code
    #     return response
    #
    # # login_required for flask login
    #
    # @app.errorhandler(401)
    # def handle_error(error):
    #     response = jsonify({'message': error.description})
    #     response.status_code = 401
    #     return response
