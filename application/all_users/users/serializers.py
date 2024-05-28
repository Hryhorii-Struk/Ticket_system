from flask import request
from marshmallow import Schema, fields, validate

from application import app, db
from application.all_users.users import User


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    email = fields.Email(required=True, validate=validate.Email(error='Invalid email address'))
    password = fields.Str(required=True, load_only=True,
                          validate=validate.Length(min=8, max=20, error='Password must be between 8 and 20 characters'))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def jsonify(self, user):
        pass


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = user_schema.load(data)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)
