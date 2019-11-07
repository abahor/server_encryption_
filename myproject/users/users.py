# normal login and register normal
from datetime import *
import random
import string
import time

from flask import redirect, render_template, Blueprint, url_for, session, request, flash, abort
# from myproject import Session
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash

from myproject import db  # , limiter
from myproject import mail
from myproject.models import Users, active_users, authenticated_user
from myproject.users.forms import updateForm, RegisterationForm, LoginForm, formRecover, changepassword, yourEmail, \
    confirmationForm

users = Blueprint('users', __name__, template_folder='temp')


def update_user_active_date(token):
    user = authenticated_user.query.filter_by(token=token).first()
    user.last_time_checked = datetime.utcnow()


@users.route('/login', methods=['post', 'get'])
# @limiter.limit("30 per hour")
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/')
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True, duration=datetime.timedelta(weeks=52))

            nex = request.args.get('next')

            if nex is None or not nex[0] == '/':
                nex = '/'
            return redirect(nex)
    print(form.errors)
    return render_template('login.html', form=form)


@users.route('/')
def main():
    return render_template('main.html')


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    session['qwertyuiopdfghjkldfghjklsdfghjkfghjk'] = None
    form = RegisterationForm()
    if form.validate_on_submit():
        print('i a m s a d s o f u c k i n g m u c h')
        # print(form.email.data)
        user = Users.query.filter_by(email=form.email.data).first()
        print(user)
        if user:
            flash(Markup('''<div class="alert alert-secondary" role="alert">the email already exsit login instead <a
            href='/login'>login</a></div>'''))
            return render_template('register.html', form=form)
        else:
            session['email'] = form.email.data
            # session['username'] = form.username.data
            session['password'] = form.password.data
            # try:
            messag = Message('confirmation code',
                             sender="jousefgamal46@gmail.com",
                             recipients=[form.email.data])
            session['confirmationion'] = "".join(random.choice(string.digits) for x in range(random.randint(1, 7)))
            # link = f"http://127.0.0.1:5000/reset?de={session['verification']}"
            print(session['confirmationion'])
            messag.body = f"Here is the confirmation code copy it and put it into the confirmation box to  your password " \
                f"{session['confirmationion']} "
            messag.html = render_template('/confirmationmail.html')
            mail.send(messag)
            session['qwertyuiopdfghjkldfghjklsdfghjkfghjk'] = True
            return redirect(url_for('users.confirmation'))
            # except Exception as e:
            #     print(e)
            #     session['qwertyuiopdfghjkldfghjklsdfghjkfghjk'] = False
    print(form.errors)
    return render_template('register.html', form=form)


@users.route("/confirmation", methods=['post', 'get'])
def confirmation():
    if current_user.is_authenticated:
        return render_template('logged_in_already.html')
    try:
        if session['qwertyuiopdfghjkldfghjklsdfghjkfghjk']:
            print('i am happy')
            form = confirmationForm()
            if form.validate_on_submit():
                print('i am happy')
                print(session['confirmationion'])
                if session['confirmationion'] == form.password.data:
                    ser = Users(email=session['email'], username=session['username'], password=session['password'],
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
    except Exception as e:
        abort(404)
    return redirect("/")


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
        print(form.email.data)
        d = Users.query.filter_by(email=form.email.data).first()
        print(Users.query.filter_by(email='abahormelad@gmail.com').first().email)
        print(d)
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
                link = f"http://127.0.0.1:5000/reset?de={session['verification']}"
                msg.body = f"Here is the reset link copy it and put it into your browser to reset your password " \
                    f"http:/127.0.0.1/reset?de={session['verification']}'>reset password</a>"
                msg.html = render_template('/resetpassword.html', link=link)
                mail.send(msg)
                flash(Markup('<div class="alert alert-success" role="alert">The email have been sent</div>'))
            except:
                abort(404)
    return render_template('forget-password.html', form=form)


@users.route('/reset', methods=['post', 'get'])
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
        abort(404)
    return redirect('/')


@users.route('/change')
def change():
    form = changepassword()
    if form.validate_on_submit():
        d = Users.query.filter_by(email=form.email.data).first()
        if check_password_hash(current_user.password, form.password.data):
            current_user.password = generate_password_hash(form.password_new.data)
            try:
                db.session.commit()
            except:
                db.rollback()
    return render_template('change_password.html', form=form)


@users.route('/account')
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


@users.route('/username')
def username_check():
    del session['email_checked']
    c = request.form['c']
    p = Users.query.filter_by(email=c).first()
    if p:
        session['email_checked'] = c
        return True


@users.route('/password')
def password_check():
    if session['email_checked']:
        user = Users.query.filter_by(email=session['email_checked'])
        d = request.form['c']
        if user.check_password(d):
            pass


@users.route('/test')
def test():
    d = request.args.get('te')
    print(session['testing'])
    session['testing'].append(d)
    for i in session['testing']:
        print(i)
    return 'added'


@users.route('/get')
def get():
    # get = session['testing']
    print(session['testing'])
    return str(session['testing'])


@users.route('/d')
def d():
    session['testing'] = []
    return ''


@users.route('/keep_alive')
def keep_alive():
    token = request.args.get('token')
    update_user_active_date(token)
    id = request.args.get('id')
    sid = request.sid
    if active_users.query.filter_by(user_id=id).first() is None:
        active_users(user_id=id, request_sid=sid)
    else:
        current = active_users.query.filter_by(user_id=id)
        current_user.date = datetime.utcnow()

    return 'success'


def check_if_user_is_authenticated():
    d = authenticated_user.query.all()
    for i in d:
        if datetime.utcnow() - i.date > timedelta(hours=1):
            db.session.delete(i)
            db.session.commit()


def update_the_active_users():
    d = active_users.query.all()
    for i in d:
        if datetime.utcnow() - i.date > timedelta(seconds=10):
            db.session.delete(i)
            db.session.commit()


while True:
    time.sleep(10)
    update_the_active_users()
    check_if_user_is_authenticated()
