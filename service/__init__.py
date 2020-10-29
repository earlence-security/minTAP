import os
from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ifttt_reddit.sqlite'),
        CHANNEL_KEY='W0SCQpkbG-ogYLgMVUI-KM-LPodRZP1yJjPPfUX6BNAvPG-qXVGRqGG3avnS3bBJ'
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