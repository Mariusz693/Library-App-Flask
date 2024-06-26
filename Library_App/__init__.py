from flask import Flask
from .models import db, User
from dotenv import load_dotenv
from flask_login import LoginManager


load_dotenv()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app