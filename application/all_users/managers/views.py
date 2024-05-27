from importlib.resources import Resource

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from application.all_users.admins.apps import JWTManager
from application.all_users.admins.views import jwt_required
from application.ticket_system.auth.views import Api
from application.ticket_system.models.serializers import UserSerializer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<UserModel(id={self.id}, is_active={self.is_active})>'


class NotifyManager(Resource):
    @jwt_required()
    def post(self, pk):
        brand_name = request.json.get('brand_name')

        return jsonify({'message': 'Manager has been notified'}), 200


class BanUserView(Resource):
    def patch(self, pk):
        user = UserModel.query.get(pk)
        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return jsonify(serializer.data), 200


def patch(pk):
    user = UserModel.query.get(pk)
    if not user.is_active:
        user.is_active = True
        user.save()
    serializer = UserSerializer(user)
    return jsonify(serializer.data), 200


class UnBanUserView(Resource):
    pass


api.add_resource(NotifyManager, '/notify_manager/<int:pk>')
api.add_resource(BanUserView, '/ban_user/<int:pk>')
api.add_resource(UnBanUserView, '/unban_user/<int:pk>')

if __name__ == '__main__':
    db.create_all()
    app.run()
