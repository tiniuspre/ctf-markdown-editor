import sqlalchemy
from flask import Flask
from flask_login import LoginManager

from users.models import db, Users

from users.index import index
from users.login import login
from users.logout import logout
from users.register import register
from users.home import home
from users.profile import profile

from werkzeug.security import generate_password_hash

import os

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')

app.config['SECRET_KEY'] = os.getenv('secret_key', 'secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['REMEMBER_COOKIE_HTTPONLY'] = False

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
app.app_context().push()

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(home)
app.register_blueprint(profile)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def create_db():
    db.create_all()
    try:
        hashed_password = generate_password_hash(os.getenv("ADMIN_PASSWORD", "passord"), method='pbkdf2')
        admin = Users(username='admin', password=hashed_password, markdown="#"+os.getenv("flag", "flag{test}"), admin=True)
        db.session.add(admin)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


create_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
