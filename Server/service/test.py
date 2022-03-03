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
                         'code_signature': '36iVB8KCUg09IGlYcl8Ky8AVjV7XZyRGFvqj21CJ+O0Od2dbthqNAddT3CFkVpKp41hSgboorlyvE+Knu7qqN7WzKqph/UM36I+n+t5o3XBDFu/oFMoq6Rc95VdM6o0erTE/8y2Mb+2kLSDQGl7gVs19Fq1VY/7EfpqnjX+FI6zExad+uzS26ZnfcyhRCPW8BKC9azL3yIgsOeUgLLxBcvZkbKv/YyYgTVyODmS/2feo5x8Ab1X7vwJMRQpYmfx4dLIvXPmOdKO9Z0pmm3YPHTPJSR1p3byBjdKS9gzSJDJDtW4gIFQrAtjjppWYWpJyMvo/FPlWZy2e7TX4rtml6A==',
                         'filter_code': "%0Afunction%20filter(data)%20%7B%0Avar%20data2%20=%20data.copy()%0Aconst%20Trigger%20=%20new%20mintapToyTrigger(data2);%0Aconst%20MintapService%20=%20%7BmintapToyTrigger:%20Trigger%7D;%0Aconst%20Action%20=%20new%20DummyAction();%0A%0Alet%C2%A0x%C2%A0=%C2%A0MintapService.mintapToyTrigger.Title%0A%C2%A0%0Aif%C2%A0(x%C2%A0===%C2%A0'Demo%C2%A0Skip%C2%A0Title')%C2%A0%7B%0A%C2%A0%C2%A0return%20null;%0A%7D%0A%C2%A0%0AAction.action(MintapService.mintapToyTrigger.Content)%0AAction.action(MintapService.mintapToyTrigger.Title)%0A%20%20%20%20%0Areturn%20MintapService.mintapToyTrigger.accessedFields();%0A%0A%7D%20%20%20%0A"},

                }
            },
            "accessToken": current_app.config['ACCESS_TOKEN']
        }
    }

    return data
