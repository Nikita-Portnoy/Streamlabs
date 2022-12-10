from flask import Flask
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    jwt = JWTManager(app)

    app.config.from_pyfile('../config_dev.cfg')

    from app.api import API
    app.register_blueprint(API)

    #JWT Identity Loader
    @jwt.user_identity_loader
    def jwt_identity(user):
        return user.public_id

    return app