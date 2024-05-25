

import datetime

from flask import flash, g, redirect, url_for
from flask_babel import gettext
from flask_login import login_required
from flask import abort
from flask import render_template

from application import app, db
from application.ticket_system.forms.ticket_system_forms import UnSubscribeUser
from application.ticket_system.models.ticket_system_models import FlicketSubscription
from application.ticket_system.models.ticket_system_models import FlicketTicket
from application.ticket_system.models.ticket_system_user import FlicketUser
from application.ticket_system.scripts.ticket_system_functions import add_action
from . import flicket_bp


@flicket_bp.route(app.config['FLICKET'] + 'unsubscribe/<int:ticket_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def unsubscribe_ticket(ticket_id=None, user_id=None):
    if not ticket_id and user_id:
        return abort(404)

    form = UnSubscribeUser()

    ticket = FlicketTicket.query.filter_by(id=ticket_id).one()
    user = FlicketUser.query.filter_by(id=user_id).one()

    form.username.data = user.username

    if form.validate_on_submit():

        if ticket.can_unsubscribe(user):
            subscription = FlicketSubscription.query.filter_by(user=user, ticket=ticket).one()
            # unsubscribe user to ticket
            ticket.last_updated = datetime.datetime.now()
            add_action(ticket, 'unsubscribe', recipient=user)
            db.session.delete(subscription)
            db.session.commit()
            flash(gettext('"{}" has been unsubscribed from this ticket.'.format(user.name)), category='success')

        else:

            flash(gettext('Could not unsubscribe "{}" from ticket due to permission restrictions.'.format(user.name)),
                  category='warning')

        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

    # else:
    #     print(form.errors)

    return render_template('ticket_system_unsubscribe_user.html', form=form, title='Unsubscribe', ticket=ticket, user=user)