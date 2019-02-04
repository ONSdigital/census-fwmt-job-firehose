from flask import Flask, request, g, Response
import xml.etree.ElementTree as ET
import json
import os
import random

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from . import db
    db.init_app(app)
    from . import rabbit
    rabbit.init_app(app)
    from . import rm_builder
    rm_builder.init_app(app)

    app.config.from_mapping(
        SECRET_KEY = 'secret',
        RABBIT_URL = 'localhost',
        RABBIT_USERNAME = 'guest',
        RABBIT_PASSWORD = 'guest',
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_pyfile('config.py', silent=False)

    @app.route("/rm/actionRequest", methods=['GET', 'POST'])
    def handle_rm_action_request():
        count = int(request.args.get('count'))

        def make_message():
            id = db.generate_id()
            address = db.pick_address()
            contact = pick_contact()
            tree = rm_builder.construct_RM_action_request(id, address, contact)
            xml = ET.tostring(tree, encoding='unicode')
            return xml

        if request.method == 'GET':
            messages = []
            for _ in range(count):
                messages.append(make_message())
            return Response(json.dumps(messages), mimetype='application/json')
        elif request.method == 'POST':
            rabbit = RabbitProxy()
            for _ in range(count):
                success = rabbit.send(make_message())
                if not success:
                    print('Message could not be confirmed')
                    raise Exception()
            rabbit.close()
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
