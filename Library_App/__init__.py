from flask import Flask
from .models import db
from dotenv import load_dotenv


load_dotenv()


def create_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app