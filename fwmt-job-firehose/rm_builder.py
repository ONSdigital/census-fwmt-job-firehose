import xml.etree.ElementTree as ET

def init_app(app):
    pass

def construct_RM_action_request(id, address_data, contact_data):
    ins         = ET.Element('actionInstruction')
    req         = ET.SubElement(ins, 'actionRequest')
    actionPlan  = ET.SubElement(req, 'actionPlan')
    actionType  = ET.SubElement(req, 'actionType') # mandatory
    questionSet = ET.SubElement(req, 'questionSet')

    contact                   = ET.SubElement(req, 'contact')
    contact_title             = ET.SubElement(contact, 'title')
    contact_title.text        = contact_data.get('title', None)
    contact_forename          = ET.SubElement(contact, 'forename')
    contact_forename.text     = contact_data.get('forename', None)
    contact_surname           = ET.SubElement(contact, 'surname')
    contact_surname.text      = contact_data.get('surname', None)
    contact_phoneNumber       = ET.SubElement(contact, 'phoneNumber')
    contact_phoneNumber.text  = contact_data.get('phoneNumber', None)
    contact_emailAddress      = ET.SubElement(contact, 'emailAddress')
    contact_emailAddress.text = contact_data.get('emailAddress', None)
    contact_ruName            = ET.SubElement(contact, 'ruName')
    contact_ruName.text       = contact_data.get('ruName', None)
    contact_tradingStyle      = ET.SubElement(contact, 'tradingStyle')
    contact_tradingStyle.text = contact_data.get('tradingStyle', None)

    address                       = ET.SubElement(req, 'address') # mandatory
    address_sampleUnitRef         = ET.SubElement(address, 'sampleUnitRef') # mandatory
    address_sampleUnitRef.text    = address_data.get('sampleUnitRef', None)
    address_type                  = ET.SubElement(address, 'type')
    address_type.text             = address_data.get('type', None)
    address_estabType             = ET.SubElement(address, 'estabType')
    address_estabType.text        = address_data.get('estabType', None)
    address_locality              = ET.SubElement(address, 'locality')
    address_locality.text         = address_data.get('locality', None)
    address_organisationName      = ET.SubElement(address, 'organisationName')
    address_organisationName.text = address_data.get('organisationName', None)
    address_category              = ET.SubElement(address, 'category')
    address_category.text         = address_data.get('category', None)
    address_line1                 = ET.SubElement(address, 'line1')
    address_line1.text            = address_data.get('line1', None)
    address_line2                 = ET.SubElement(address, 'line2')
    address_line2.text            = address_data.get('line2', None)
    address_line3                 = ET.SubElement(address, 'line3')
    address_line3.text            = address_data.get('line3', None)
    address_line4                 = ET.SubElement(address, 'line4')
    address_line4.text            = address_data.get('line4', None)
    address_townName              = ET.SubElement(address, 'townName')
    address_townName.text         = address_data.get('townName', None)
    address_postcode              = ET.SubElement(address, 'postcode')
    address_postcode.text         = address_data.get('postcode', None)
    address_country               = ET.SubElement(address, 'country')
    address_country.text          = address_data.get('country', None)
    address_ladCode               = ET.SubElement(address, 'ladCode')
    address_ladCode.text          = address_data.get('ladCode', None)
    address_latitude              = ET.SubElement(address, 'latitude')
    address_latitude.text         = address_data.get('latitude', '0')
    address_longitude             = ET.SubElement(address, 'longitude')
    address_longitude.text        = address_data.get('longitude', '0')

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

