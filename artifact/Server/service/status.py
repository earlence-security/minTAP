from flask import Blueprint, request, current_app

bp = Blueprint('status', __name__, url_prefix='/ifttt/v1/')


@bp.route('/status', methods=['GET', 'POST'])
def status():
    if request.headers['IFTTT-Channel-Key'] != current_app.config['CHANNEL_KEY']:
        return '', 401

    return ''
