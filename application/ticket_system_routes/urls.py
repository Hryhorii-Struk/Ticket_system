from flask import Blueprint

ticket_system_routes = Blueprint('ticket_system_routes', __name__)

@ticket_system_routes.route('/')
def index():
    return "Ticket system home page"

@ticket_system_routes.route('/tickets/')
def tickets():
    return "List of tickets"

@ticket_system_routes.route('/tickets/<int:ticket_id>/')
def ticket_detail(ticket_id):
    return f"Ticket {ticket_id} details"

@ticket_system_routes.route('/tickets/create/', methods=['GET', 'POST'])
def create_ticket():
    return "Create new ticket"

@ticket_system_routes.route('/tickets/<int:ticket_id>/update/', methods=['GET', 'POST'])
def update_ticket(ticket_id):
    return f"Update ticket {ticket_id}"

@ticket_system_routes.route('/tickets/<int:ticket_id>/delete/', methods=['POST'])
def delete_ticket(ticket_id):
    return f"Delete ticket {ticket_id}"
