from flask import Blueprint, render_template
from .models import UserType


main = Blueprint('main', __name__)


@main.context_processor
def context_data():

    return dict(
        admin=UserType.Admin.name,
        client=UserType.Client.name,
    )


@main.route('/')
def index():

    return render_template('index.html')