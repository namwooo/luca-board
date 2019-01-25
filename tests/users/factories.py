import factory

from app import db
from app.users.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = None

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.lazy_attribute(lambda obj: '%s' % obj.first_name)
    email = factory.lazy_attribute(lambda obj: '%s@test.com' % obj.first_name)
    password = factory.PostGenerationMethodCall('set_password',
                                                'vi8c4i9vho')


