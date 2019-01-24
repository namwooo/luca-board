import factory
from factory.alchemy import SQLAlchemyModelFactory

from app import db
from app.users.models import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    username = factory.Faker('name')
    email = factory.Faker('email')
    first_name = factory.Sequence(lambda n: 'first name %d' % n)
    last_name = factory.Sequence(lambda n: 'last name %d' % n)
    password = factory.Faker('password')
