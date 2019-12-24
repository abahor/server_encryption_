# hard shit will be here
from functools import wraps
from flask import request, session
from flask_login import current_user

from myproject import socket
from flask_socketio import emit, disconnect

# @socketio.route('/connect',namespace='mainsocket')
from myproject.models import authenticated_user, active_users


@socket.on('accepted', namespace='/mainsocket')
def accepted(msg):
    if check_for_token(msg['token']):
        disconnect()
    # checking recipient
    my = myid()
    recipient = rec_by_id(msg['id'])
    if not recipient:
        disconnect()
    emit('accepted_of_connection', {'hisid': my}, recipient=recipient)


@socket.on('rejected', namespace='/mainsocket')
def rejected(msg):
    if check_for_token(msg['token']):
        disconnect()

    recipient = rec_by_id(msg['id'])

    my = myid()
    emit('rejected_of_connection', {'hisid': my}, recipient=recipient)


@socket.on('see_if_connected', namespace='/mainsocket')
def see_if_connected(msg):
    if check_for_token(msg['token']):
        disconnect()

    if current_user.myid == msg['his_id']:
        return disconnect()
    my = myid()
    if active_users.query.filter_by(user_id=msg['his_id']).first():
        recipient = rec_by_id(msg['his_id'])

        emit('receive', {'hisid': my}, recipent=recipient)
    else:
        emit('rejected_of_connection', {'hisid': msg['hisid']}, recipient=my)





















# USEFUL FUNCTION TO USE ABOVE
def check_for_token(token):
    try:
        if session['token']:
            pass
    except:
        if authenticated_user.query.filter_by(token=token).first():
            session['token'] = token
            return False
        else:
            return True
    if session['token'] == token:
        return False
    return ''


def rec_by_id(m):
    user = active_users.query.filter_by(user_id=m)
    if not user:
        return False
    return user.request_sid


def myid():
    token = request.args.get('token')
    io = authenticated_user.query.filter_by(token).first()
    if not io:
        return False
    return io.user_id
