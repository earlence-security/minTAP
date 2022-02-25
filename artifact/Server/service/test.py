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
                          {'new_top_post':
                               {'subreddit': 'worldnews',
                                'filter_code': secrets.token_hex(32),
                                'code_signature': secrets.token_hex(32)},
                           'new_test_data':
                               {'subreddit': 'worldnews',
                                'filter_code': secrets.token_hex(32),
                                'code_signature': secrets.token_hex(32)},

                          }
                      },
                 "accessToken": "taSvYgeXfM1HjVISJbUXVBIw1YUkKABm"
                 }
            }

    return data