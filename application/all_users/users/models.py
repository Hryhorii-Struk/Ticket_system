from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', backref=db.backref('users', lazy=True))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Create groups
customer1_group = Group(name='Customer 1')
customer2_group = Group(name='Customer 2')
customer3_group = Group(name='Customer 3')

db.session.add_all([customer1_group, customer2_group, customer3_group])
db.session.commit()

# Create users
user1 = User(username='user1', password='password1')
user2 = User(username='user2', password='password2')
user3 = User(username='user3', password='password3')
user4 = User(username='user4', password='password4')
user5 = User(username='user5', password='password5')

db.session.add_all([user1, user2, user3, user4, user5])
db.session.commit()

# Add users to groups
user1.group = customer1_group
user2.group = customer1_group
user3.group = customer2_group
user4.group = customer3_group
user5.group = customer3_group

db.session.commit()


@app.route('/add_users_to_group', methods=['POST'])
def add_users_to_group():
    data = request.get_json()
    group_name = data.get('group_name')
    user_usernames = data.get('user_usernames')

    if not group_name or not user_usernames:
        return jsonify({'error': 'Invalid request payload'}), 400

    group = Group.query.filter_by(name=group_name).first()
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    users = User.query.filter(User.username.in_(user_usernames)).all()
    if len(users) != len(user_usernames):
        return jsonify({'error': 'Some users not found'}), 404

    for user in users:
        user.group = group
    db.session.commit()

    return jsonify({'message': 'Users added to group successfully'})


if __name__ == '__main__':
    app.run()