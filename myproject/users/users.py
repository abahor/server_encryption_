# normal login and register normal
import threading
from datetime import *
import random
import string
import time

from flask import redirect, render_template, Blueprint, url_for, session, request, flash, abort, jsonify, Response
# from myproject import Session
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash

from myproject import db, limiter
from myproject import mail
from myproject.models import Users, active_users, BlockedUsers, authenticated_user  # ,  authenticated_user
from myproject.users.forms import updateForm, RegisterationForm, LoginForm, formRecover, changepassword, yourEmail, \
    confirmationForm

users = Blueprint('users', __name__, template_folder='temp')


# def update_user_active_date(token):
#     user = authenticated_user.query.filter_by(token=token).first()
#     user.last_time_checked = datetime.utcnow()


@users.route('/login', methods=['post', 'get'])
@limiter.limit("20 per hour")
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/')
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            # login_user(user, remember=True, duration=datetime.timedelta(weeks=52))
            login_user(user)

            nex = request.args.get('next')

            if nex is None or not nex[0] == '/' or nex == '/logout':
                nex = '/'
            return redirect(nex)
    print(form.errors)
    return render_template('login.html', form=form)


@users.route('/')
def main():
    return render_template('main.html')


@users.route('/register', methods=['POST', 'GET'])
@limiter.limit("20 per hour")
def register():
    if current_user.is_authenticated:
        return redirect('/')
    session['qwertyuiopdfghjkldfghjklsdfghjkfghjk'] = None
    form = RegisterationForm()
    if form.validate_on_submit():
        print('i a m s a d s o f u c k i n g m u c h')
        print(form.email.data)
        user = Users.query.filter_by(email=form.email.data).first()
        # print(user)
        if user:
            flash(Markup('''<div class="alert alert-secondary" role="alert">the email already exsit login instead <a
                href='/login'>login</a></div>'''))
            return render_template('register.html', form=form)
        else:
            print('except ')
            session['email'] = form.email.data
            # session['username'] = form.username.data
            session['password'] = form.password.data
            # try:
            messag = Message('confirmation code',
                             sender="jousefgamal46@gmail.com",
                             recipients=[form.email.data])
            session['confirmation'] = "".join(random.choice(string.digits) for x in range(random.randint(1, 7)))
            # link = f"http://127.0.0.1:5000/reset?de={session['verification']}"
            print(session['confirmation'])
            messag.body = f"Here is the confirmation code copy it and put it into the confirmation box to  your password {session['confirmation']} "
            messag.html = render_template('/confirmationmail.html')
            ser = Users(email=session['email'], password=session['password'],
                        myid=generate_new_id())
            db.session.add(ser)
            db.session.commit()

            # ---------------remove this when the internet come
            mail.send(messag)
            session['qwertyuiopdfghjkldfghjklsdfghjkfghjk'] = True
            return redirect(url_for('users.confirmation'))
            # except Exception as e:
            #     print(e)
            #     session['qwertyuiopdfghjkldfghjklsdfghjkfghjk'] = False
    print(form.errors)
    return render_template('register.html', form=form)


@users.route("/confirmation", methods=['post', 'get'])
@limiter.limit("30 per hour")
def confirmation():
    if current_user.is_authenticated:
        return render_template('logged_in_already.html')
    # try:
    if session['qwertyuiopdfghjkldfghjklsdfghjkfghjk']:
        print('i am happy')
        form = confirmationForm()
        if form.validate_on_submit():
            print('i am happy')
            print(session['confirmation'])
            if session['confirmation'] == form.password.data:
                ser = Users(email=session['email'], password=session['password'],
                            myid=generate_new_id())
                try:
                    db.session.add(ser)
                    db.session.commit()
                    session['qwertyuiopdfghjkldfghjklsdfghjkfghjk'] = None
                    # return redirect(url_for('users.login'))
                    return redirect(url_for('users.account'))
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    return 'something went wrong'
            else:
                flash('please enter the code correctly')
                return render_template('recover.html')
        else:
            print(form.errors)
            return render_template('recover.html', form=form)
    else:
        return redirect('/')
    # except Exception as e:
    #     abort(404)


