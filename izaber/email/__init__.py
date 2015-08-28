import smtplib
import logging

from email.parser import Parser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup

from izaber import config, app_config
from izaber.startup import initializer
from izaber.paths import paths
from izaber.templates import parse

log = logging.getLogger('email')

class Mailer(object):
    def load_config(self,**options):
        self.options = options

    def sendmail(self,*args,**kwargs):
        host = self.options.get('host',config.email.host)
        server = smtplib.SMTP(host)
        server.sendmail(*args,**kwargs)
        server.quit()

    def send_message(self,msg):
        return self.sendmail(
                    msg['from'],
                    msg['to'],
                    msg.as_string()
                )

    def basic_send(
              self,
              from_addr,
              to_addrs,
              subject,
              body
          ):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = ", ".join(to_addrs)
        self.sendmail(from_addr,to_addrs,msg.as_string())

    def template_send(self,fpath,**kwargs):
        msg = self.template_parse(fpath,**kwargs)
        if self.options.get('debug'):
            log.debug(msg.as_string())
        else:
            to = msg['to']
            if isinstance(to,basestring):
                to = [to.split(',')]
            self.sendmail(
                msg['from'],
                to,
                msg.as_string()
            )

    def template_parse(self,fpath,**tags):

        tags['config'] = config.dict()

        parsed_email = parse(fpath,**tags)

        e = Parser().parsestr(parsed_email)

        msg = MIMEMultipart('alternative')
        for k,v in dict(e).iteritems():
            msg[k] = v

        html = e.get_payload()

        soup = BeautifulSoup(html,"html5lib")
        text = soup.get_text()

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        return msg

mailer = Mailer()

@initializer('email')
def load_config(**options):
    email_config = config.email.dict()
    mailer.load_config(**email_config)

