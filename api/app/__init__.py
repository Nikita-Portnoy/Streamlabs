from flask import Flask, jsonify, abort

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('../config_dev.cfg')

    from app.api import API
    app.register_blueprint(API)

    return app