# @users.route('/recover', methods=['GET', 'POST'])
# @login_required
# def recover():
#     form = formRecover()
#     try:
#         if session['change']:
#             if form.validate_on_submit():
#                 current_user.password = generate_password_hash(form.password.data)
#                 db.session.commit()
#                 session['change'] = False
#                 return render_template('recovered.html')
#             else:
#                 return render_template('recover.html', form=form)
#     except Exception as e:
#         abort(404)
#     return redirect(url_for('main.index'))

@users.route('/forget-password', methods=['post', 'get'])
def forget():
    if current_user.is_authenticated:
        return render_template('logged_in_already.html')
    form = yourEmail()
    if form.validate_on_submit():
        # print(form.email.data)
        d = Users.query.filter_by(email=form.email.data).first()
        # print(Users.query.filter_by(email='abahormelad@gmail.com').first().email)
        # print(d)
        if d is None:
            flash(Markup("<div class='alert alert-warning' role='alert'>this email doesn't related to any account try "
                         "<a href='/register'>register</a></div>"))
        else:
            session['user'] = d.id
            try:
                msg = Message('reset Email',
                              sender="jousefgamal46@gmail.com",
                              recipients=[form.email.data])
                session['verification'] = "".join(random.choice(string.digits) for x in range(random.randint(1, 12)))
                link = f"{url_for('reset', _external=True)}?de={session['verification']}"
                msg.body = f"Here is the reset link copy it and put it into your browser to reset your password " \
                    f"http:/127.0.0.1/reset?de={session['verification']}'>reset password</a>"
                msg.html = render_template('/resetpassword.html', link=link)
                mail.send(msg)
                flash(Markup('<div class="alert alert-success" role="alert">The email has been sent</div>'))
            except Exception as e:
                abort(404, e)
    return render_template('forget-password.html', form=form)


@users.route('/reset', methods=['get'])
def reset():
    form = formRecover()
    de = request.args.get('de')
    print(de)
    # print(session['verification'])
    try:
        if de == session['verification']:
            if form.validate_on_submit():
                d = Users.query.get(session['user'])
                d.password = generate_password_hash(form.password.data)
                db.session.commit()
                return redirect(url_for('users.login'))
            else:
                return render_template('recover.html', form=form)
    except Exception as e:
        abort(404, e)
    return redirect('/')


@users.route('/change', methods=['post', 'get'])
@login_required
@limiter.limit("30 per hour")
def change():
    form = changepassword()
    if form.validate_on_submit():
        # d = Users.query.filter_by(email=form.email.data).first()
        if check_password_hash(current_user.password, form.password.data):
            current_user.password = generate_password_hash(form.password_new.data)
            try:
                db.session.commit()
                flash('Password has been changed')
            except Exception as e:
                db.rollback()
                return abort(404, e)
    return render_template('change_password.html', form=form)


@users.route('/account')
@limiter.limit("30 per hour")
@login_required
def account():
    form = updateForm()
    return render_template('account.html', form=form)


# @users.route('/myid') # ----------    contact id
# users.route           ------------ my id

def generate_new_id():
    while True:
        chars = "".join([random.choice(string.ascii_letters + string.digits) for i in range(48)])
        check = Users.query.filter_by(myid=chars).first()
        if check:
            pass
        else:
            break
    return chars


@users.route('/username', methods=['post'])
@limiter.limit("10 per hour")
def username_check():
    try:
        del session['email_checked']
    except:
        pass
    # c = request.form['c']
    c = request.args.get('c')
    p = Users.query.filter_by(email=c).first()
    print(p)
    if p:
        session['email_checked'] = c
        return ''
    else:
        return abort(404)


@users.route('/password', methods=['post'])
@limiter.limit("10 per hour")
def password_check():
    if current_user.is_authenticated:
        return ''  # you is currently logged in
    if session['email_checked']:
        user = Users.query.filter_by(email=session['email_checked']).first()
        d = request.args.get('c')
        print(d)
        print(user)
        print(user.check_password(str(d)))
        if user.check_password(str(d)):
            login_user(user)
            token = generate_new_id()
            p = authenticated_user.query.filter_by(user_id=user.myid).first()
            if p:
                return {'id': p.user_id, 'token': p.token}
            u = authenticated_user(user_id=user.myid, token=token)  #
            db.session.add(u)
            db.session.commit()
            return jsonify({'token': token, 'id': user.myid})
        else:
            print('i am sad')
            return abort(404)
    return abort(404)


