from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = ''
    with app.app_context():
        from .api import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
    return app
