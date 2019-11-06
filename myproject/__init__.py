from flask import Flask, url_for
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)

socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'mykeyasdfghjklsdfghnjm'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://codeXz:hpprobook450g3*@127.0.0.1/server_encryption_'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10000 per day", "300 per hour"]
)

app.config.update(
    debug=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='jousefgamal46@gmail.com',
    MAIL_PASSWORD='jousefgamal123456789'
)

mail = Mail(app)

db = SQLAlchemy(app)
Migrate(app, db)

login = LoginManager()
login.init_app(app)
login.login_view = 'users.login'


from myproject.users.users import users
# from myproject.main.main import main

app.register_blueprint(users)
# app.register_blueprint(main)
