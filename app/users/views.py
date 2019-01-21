from flask_classful import FlaskView


class IndexView(FlaskView):
    def index(self):
        return 'hey jude'