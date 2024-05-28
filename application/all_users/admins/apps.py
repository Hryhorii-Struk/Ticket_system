from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from application.all_users.users import routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'jjj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'join'


db = SQLAlchemy(app)


class JWTManager:
    pass


jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_email_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class AdminsConfig:
    def __init__(self, app):
        self.app = app

    def init_app(self, app):
        self.app = app
        # Add any initialization code specific to the Admins module
        db.init_app(app)
        jwt.init_app(app)

    def register_blueprints(self):
        # Register any blueprints specific to the Admins module

        self.app.register_blueprint(routes.auth_bp, url_prefix='/auth')

    def register_extensions(self):
        # Register any extensions specific to the Admins module
        pass


# Create the Flask app and configure the extensions
app = Flask(__name__)
AdminsConfig(app).init_app(app)
AdminsConfig(app).register_blueprints()
AdminsConfig(app).register_extensions()

# Run the Flask app
if __name__ == '__main__':
    app.run()