# @users.route('/test')
# def test():
#     d = request.args.get('te')
#     print(session['testing'])
#     session['testing'].append(d)
#     for i in session['testing']:
#         print(i)
#     return 'added'


@users.route('/privacy')
def privacy():
    return render_template('privacy.html')


# @users.route('/get')
# def get():
#     # get = session['testing']
#     print(session['testing'])
#     return str(session['testing'])


# @users.route('/d')
# def d():
#     session['testing'] = []
#     return ''
#

@users.route('/keep_alive', methods=['POST'])
def keep_alive():
    token = request.args.get('token')
    auth = authenticated_user.query.filter_by(token=token).first()
    if not auth:
        return abort(404)
    # update_user_active_date(token)
    # id = request.args.get('id')
    sid = request.sid
    try:
        if session['user_active_keep_alive_id']:
            user = active_users.query.get(session['user_active_keep_alive_id'])
            user.date = datetime.utcnow()
            auth.last_time_checked = datetime.utcnow()
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return abort(404)
    except:
        if active_users.query.filter_by(user_id=auth.user_id).first() is None:
            try:
                act = active_users(user_id=auth.user_id, request_sid=sid)
                db.session.add(act)
                auth.last_time_checked = datetime.utcnow()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return abort(404, e)

        else:
            try:
                current = active_users.query.filter_by(user_id=auth.user_id).first()
                current.date = datetime.utcnow()
                session['user_active_keep_alive_id'] = current.id
                auth.last_time_checked = datetime.utcnow()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return abort(404, e)

        if authenticated_user.query.filter_by(token=token):
            auth = authenticated_user.query.filter_by(user_id=id).first()
            auth.last_time_checked = datetime.utcnow()
        return 'success'
    return ''


# def check_if_user_is_authenticated():
#     d = authenticated_user.query.all()
#     for i in d:
#         if datetime.utcnow() - i.date > timedelta(hours=1):  # there is a problem here
#             db.session.delete(i)
#             db.session.commit()


#
#
# def update_the_active_users():
#     all_users = active_users.query.all()
#     for i in all_users:
#         if datetime.utcnow() - i.date > timedelta(seconds=10):
#             db.session.delete(i)
#             db.session.commit()
#
#
# #
# def par():
#     while True:
#         time.sleep(10)
#         update_the_active_users()
#         # check_if_user_is_authenticated()
#
#
# t = threading.Thread(target=par)
# t.start()


@users.route('/logout')
@login_required
def logout():
    logout_user()
    user_id = request.args.get('id')
    u = authenticated_user.query.filter_by(user_id=user_id).first()
    try:
        db.session.delete(u)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return abort(404, e)
    return render_template('logout.html')


# @users.route('/seeifconnected')
# @login_required
# def seeifconnected():
#     hisid = request.args.get('connectid')
#     token = request.args.get('token')
#     if not authenticated_user.query.filter_by(token=token).first():
#         return abort(404)
#     a = active_users.query.filter_by(user_id=hisid)
#     if a:
#         return 'success'
#     return ''


@users.route('/unblock')
@login_required
def unblock():
    hisid = request.args.get('id')
    o = BlockedUsers.query.filter_by(blocked_user=hisid)
    if o:
        db.session.delete(o)
        db.session.commit()
        return ''
    else:
        logout_user()
    return ''


@users.route('/about')
def about():
    return render_template('about.html')


@users.route('/if_logged_in', methods=['post'])
def if_logged_in():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return ''
    else:
        return abort(404)


@users.route('/myid', methods=['post'])
def myid():
    token = request.args.get('token')
    io = authenticated_user.query.filter_by(token=token).first()
    if not io:
        return abort(404)
    de = Users.query.filter_by(myid=io.user_id).first()
    return de.myid
