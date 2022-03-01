import os
from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ifttt_reddit.sqlite'),
        CHANNEL_KEY='g6Ra5M_VZyn-NM4N6zgCdlGyYbOXieTx6FK1a0kpbAN9268iYnhXPNfYHhkXvoz2',
        CLIENT_ID='24ad3856fc2d8b8caaa96f2af275abf4',
        CLIENT_SECRET='acb0d5760dd8ea29d601825131e8e2dd98febad0934f55b727bc13039dfa4c65',
        ACCESS_TOKEN='e513b0b35a82b47fc6729716e8fac57e77e85995dd054a86fa495728bfca8ae540e0b4c14fce4e60'
    )

    from . import db
    db.init_app(app)


    from . import trigger, status, test, auth, user
    app.register_blueprint(trigger.bp)
    app.register_blueprint(status.bp)
    app.register_blueprint(test.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)

    return app