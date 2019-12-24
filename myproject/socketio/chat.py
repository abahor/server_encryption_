from flask import request, session
from flask_login import current_user

from myproject import socket
from flask_socketio import emit, disconnect

from myproject.models import authenticated_user, active_users


#  NEED THE CHECKING FOR EVERY FUNCTION TO CHECK IF IT IS STILL WORKING

@socket.on('my_key', namespace='/start_chat')
def connect(msg):
    if check_for_token(msg['token']):
        disconnect()

    key = msg['key']
    recipient = rec_by_id(msg['hisid'])
    emit('exchange', {'key': key}, recipient=recipient)


@socket.on('send_message', namespace='/start_chat')
def send_message(msg):
    if check_for_token(msg['token']):
        disconnect()

    message = msg['message']
    recipient = rec_by_id(msg['hisid'])
    date = msg['date']
    emit('receive', {'message': message, 'date': date}, recipient=recipient)  # remove

















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
