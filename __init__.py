from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response
import xml.etree.ElementTree as ET
import json
import pika
import uuid
import random

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = 'secret',
        ADDRESS_FILES = '',
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

# # # ID
def generate_id():
    id = str(uuid.uuid4())
    get_db().cursor().execute('''INSERT INTO ids (id) VALUES (?)''', (id,))
    return id

# # # ADDRESSES
addresses = None

def load_addresses():
    addresses = []
    files = app.config['ADDRESS_FILES'].split(';')
    for f in files:
        with open(f) as text:
            j = json.load(text)
            addresses.extend(j['addresses'])
    return addresses

def get_addresses():
    global addresses
    if addresses == None:
        addresses = load_addresses()
    return addresses

def pick_address():
    return random.choice(get_addresses())

# # # CONTACTS
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

# # # RM ACTION REQUEST
def construct_RM_action_request():
    data_address = pick_address()
    data_contact = pick_contact()
    id = generate_id()

    ins         = ET.Element('actionInstruction')
    req         = ET.SubElement(ins, 'actionRequest')
    actionPlan  = ET.SubElement(req, 'actionPlan')
    actionType  = ET.SubElement(req, 'actionType') # mandatory
    questionSet = ET.SubElement(req, 'questionSet')

    contact                   = ET.SubElement(req, 'contact')
    contact_title             = ET.SubElement(contact, 'title')
    contact_title.text        = data_contact.get('title', None)
    contact_forename          = ET.SubElement(contact, 'forename')
    contact_forename.text     = data_contact.get('forename', None)
    contact_surname           = ET.SubElement(contact, 'surname')
    contact_surname.text      = data_contact.get('surname', None)
    contact_phoneNumber       = ET.SubElement(contact, 'phoneNumber')
    contact_phoneNumber.text  = data_contact.get('phoneNumber', None)
    contact_emailAddress      = ET.SubElement(contact, 'emailAddress')
    contact_emailAddress.text = data_contact.get('emailAddress', None)
    contact_ruName            = ET.SubElement(contact, 'ruName')
    contact_ruName.text       = data_contact.get('ruName', None)
    contact_tradingStyle      = ET.SubElement(contact, 'tradingStyle')
    contact_tradingStyle.text = data_contact.get('tradingStyle', None)

    address                       = ET.SubElement(req, 'address') # mandatory
    address_sampleUnitRef         = ET.SubElement(address, 'sampleUnitRef') # mandatory
    address_sampleUnitRef.text    = data_address.get('sampleUnitRef', None)
    address_type                  = ET.SubElement(address, 'type')
    address_type.text             = data_address.get('type', None)
    address_estabType             = ET.SubElement(address, 'estabType')
    address_estabType.text        = data_address.get('estabType', None)
    address_locality              = ET.SubElement(address, 'locality')
    address_locality.text         = data_address.get('locality', None)
    address_organisationName      = ET.SubElement(address, 'organisationName')
    address_organisationName.text = data_address.get('organisationName', None)
    address_category              = ET.SubElement(address, 'category')
    address_category.text         = data_address.get('category', None)
    address_line1                 = ET.SubElement(address, 'line1')
    address_line1.text            = data_address.get('line1', None)
    address_line2                 = ET.SubElement(address, 'line2')
    address_line2.text            = data_address.get('line2', None)
    address_line3                 = ET.SubElement(address, 'line3')
    address_line3.text            = data_address.get('line3', None)
    address_line4                 = ET.SubElement(address, 'line4')
    address_line4.text            = data_address.get('line4', None)
    address_townName              = ET.SubElement(address, 'townName')
    address_townName.text         = data_address.get('townName', None)
    address_postcode              = ET.SubElement(address, 'postcode')
    address_postcode.text         = data_address.get('postcode', None)
    address_country               = ET.SubElement(address, 'country')
    address_country.text          = data_address.get('country', None)
    address_ladCode               = ET.SubElement(address, 'ladCode')
    address_ladCode.text          = data_address.get('ladCode', None)
    address_latitude              = ET.SubElement(address, 'latitude')
    address_latitude.text         = data_address.get('latitude', '0')
    address_longitude             = ET.SubElement(address, 'longitude')
    address_longitude.text        = data_address.get('longitude', '0')

    legalBasis       = ET.SubElement(req, 'legalBasis')
    region           = ET.SubElement(req, 'region')
    respondentStatus = ET.SubElement(req, 'respondentStatus')
    enrolmentStatus  = ET.SubElement(req, 'enrolmentStatus')
    caseGroupStatus  = ET.SubElement(req, 'caseGroupStatus')
    caseId           = ET.SubElement(req, 'caseId')
    caseId.text      = id
    priority         = ET.SubElement(req, 'priority') # enum-limited to 'highest', 'higher', 'medium', 'lower', 'lowest'
    priority         = 'medium'
    caseRef          = ET.SubElement(req, 'caseRef') # id
    caseRef.text     = id
    iac              = ET.SubElement(req, 'iac')

    events  = ET.SubElement(req, 'events') # mandatory
    # event_1 = ET.SubElement(events, 'event', text = 'foo')

    exerciseRef       = ET.SubElement(req, 'exerciseRef')
    userDescription   = ET.SubElement(req, 'userDescription')
    surveyName        = ET.SubElement(req, 'surveyName')
    surveyRef         = ET.SubElement(req, 'surveyRef') # 'HH', 'CCS' or 'CE' to match a job service component
    surveyRef.text    = 'HH'
    returnByDate      = ET.SubElement(req, 'returnByDate')
    returnByDate.text = '01/01/1999'
    return ins

# # # RABBIT
class RabbitProxy:
    def __init__(self):
        self.connection = pika.BlockingConnection()
        self.channel = self.connection.channel()
        self.channel.confirm_delivery()
        self.properties = pika.BasicProperties(content_type = 'text/json', delivery_mode = 1)

    def send(self, msg):
        return self.channel.basic_publish(
            exchange    = '',
            routing_key = 'Action.Field',
            body        = msg,
            properties  = self.properties)

    def close(self):
        self.connection.close()

# # # REQUESTS
@app.route("/rm/actionRequest", methods=['GET', 'POST'])
def handle_rm_action_request():
    count = int(request.args.get('count'))

    def make_message():
        tree = construct_RM_action_request()
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
