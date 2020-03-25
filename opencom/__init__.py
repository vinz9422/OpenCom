import os

from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path,'opencom.sqlite')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db, auth, compte
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(compte.bp)

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template("404.html"), 404

    @app.route("/")
    def index():
        return render_template('index.html')

    return app
