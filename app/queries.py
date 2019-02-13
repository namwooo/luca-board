from flask_sqlalchemy import BaseQuery

from app.exceptions import NotFoundException


class CustomBaseQuery(BaseQuery):
    def get_or_404(self, ident):
        model_class_name = self._mapper_zero().class_.__name__

        rv = self.get(ident)
        if rv is None:
            # e.g. 'message': 'User 1 not found'
            # abort(mapping=NotFoundException, message=model_class_name + ' ' + str(ident) + ' not found')
            raise NotFoundException()
            # error_message = json.dumps({'message': model_class_name + ' ' + str(ident) + ' not found'})
            # abort(Response(error_message, 404))
        return rv

    def first_or_404(self):
        rv = self.first()
        if rv is None:
            raise NotFoundException()
        return rv
