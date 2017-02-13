from flask import render_template, request, redirect, url_for, session, Blueprint


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "TODO"
