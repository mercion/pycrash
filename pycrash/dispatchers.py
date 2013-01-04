'''
Dispatchers are responsible for handle'ing the raw XML crash report and senfding
it to the appropriate location.
'''
import smtplib

from __init__ import XMLtoHTML
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders


class BaseDispatcher(object):
    def dispatch(self, xml_crash_report):
        raise NotImplementedError()

class XMLMailDispatcher(BaseDispatcher):
    '''
    This dispatcher will take the xml crash dump and generate an
    email message. The body of the message will contain a summary
    of the crash dump, with the full XML report atached to the email.
    '''
    def __init__(self, from_address, to_address, outbound_server):
        self.from_address = from_address
        self.to_address = to_address
        self.outbound_server = outbound_server
        self.server = smtplib.SMTP()
        self.server.connect(outbound_server)

    def dispatch(self, xml_crash_report):
        msg = MIMEText(xml_crash_report)
        msg['Subject'] = 'ACR'
        msg['From'] = self.from_address
        msg['To'] = self.to_address

        self.server.sendmail(self.from_address,
                   [self.to_address],
                   msg.as_string())


class HTMLMailDispatcher(BaseDispatcher):
    '''
    This dispatcher will take the XML crash report and generate
    a HTML crash report. This html crash report will then be 
    sent as an email to the :param:to_address. The XML report
    will also be attached to this email.
    '''
    def __init__(self, from_address, to_address, outbound_server):
        self.from_address = from_address
        self.to_address = to_address
        self.outbound_server = outbound_server
        self.server = smtplib.SMTP()
        self.server.connect(outbound_server)

    def _XMLtoHTML(self, xml_report):
        return XMLtoHTML(xml_report)

    def dispatch(self, xml_crash_report):
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = 'ACR'
        MESSAGE['To'] = self.to_address
        MESSAGE['From'] = self.from_address
        MESSAGE.preamble = 'Your email client does not support HTML! sorry dude'

        HTML_BODY = MIMEText(self._XMLtoHTML(xml_crash_report), 'html')

        MESSAGE.attach(HTML_BODY)

        #Lets atch the XML report
        part = MIMEBase('application', "octet-stream")
        part.set_payload(xml_crash_report)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 
                        'attachment; filename="report.xml"')
        MESSAGE.attach(part)
        

        self.server.sendmail(self.from_address,
                   [self.to_address],
                   MESSAGE.as_string())

class XMLPostDispatcher(BaseDispatcher):
    '''
    This dispatcher will take the xml_report and then submit
    a HTTP POST request to the :pram:target_uri. The body of the POST
    message will contain the XML crash report. 
    '''

    pass

def generate_http_report(xml_crash_report):
    pass


    
