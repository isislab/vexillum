


def init_utils(app):
    app.jinja_env.globals.update(signed_up=signed_up)
    app.jinja_env.globals.update(joined_group=joined_group)
    app.jinja_env.globals.update(check_rated=check_rated)

def init_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def general_error(error):
        return render_template('errors/500.html'), 500
