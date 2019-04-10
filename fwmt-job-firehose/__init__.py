from flask import Flask, request, g, Response
import xml.etree.ElementTree as ET
import json
import os
import random

def config_by_env(app, env):
    val = os.environ.get(env, default=None)
    if val:
        app.config[env] = val

def config_app(app):
    # default values
    app.config.from_mapping(
        SECRET_KEY = 'secret',
        RABBIT_URL = 'amqp://guest:guest@localhost:5672/%2F',
    )

    # disk configuration
    app.config.from_pyfile('config.py', silent=False)

    # environmental overrides
    config_by_env(app, 'SECRET_KEY')
    config_by_env(app, 'RABBIT_URL')

def get_arg_or_fail(request, name):
    arg = request.args.get(name)
    if not arg:
        raise ValueError("Invalid argument: " + name)
    return arg

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from . import db
    db.init_app(app)
    from . import rabbit
    rabbit.init_app(app)
    from . import rm_builder
    rm_builder.init_app(app)
    from . import pause_builder
    pause_builder.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    config_app(app)

    @app.route("/info", methods=['GET'])
    def handle_info():
        return "Ready!"

    @app.route("/rm/actionRequest", methods=['GET', 'POST'])
    def handle_rm_action_request():
        count = int(get_arg_or_fail(request, 'count'))

        def make_message():
            id = db.generate_id()
            address = db.pick_address()
            contact = pick_contact()
            pause = pause_builder.construct_pause()
            tree = rm_builder.construct_RM_action_request(id, address, contact, pause)
            xml = ET.tostring(tree, encoding='unicode')
            return xml

        if request.method == 'GET':
            messages = []
            for _ in range(count):
                messages.append(make_message())
            return Response(json.dumps(messages), mimetype='application/json')
        elif request.method == 'POST':
            proxy = rabbit.RabbitProxy(app.config['RABBIT_URL'])
            for _ in range(count):
                success = proxy.send(make_message())
                if not success:
                    print('Message could not be confirmed')
                    raise Exception()
            proxy.close()
            return Response()

    return app

def pick_contact():
    return {
        'title':         'Mr',
        'forename':      'John',
        'surname':       'Smith',
        'phoneNumber':   '00000000000',
        'emailAddress':  'john.smith@email.com',
        'ruName':        '',
        'tradingStyle':  ''
    }
