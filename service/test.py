import secrets
from flask import Blueprint, request, current_app

bp = Blueprint('test', __name__, url_prefix='/ifttt/v1/test')


@bp.route("/setup", methods=['GET', 'POST'])
def test_setup():
    if request.headers['IFTTT-Channel-Key'] != current_app.config['CHANNEL_KEY']:
        return '', 401

    data = {'data':
        {'samples':
            {'triggers':
                {
                    'mintap_toy_trigger':
                        {'author': 'Alice',
                         'filter_code': secrets.token_hex(32),
                         'code_signature': secrets.token_hex(32)},

                }
            },
            "accessToken": current_app.config['ACCESS_TOKEN']
        }
    }

    return data
