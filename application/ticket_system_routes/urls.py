from flask import Blueprint, request, jsonify
from .models import Ticket


ticket_system_routes = Blueprint('ticket_system_routes', __name__)


class SQLAlchemy:
    def __init__(self):
        self.session = None

    pass


db = SQLAlchemy()


@ticket_system_routes.route('/')
def index():
    return "Ticket system home page"


@ticket_system_routes.route('/tickets/')
def tickets():
    ticket = db.session.query(Ticket).all()
    return jsonify([ticket.to_dict() for ticket in ticket])


@ticket_system_routes.route('/tickets/<int:ticket_id>/')
def ticket_detail(ticket_id):
    ticket = db.session.query(Ticket).get(ticket_id)
    if ticket is None:
        return jsonify({'error': 'Ticket not found'}), 404
    return jsonify(ticket.to_dict())


@ticket_system_routes.route('/tickets/create/', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        ticket = Ticket()
        db.session.add(ticket)
        db.session.commit()
        return jsonify(ticket.to_dict()), 201
    return "Create new ticket"


@ticket_system_routes.route('/tickets/<int:ticket_id>/update/', methods=['GET', 'POST'])
def update_ticket(ticket_id):
    ticket = db.session.query(Ticket).get(ticket_id)
    if ticket is None:
        return jsonify({'error': 'Ticket not found'}), 404
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        ticket.update(**data)
        db.session.commit()
        return jsonify(ticket.to_dict())
    return f"Update ticket {ticket_id}"


@ticket_system_routes.route('/tickets/<int:ticket_id>/delete/', methods=['POST'])
def delete_ticket(ticket_id):
    ticket = db.session.query(Ticket).get(ticket_id)
    if ticket is None:
        return jsonify({'error': 'Ticket not found'}), 404
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket deleted'})
