from flask import Flask, url_for
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO, send, emit
# from flask_session import Session

app = Flask(__name__)

# SESSION_TYPE = 'redis'
# Session(app)
# socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'mykeyasdfghjklsdfghnjm'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://codeXz:hpprobook450g3*@127.0.0.1/server_encryption_'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeLrKgUAAAAAJg9CiLKCdXH1igYZPw6m1rJ8X3o'
# app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeLrKgUAAAAAHE9JIIuXxvmN7TgubnMtpA7Jfpw'

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
    MAIL_USERNAME='mohsengamal100@gmail.com',
    MAIL_PASSWORD='mohsen123456789'
)

mail = Mail(app)

db = SQLAlchemy(app)
Migrate(app, db)

login = LoginManager()
login.init_app(app)
login.login_view = 'users.login'
login.refresh_view = 'users.change'

from myproject.users.users import users
# from myproject.main.main import main


app.register_blueprint(users)
# app.register_blueprint(main)
