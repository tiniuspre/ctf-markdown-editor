import uuid

import sqlalchemy
from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .models import db, Users

register = Blueprint('register', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(register)


@register.route('/register', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not username or not password1 or not password2:
            return redirect(url_for('register.show') + '?error=missing-fields')
        if password1 != password2:
            return redirect(url_for('register.show') + '?error=passwords-dont-match')

        hashed_password = generate_password_hash(password1, method='pbkdf2')
        try:
            new_user = Users(
                username=username,
                password=hashed_password,
                uuid=str(uuid.uuid4()),
            )

            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return redirect(url_for('register.show') + '?error=user-exists')

        return redirect(url_for('login.show') + '?success=account-created')

    else:
        return render_template('register.html')