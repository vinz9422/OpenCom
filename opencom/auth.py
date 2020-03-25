import functools

from flask import (Blueprint, flash, g, redirect, url_for, render_template, request, session)

from werkzeug.security import check_password_hash, generate_password_hash

from opencom.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['pwd']
        db = get_db()
        error = None

        if not username:
            error = "Nom d'utilisateur requis"
        elif not pwd:
            error = "Password requis"
        elif db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            error = "Nom d'utilisateur {} deja pris!".format(username)

        if error is None:
            db.execute('INSERT INTO users (username, pwd) VALUES (?, ?)',(username,generate_password_hash(pwd)))
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['pwd']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = "Utilisateur inconnu"
        elif not check_password_hash(user['pwd'],pwd):
            error = "Mot de passe erroné"

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('logout')
def logout():
    if g.user is not None:
        session.clear()

    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_views(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    
    return wrapped_views