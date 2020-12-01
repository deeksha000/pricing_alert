from flask import render_template, url_for, session, Blueprint, redirect, request
import json
from models.user import User, UserErrors

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email
            return email
        except UserErrors.UserError as e:
            return e.message
    return render_template('users/register.html')


@user_blueprint.route('/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.login_valid(email, password):
                session['email'] = email
                return render_template('users/page.html')
        except UserErrors.UserError as e:
            return e.message
    return render_template('users/login.html')


@user_blueprint.route('/logout', methods=['GET', 'POST'])
def logout_user():
    session['email'] = None
    return redirect(url_for('.login_user'))
