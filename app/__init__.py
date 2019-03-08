from datetime import timedelta
from functools import wraps

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required
from flask_jwt_extended.exceptions import UserClaimsVerificationError, NoAuthorizationError
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from marshmallow import ValidationError
from werkzeug.exceptions import Unauthorized

from app.config import config
from app.exceptions import NotFoundException, UnauthorizedException, WriterOnlyException
from app.helpers import camel_to_snake, change_dict_naming_convention, snake_to_camel
from app.queries import CustomBaseQuery

db = SQLAlchemy(query_class=CustomBaseQuery)
ma = Marshmallow()
lm = LoginManager()
jm = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Set config
    if test_config is None:
        app.config.from_object(config.BaseConfig)
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
    jm.init_app(app)

    # CORS policy
    CORS(app, supports_credentials=True)

    # register views
    from .users.views import UserView
    from .boards.views import BoardView
    from .posts.views import PostView
    from .comments.views import CommentView

    CommentView.register(app, route_base='/', trailing_slash=False)
    PostView.register(app, route_base='/', trailing_slash=False)
    BoardView.register(app, route_base='boards', trailing_slash=False)
    UserView.register(app, route_base='users', trailing_slash=False)

    @app.before_request
    def change_case_convention():
        if request.json:
            converted_data = change_dict_naming_convention(request.json, camel_to_snake)
            request.data = converted_data

        if request.args:
            converted_args = change_dict_naming_convention(request.args, camel_to_snake)
            request.args = converted_args

    return app


def transaction(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    return decorated_view


def handle_error(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except NotFoundException as e:
            return jsonify({'msg': e.message}), 404
        except ValidationError as e:
            return jsonify(e.messages), 422
        except Unauthorized as e:
            return jsonify({'msg': e.description}), 401
        except WriterOnlyException as e:
            return jsonify({'msg': e.message}), 403
        except NoAuthorizationError as e:
            raise NoAuthorizationError
        except Exception as e:
            raise e

    return decorated_view
