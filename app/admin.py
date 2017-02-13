from flask import render_template, request, redirect, url_for, session, Blueprint


admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_panel():
    return "TODO"
