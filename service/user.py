from flask import Blueprint, request, current_app

bp = Blueprint('user', __name__, url_prefix='/ifttt/v1/user')


@bp.route("/info", methods=['GET', 'POST'])
def user_info():

    data = {"data": {
        "name": "Demo User",
        "id": "heisenberg",
    }
    }

    return data
