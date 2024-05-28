from flask import Flask
from .models import db
from .views import analysts_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)

    app.register_blueprint(analysts_blueprint)

    return app
